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

def literal(mention):
    def _summoning_check(message, mention=mention):
        if '<@!' in mention:
            mention2 = mention.replace('<@!', '<@')
        else:
            mention2 = mention.replace('<@', '<@!')
        content = message.content
        if mention in content or mention2 in content:
            if mention in message.content:
                message.content = content.replace(mention, '', 1)
            else:
                message.content = content.replace(mention2, '', 1)
            return message
        return _summoning_check

def prefix(prefix):
    def _summoning_check(message, prefix=prefix):
        if message.content.startswith(prefix):
            message.content = message.content[len(prefix):]
            return message
    return _summoning_check
