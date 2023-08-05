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

import os
import sys
import time
import asyncio
import difflib
import discord
import inspect
import logging
import importlib
import traceback

from copy import deepcopy
from functools import wraps, lru_cache, partial

# Context and helper class

class Kontext:
    def __init__(self, bot, message):
        self.bot = bot

        self.message = message
        self.author = message.author
        self.channel = message.channel
        self.guild = message.guild

        self.extension = None
        self.section = None
        self.invocation = None
        self.log = bot.log

    def load(self, invocation):
        """
        Loads the invocation and the extension
        This function exists for
        possible extensions
        """
        self.invocation = invocation
        self.extension = invocation.extension
        self.section = invocation.section

    async def fit(self, invocations):    
        """
        Iterates over all invocations to find 
        whose fits the ctx, using __check__
        __check__ needs to return a Class or a false value

        Returns a invocation, or None
        """
        for v in invocations.values():
            invocation = await asyncio.coroutine(v.__check__)(self)
            if invocation:
                self.load(invocation)
                return True
        return False

    async def invoke(self):
        """
        Takes the context with the invocation instance,
        and try to get the args from __argf__
        If succeed, run the invocation function
        """
        try:
            f = self.invocation.__argf__
            result = await asyncio.coroutine(f)(self)
            if result is not None:
                f = asyncio.coroutine(self.invocation.function)
                return await f(self, *result[0], **result[1])
        except Exception as e:
            self.log.exception('Error on invocation')
            raise e

    async def send(self, *args, **kwargs):
        """
        Its just a alias of channel.send,
        exists for extensions
        """
        return await self.channel.send(*args, **kwargs)

def EnhancedBot(parent, name='EnhancedBot'):
    return type(name, (parent,), dict(Bot.__dict__))

class Bot:
    def initialize(self, log_name='Kommando.py'):
        self.Kontext = deepcopy(Kontext)
        
        # Log definition
        self.log = logging.getLogger(type(self).__name__)
        self.log.setLevel(logging.DEBUG)

        self.summoning = lambda _: None
        self.invocations = {}

    def kontext(self, message):
        return self.Kontext(self, message)
        
    # Invocation decorator

    def invocation(self, template, **kwargs):
        """
        Decorator for creating invocations, 
        uses a function and a Template class

        Kwargs are used as invocation Class
        variables, a custom __installation__
        can be defined on Template
        """
        def decorator(f):
            @wraps(f)
            async def decorated(ctx, *args, **kwargs):
                return await f(ctx, *args, **kwargs)
            section = inspect.getframeinfo(inspect.currentframe().f_back).function
            defaults = {'id': f.__name__, 'function': decorated, 
                        'extension': decorated.__module__, 'stats': {},
                        'section': section, 'bot': self}
            invocation = template(**{**defaults, **kwargs})
            if hasattr(invocation, '__install__'):
                invocation.__install__()
            else:
                self.invocations[invocation.id] = invocation
            return decorated
        return decorator

    # Parse functions

    async def parse_message(self, message):
        """
        Takes the message and try to see if
        its context fit to an invocation

        If fits, the invocation is called
        """

        if message.author.bot:
            return False

        kmessage = await asyncio.coroutine(self.summoning)(message)
        if kmessage:
            ctx = self.kontext(message)
            if await ctx.fit(self.invocations):
                return await ctx.invoke()

        if hasattr(self, 'process_commands'):
            await self.process_commands(message)
