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

import uuid
import time
import random
import asyncio

from functools import wraps, partial

def concurrency(level=3):
    def decorator(f):
        @wraps(f)
        async def decorated(ktx, *args, **kwargs):
            stats = ktx.invocation.stats
            ktx.invocation.concurrency = (level)
            if 'instances' not in stats:
                stats['instances'] = []
            if ktx.guild is None:
                ktx.guild = ktx.channel
            ids = [0, ktx.guild.id, ktx.channel.id,
                   ktx.author.id]
            instances = stats['instances']
            req_id = ids[level]
            if req_id not in instances:
                instances.append(req_id)
                try:
                    return await f(ktx, *args, **kwargs)
                except Exception as err:
                    raise err
                finally:
                    del instances[instances.index(req_id)]
            await ktx.send_response('concurrency')
        return decorated
    return decorator

def cooldown(seconds=5, level=3):
    def decorator(f):
        @wraps(f)
        async def decorated(ktx, *args, **kwargs):
            stats = ktx.invocation.stats
            ktx.invocation.cooldown = (seconds, level)
            if 'cooldowns' not in stats:
                stats['cooldowns'] = {}
            c = stats['cooldowns']
            if ktx.guild is None:
                ktx.guild = ktx.channel
            ids = [0, ktx.guild.id, ktx.channel.id,
                   ktx.author.id]
            req_id = ids[level]
            if req_id in c:
                cold = time.time() - c[req_id] > seconds
            else:
                cold = True
            if cold:
                c[req_id] = time.time()
                return await f(ktx, *args, **kwargs)
            else:
                await ktx.send_response('cooldown')
        return decorated
    return decorator

def use_limit(uses, seconds=60, level=3):
    def decorator(f):
        @wraps(f)
        async def decorated(ktx, *args, **kwargs):
            stats = ktx.invocation.stats
            ktx.invocation.use_limit = (uses, seconds, level)
            if 'use_limit' not in stats:
                stats['use_limit'] = {}
            c = stats['use_limit']
            if ktx.guild is None:
                ktx.guild = ktx.channel
            ids = [0, ktx.guild.id, ktx.channel.id,
                   ktx.author.id]
            req_id = ids[level]
            if req_id in c:
                u_uses, at_time = c[req_id]
                cold = time.time() - at_time > seconds
            else:
                u_uses, at_time = (0, time.time())
                cold = True
            if u_uses < uses:
                c[req_id] = (u_uses + 1, at_time)
            elif cold:
                c[req_id] = (0, time.time())
            else:
                await ktx.send_response('use-limit')
                return
            return await f(ktx, *args, **kwargs)
        return decorated
    return decorator

def tester(check, response='tester'):
    def decorator(f):
        @wraps(f)
        async def decorated(ktx, *args, **kwargs):
            if await asyncio.coroutine(check)(ktx):
                return await f(ktx, *args, **kwargs)
            else:
                await ktx.send_response(response)
        return decorated
    return decorator

def evaluator(source, response='evaluator'):
    def decorator(f):
        @wraps(f)
        async def decorated(ktx, *args, **kwargs):
            if eval(source):
                return await f(ktx, *args, **kwargs)
            else:
                await ktx.send_response(response)
        return decorated
    return decorator

def randomize(percentage=100, response='randomize'):
    return partial(tester, random.randint(0, 100) >= percentage, response=response)

def need_files(fmin=1, fmax=10):
    def decorator(f):
        @wraps(f)
        async def decorated(ktx, *args, **kwargs):
            if fmin < len(ktx.message.attachments) > fmax:
                return await f(ktx, *args, **kwargs)
            else:
                await ktx.send_response('need-files')
        return decorated
    return decorator

def need_channel(name):
    def decorator(f):
        @wraps(f)
        async def decorated(ktx, *args, **kwargs):
            channel = None
            for x in ktx.message.guild.channels:
                if x.name == name:
                    channel = x
            if channel is not None:
                return await f(ktx, *args, **kwargs)
            else:
                await ktx.send_response('need-channel', name)
        return decorated
    return decorator

def need_perms(perms):
    def decorator(f):
        @wraps(f)
        async def decorated(ktx, *args, **kwargs):
            p = []
            for role in ktx.author.roles:
                p.extend(role.permissions)
            p = set([x[0] for x in p if x[1]])
            if all([x in p for x in perms]):
                return await f(ktx, *args, **kwargs)
            else:
                await ktx.send_response('need-perms')

        return decorated

    return decorator

def need_role(name):
    def decorator(f):
        @wraps(f)
        async def decorated(ktx, *args, **kwargs):
            for role in ktx.author.roles:
                if str(role) == name:
                    return await f(ktx, *args, **kwargs)
            await ktx.send_response('need-role', name)
        return decorated
    return decorator

owner_only = evaluator("ktx.author.id == int(ktx.bot.owner_id)",
                       response='owner-only')

dm_only = evaluator("isinstance(ktx.channel, discord.DMChannel)",
                    response='dm-only')

guild_only = evaluator("if not isinstance(ktx.channel, discord.DMChannel)",
                       response='guild-only')

nsfw_only = evaluator('ktx.message.channel.is_nsfw()',
                      response='nsfw-only')

safe_only = evaluator('not ktx.message.channel.is_nsfw()',
                      response='safe-only')
