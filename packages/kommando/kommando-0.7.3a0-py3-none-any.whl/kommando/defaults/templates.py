"""
MIT License

Copyright (c) 2018 Andre Augusto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import re
import random
import asyncio
import discord
import inspect

from functools import lru_cache

def parameters(f):
    exclude = ['self', 'cls', 'ktx']
    _par = inspect.signature(f).parameters
    _par_list = [x for x in _par if x not in exclude]
    return {x: _par[x] for x in _par_list}

def get_invocation(query, root):
    if query in root:
        return root[query]
    else:
        for _, invocation in root.items():
            if hasattr(invocation, '__share__'):
                search = invocation.__share__(query)
                if search:
                    break
    try:  
        return search
    except UnboundLocalError:
        return None

def remove_invocation(query, root):
    search = get_invocation(query, root)
    if search:
        search.__uninstall__()
        return True
    return False

class Common:
    def __init__(self, **kwargs):
        self.id, self.function = None, None
        self.scroll, self.stats = None, None
        self.split = lambda x: x.split()
        self.root, self.bot = None, None

        self.__dict__ = {**self.__dict__, **kwargs}

    def arg_parser(self, ktx):
        hargs = ktx.hargs

        pars = parameters(self.function)

        args = []
        kwargs = {}
        n = 0

        def parse(kind, ann):
            nonlocal n
            if kind is inspect._VAR_POSITIONAL:
                if hargs[n:]:
                    if ann is None:
                        val = hargs[n:]
                    else:
                        try:
                            return ann(ktx, hargs[n:])
                        except TypeError:
                            return ann(hargs[n:])
                    n = len(hargs) - 1
                    return val
                else:
                    raise IndexError
            elif ann is not None:
                if callable(ann):
                    try:
                        return ann(ktx, hargs[n])
                    except TypeError:
                        return ann(hargs[n])
                elif type(ann) in (list, set, tuple):
                    for x in ann:
                        try:
                            return parse(kind, x)
                        except ValueError:
                            pass
                    raise ValueError
                else:
                    ktx.logger.warning(f'Strange annotation: {ann}')
            return hargs[n]

        for k, v in pars.items():
            try:
                kind = v.kind 
                ann = v.annotation if v.annotation is not v.empty else None
                if kind is v.POSITIONAL_OR_KEYWORD:
                    if v.default is v.empty:
                        args.append(parse(kind, ann))
                    else:
                        kwargs[k] = parse(kind, ann)
                elif kind is v.VAR_POSITIONAL:
                    args.extend(parse(kind, ann))
                elif kind is v.KEYWORD_ONLY:
                    kwargs[k] = parse(kind, ann)
                elif kind is v.VAR_KEYWORD:
                    raise ValueError
                n += 1
            except (IndexError, ValueError):
                break

        for k, v in pars.items():
            if k not in kwargs and v.default is not v.empty:
                kwargs[k] = v.default

        min_args = len([k for k,v in pars.items() if v.default is v.empty])

        if n >= min_args:
            return args, kwargs
        else:
            return None, None

    def _common_split(self, ktx):
        return self.split(ktx.message.content)

    def __install__(self):
        if self.root is not None:
            root = get_invocation(self.root, root=self.bot.invocations)
            root.sub_invocations[self.id] = self
        else:
            self.bot.invocations[self.id] = self
            
    def __uninstall__(self):
        if self.root is not None:
            root = get_invocation(self.root, root=self.bot.invocations)
            del root.sub_invocations[self.id]
        else:
            del self.bot.invocations[self.id]

    @lru_cache()
    def translation(self, language):
        def parse(r):
            if type(r) == str:
                return r
            elif type(r) in (tuple, list):
                return random.choice(r)
            elif type(r) is dict:
                for x in self.bot.emotional_state:
                    if x in r:
                        return parse(r[x])
        data = {}
        try:
            lang_data = self.bot.dictionary[language]
            lang_data = lang_data['specific'][self.scroll][self.id]
            data['name'] = parse(lang_data['__name__'] if '__name__' in lang_data else self.id)
            data['description'] = parse(lang_data['__desc__'] if '__desc__' in lang_data else '\u200b')
            if '__regex__' in lang_data:
                data['regex'] = parse(lang_data['__regex__'])
        except KeyError:
            data['name'] = self.id
            data['description'] = '\u200b'
        return data

class Container(Common):
    def __init__(self, **kwargs):
        self.sub_invocations = {}
        self.split = None
        self.color = None
        self.root = None
        super().__init__(**kwargs)

    def __len__(self):
        i = 0
        for v in self.sub_invocations.values():
            if hasattr(v, '__len__'):
                i += len(v)
            else:
                i += 1
        return i

    def __share__(self, query):
        return get_invocation(query, root=self.sub_invocations)

    async def __check__(self, ktx):
        for v in self.sub_invocations.values():
            invocation = await asyncio.coroutine(v.__check__)(ktx)
            if invocation:
                return invocation

    @lru_cache()
    def usage(self, language):
        if not hasattr(self.bot, 'color'):
            self.bot.color = 0xAE3333
        trdata = self.translation(language)
        embed = discord.Embed(description=trdata['description'], 
                              color=self.color or self.bot.color)
        embed.set_author(name=trdata['name'], 
                         icon_url=self.bot.client.user.avatar_url)
        for _, v in self.sub_invocations.items():
            if hasattr(v, 'field'):
                kwargs = v.field(language)
                embed.add_field(**kwargs)
        return embed
    
    @lru_cache()   
    def field(self, language):
        trdata = self.translation(language)
        return {'name': trdata['name'], 
                'value': ', '.join([f"**`{x}`**" for x in self.sub_invocations.keys()]),
                'inline': False}

class Group(Container):
    @lru_cache()
    def usage(self, language):
        if not hasattr(self.bot, 'color'):
            self.bot.color = 0xAE3333
        trdata = self.translation(language)
        embed = discord.Embed(description=trdata['description'], 
                              color=self.color or self.bot.color)
        embed.set_author(name=trdata['name'], 
                         icon_url=self.bot.user.avatar_url)
        for _, v in self.sub_invocations.items():
            if hasattr(v, 'field'):
                kwargs = v.field(language)
                kwargs['name'] = f'{self.id} {kwargs["name"]}'
                embed.add_field(**kwargs)
        return embed

    async def __argf__(self, ktx):
        try:
            splitted = self._common_split(ktx)[1:]
            content = ktx.message.content
            ktx.message.content = content[content.index(splitted[0]):]
            check = [x for x in [v.__check__(ktx) for v in self.sub_invocations.values()] if x]
            if len(splitted) > 0 and any(check):
                ktx.invocation = check[0]
                return await ktx.invoke()
            raise IndexError
        except IndexError:
            if hasattr(self, 'usage'):
                await ktx.send(embed=self.usage(ktx.language))
    
    def __check__(self, ktx):
        trdata = self.translation(ktx.language)
        if ktx.message.content.split()[0] == trdata['name']:
            return self

    @lru_cache()
    def field(self, language):
        trdata = self.translation(language)
        return {'name': trdata['name'], 
                'value': ', '.join([f"**`{trdata['name']} {x}`**" 
                                    for x in self.sub_invocations.keys()]),
                'inline': False}
    
class Command(Common):
    def __init__(self, **kwargs):
        self.color = None
        super().__init__(**kwargs)

    async def __argf__(self, ktx):
        splitted = self._common_split(ktx)
        trdata = self.translation(ktx.language)
        ktx.hargs = splitted[splitted.index(trdata['name']) + 1:]
        result = self.arg_parser(ktx)
        if None not in result:
            return result[0], result[1]
        else:
            if hasattr(self, 'usage'):
                await ktx.send(embed=self.usage(ktx.language))

    def __check__(self, ktx):
        trdata = self.translation(ktx.language)
        if ktx.message.content.split()[0] == trdata['name']:
            return self

    @lru_cache()
    def field(self, language):
        pars = parameters(self.function)
        args = ''.join([f' ({v.name}) ' if v.default is v.empty 
                        else f' [{v.name}]' for v in pars.values()
                        if not v.name.startswith('_')])
        trdata = self.translation(language)
        return {'name': trdata['name'] + args, 'value': trdata['description'],
                'inline': False}
        
    @lru_cache()
    def usage(self, language):
        if not hasattr(self.bot, 'color'):
            self.bot.color = 0xAE3333
        field = self.field(language)
        embed = discord.Embed(title=field['name'], description=field['value'], 
                              color=self.color or self.bot.color)
        return embed

class Summon(Common):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __argf__(self, ktx):
        regex = self.translation(ktx.language)['regex']
        groups = re.match(regex, ktx.message.content).groupdict()
        pars = parameters(self.function)
        kwdefaults = {k: v for k, v in pars.items() if v.default is not v.empty}
        hargs = list(pars)
        for n, x in enumerate(pars):
            try:
                hargs[n] = groups[x]
            except KeyError:
                hargs[n] = kwdefaults[x]
                ktx.logger.warning('The arg ("{x}"), is not on regex')
        ktx.hargs = hargs
        return self.arg_parser(ktx)

    def __check__(self, ktx):
        trdata = self.translation(ktx.language)
        if 'regex' not in trdata:
            ktx.logger.error(f"Invocation without regex!")
            return False
        if re.match(trdata['regex'], ktx.message.content):
            return self

class Subliminal(Common):
    def __init__(self, **kwargs):
        self.arg_regex = re.compile(r'\*([ A-z0-9]*)\*')
        super().__init__(**kwargs)

    def __argf__(self, ktx):
        ktx.hargs = [x[1] for x in self.arg_regex.finditer(ktx.message.content)][1:]
        return self.arg_parser(ktx)

    def __check__(self, ktx):
        rsearch = list(self.arg_regex.finditer(ktx.message.content))
        trdata = self.translation(ktx.language)
        if len(rsearch) >= 1:
            if rsearch[0][1] == trdata['name']:
                return self
