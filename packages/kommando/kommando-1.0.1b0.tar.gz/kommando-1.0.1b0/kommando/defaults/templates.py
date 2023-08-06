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
from itertools import takewhile, dropwhile, tee
from typing import Iterable, Tuple, Union, Callable

from kommando.defaults.types import SpecialType

def _common_split(text:str) -> Tuple[Iterable, Iterable]:
    '''Splits a string in a shlex like way,
    preserving whitespaces inside quotes, but
    allowing open quotes
    
    Parameters:
        text: the string you need to split
    
    Returns:
        A tuple, containing a copy of the cached generator
        and a iterator of the text
    '''
    text = iter(text)
    def _splitter(text):
        while True:
            try:
                n = next(text)
                l = takewhile(lambda x: (x != n) if n == '"' else x.strip(), text)
                l = (n if n != '"' else '') + ''.join(list(filter(lambda x: x != '"', l)))
                if l.strip():
                    yield l
            except StopIteration:
                break
    return _splitter(text), text

def _parameters(f: Callable) -> Iterable[Tuple[str, inspect.Parameter]]:
    '''Get the parameters of a function, ignoring
    self, cls and ktx arguments
    
    Parameters:
        f: A function
    
    Returns:
        A iterable containing tuples (name, parameter)'''
    exclude = ['self', 'cls', 'ktx']
    _par = inspect.signature(f).parameters
    _par_list = filter(lambda x: x not in exclude, _par)
    return ((x, _par[x]) for x in _par_list)

class Common:
    def __init__(self, **kwargs):
        self.id, self.function = None, None
        self.scroll, self.stats = None, None
        self.root, self.bot = None, None

        self.__dict__ = {**self.__dict__, **kwargs}

        if not hasattr(self, 'name'):
            self.name = self.id
        if not hasattr(self, 'description'):
            self.description = '\u200b'

    def arg_parser(self, ktx, hargs: Iterable, text:Iterable=None) -> Union[Tuple[list, dict], None]:
        '''
        Transforms a iterable of user args into specific args, kwargs, based
        of function parameters and typing

        If provides 
        
        Parameters:
            ktx : Default context class from kommando.py
            hargs: A iterable containing the human-readable args
            text: Optional, a iterable that is exausted by hargs iterable,
                  if not provided, some SpecialTypes cannot be used, like
                  Unsplitted

        Returns:
            A tuple containing a list(args) and a dict(kwargs), or None
        '''

        if hasattr(self.bot, 'dictionary'): # If the translation extension is loaded
            self.translate(ktx.language) # Translates the template

        nms = {'hargs': hargs, 'text': text,
               'args': [], 'kwargs': {},
               'pars': _parameters(self.function)}

        def verify(ktx, ann):
            if isinstance(ann, SpecialType):
                return ann(ktx, nms)
            else:
                return ann(next(nms['hargs']))
                
        def iterable(x):
            try:
                iter(x)
                return True
            except TypeError:
                return False

        def parse(kind, ann):
            '''
            Try to convert a annotation from a parameter kind
            using the following logic:

            1. See if kind is *args like
            2. If not, try to convert in the following order
               - Annotation is callable
               - Annotation is iterable
               - The type of Annotation is callable
               - Unknown (returns without conversion)
            3. Else, exaust the hargs iterable on a list,
               if the annotation is not None, try to
               convert it (only callable here)
            '''
            if kind != 2: # not VAR_POSITIONAL
                if ann is None:
                    return next(nms['hargs'])
                elif callable(ann):
                    return verify(ktx, ann)
                elif iterable(ann):
                    ann = iter(ann)
                    for a in ann:
                        try:
                            return verify(ktx, a)
                        except ValueError:
                            pass
                    raise ValueError
                elif callable(type(ann)):
                    return verify(ktx, type(ann))
                else:
                    ktx.logger.warning(f'Strange annotation: {ann}')
                    return v
            else:
                l = list(nms['hargs'])
                if l:
                    return [verify(ktx, x) for x in ann] if ann else l
                else:
                    raise ValueError

        for k, v in nms['pars']:
            try:
                kind = v.kind 
                ann = v.annotation if v.annotation is not v.empty else None
                if kind == 1: # POSITIONAL_OR_KEYWORD
                    if v.default is v.empty: # POSITIONAL
                        nms['args'].append(parse(kind, ann))
                    else: # KEYWORD
                        nms['kwargs'][k] = parse(kind, ann)
                elif kind == 2: # VAR_POSITIONAL
                    nms['args'].extend(parse(kind, ann))
                elif kind == 3: # KEYWORD_ONLY
                    nms['kwargs'][k] = parse(kind, ann)
                elif kind == 4: # VAR_KEYWORD
                    pass
            except ValueError: # Wrong type
                return None
            except StopIteration: # Few hargs
                if kind > 2: # KEYWORD_ONLY or VAR_KEYWORD
                    return None

        for k, v in nms['pars']: # Fill the empty keywords
            if k not in nms['kwargs']: #  No way to v.default be v.empty here
                nms['kwargs'][k] = v.default

        try:
            next(nms['hargs'])
            return None # Too much hargs
        except StopIteration:
            return nms['args'], nms['kwargs'] # Success

    def translate(self, language:str):
        '''Translates the invocation
        based of a key (language) of
        bot.dictionary

        Only works when translation 
        extension is loaded
        '''
        def parse(k, v):
            if type(v) == str:
                return k, v
            elif type(v) in (tuple, list):
                return k, random.choice(v)
            elif type(v) is dict:
                for x in self.bot.emotional_state:
                    if x in v:
                        return parse(k, v[x])
        try:
            data = self.bot.dictionary[language]
            data = data['specific'][self.scroll][self.id]
            data = filter(lambda t: t[0].startswith('__') and t[0].endswith('__'),
                            data.items())
            data = filter(lambda x: x, map(parse, data))
            for k, v in data:
                setattr(self, k, v)
        except KeyError:
            pass

