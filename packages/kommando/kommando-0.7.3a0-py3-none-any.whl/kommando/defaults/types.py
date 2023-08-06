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
import dill
import pickle

def hellvar(_, data):
    try:
        return dill.loads(bytearray.fromhex(data))
    except pickle.UnpicklingError:
        raise ValueError

def mention(name, regex, strf):
    regex = re.compile(regex)
    def matcher(ktx, data):
        try:
            return eval(strf)(int(data))
        except ValueError:
            match = re.match(regex, data)
            if match:
                return eval(strf)(int(match.group('id')))
            else:
                raise ValueError
    matcher.__name__ = name
    return matcher

user = mention('user', r'<@(!|)(?P<id>[0-9]*)>', 'ktx.bot.get_user')
member = mention('member', r'<@(!|)(?P<id>[0-9]*)>', 'ktx.guild.get_member')
channel = mention('channel', r'<@(!|)(?P<id>[0-9]*)>', 'ktx.guild.get_channel')
role = mention('role', r'<@&(?P<id>[0-9]*)>', 'ktx.guild.get_role')
emoji = mention('emoji', r'<:[^\s]+:(?P<id>[0-9]*)>', 'ktx.bot.get_emoji')

def unsplitted(ktx, hargs):
    orig = ktx.message.content
    rev = orig[::-1]
    for x in hargs[::-1]:
        try:
            rev = rev[rev.index(x[::-1]) + len(x):]
        except ValueError:
            break
    rev = rev[::-1]
    return [orig[orig.index(rev) + len(rev):]]