class Container(Common):
    def __init__(self, **kwargs):
        self.sub_invocations = {}
        self.color = None
        self.root = None
        super().__init__(**kwargs)

        self.field = {'name': self.name, 
                      'value': ', '.join([f"**`{x}`**" for x 
                                          in self.sub_invocations.keys()]),
                      'inline': False}

    def __getitem__(self, k):
        return self.sub_invocations[k]

    def __setitem__(self, k, v):
        self.sub_invocations[k] = v

    def __delitem__(self, k):
        del self.sub_invocations[k]

    def __contains__(self, k):
        return k in self.sub_invocations

    def __len__(self):
        i = 0
        for v in self.sub_invocations.values():
            if hasattr(v, '__len__'):
                i += len(v)
            else:
                i += 1
        return i

    async def __check__(self, ktx):
        for v in self.sub_invocations.values():
            invocation = await asyncio.coroutine(v.__check__)(ktx)
            if invocation:
                return invocation

    @lru_cache()
    def usage(self, language):
        if not hasattr(self.bot, 'color'):
            self.bot.color = 0xAE3333
        embed = discord.Embed(description=self.description, 
                              color=self.color or self.bot.color)
        embed.set_author(name=self.name, 
                         icon_url=self.bot.client.user.avatar_url)
        for _, v in self.sub_invocations.items():
            if hasattr(v, 'field'):
                embed.add_field(**v.field)
        return embed

class Group(Container):
    @lru_cache()
    def usage(self, language):
        if not hasattr(self.bot, 'color'):
            self.bot.color = 0xAE3333
        embed = discord.Embed(description=self.description, 
                              color=self.color or self.bot.color)
        embed.set_author(name=self.name, 
                         icon_url=self.bot.user.avatar_url)
        for _, v in self.sub_invocations.items():
            if hasattr(v, 'field'):
                kwargs = v.field
                kwargs['name'] = f'{self.id} {kwargs["name"]}'
                embed.add_field(**kwargs)
        return embed

    async def __argf__(self, ktx):
        try:
            splitted, _ = _common_split(ktx.message.content)
            content = ktx.message.content
            ktx.message.content = content[content.index(next(splitted)):]
            next(splitted) 
            check = map(lambda v: v.__check__(ktx), 
                        self.sub_invocations.values())
            check = filter(lambda x: x, check)
            ktx.invocation = next(check)
            return await ktx.invoke()
        except StopIteration:
            if hasattr(self, 'usage'):
                await ktx.send(embed=self.usage(ktx.language))
    
    async def __check__(self, ktx):
        g, _ = _common_split(ktx.message.content)
        if next(g, None) == self.name:
            f = asyncio.coroutine(self.function)
            try:
                content = ktx.message.content
                ktx.message.content = content[content.index(next(g)):]
                command = await asyncio.coroutine(super().__check__)(ktx)
                await f(ktx, command)
                return command
            except StopIteration:
                await f(ktx, None)
                return self
    
class Command(Common):
    def __init__(self, **kwargs):
        self.color = None
        super().__init__(**kwargs)

        # Usage field
        pars = _parameters(self.function)
        args = ''.join([f' ({v.name}) ' if v.default is v.empty 
                        else f' [{v.name}]' for _, v in pars
                        if not v.name.startswith('_')])
        self.field =  {'name': self.name + args, 'value': self.description,
                       'inline': False}

    async def __argf__(self, ktx):
        hargs, text = _common_split(ktx.message.content)
        next(hargs)
        result = self.arg_parser(ktx, hargs, text=text)
        if result:
            return result[0], result[1]
        else:
            if hasattr(self, 'usage'):
                await ktx.send(embed=self.usage(ktx.language))

    def __check__(self, ktx):
        if next(_common_split(ktx.message.content)[0], None) == self.name:
            return self
        
    @lru_cache()
    def usage(self, language):
        if not hasattr(self.bot, 'color'):
            self.bot.color = 0xAE3333
        embed = discord.Embed(title=self.field['name'], 
                              description=self.field['value'], 
                              color=self.color or self.bot.color)
        return embed

class Summon(Common):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not hasattr(self, 'regex'):
            self.regex = None

    def __argf__(self, ktx):
        groups = re.match(self.regex, ktx.message.content).groupdict()
        pars = _parameters(self.function)
        return self.arg_parser(ktx, map(lambda x: groups[x[0]], pars))

    def __check__(self, ktx):
        if not self.regex:
            ktx.logger.error(f"Invocation without regex!")
            return False
        if re.match(self.regex, ktx.message.content):
            return self

class Subliminal(Common):
    def __init__(self, **kwargs):
        self.arg_regex = re.compile(r'\*([ A-z0-9]*)\*')
        super().__init__(**kwargs)

    def __argf__(self, ktx):
        hargs = (x[1] for x in self.arg_regex.finditer(ktx.message.content))
        next(hargs, None)
        return self.arg_parser(ktx, hargs)

    def __check__(self, ktx):
        try:
            x = next(self.arg_regex.finditer(ktx.message.content))
            if x == self.name:
                return self
        except StopIteration:
            pass
