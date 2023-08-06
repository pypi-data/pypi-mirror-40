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

import discord

from math import ceil
from io import IOBase, BytesIO
from typing import List, Tuple

MAX_CHUNK_SIZE = 8 * (1000 ** 2)

class DiscordFile(IOBase):
    def __init__(self, filename: str,
                 channel: discord.abc.Messageable, 
                 chunks: List[discord.Message]):

        self.filename = filename
        self.channel = channel
        self.chunks = chunks

        self.size = sum(self.sizes)
        self.cache = [b'' for _ in range(len(self.chunks))]
        self.fp = 0

    @property
    def sizes(self):
        return [x.attachments[0].size for x in self.chunks]

    @property
    def seekable(self):
        return True

    def seek(self, offset, whence=0):
        if whence == 0:
            self.fp = offset
        elif whence == 1:
            self.fp += offset
        elif whence == 2:
            self.fp = self.size + offset

    def tell(self):
        return self.fp

    def _get_parts(self, fp: int, size: int) -> Tuple[int]:
        """
        Uses the actual fp index and a size
        to determine how many parts it will
        need and where is the offset
        """
        i, ac = 0, 0
        ps, pe = None, None
        start, end = fp, fp + size

        sizes = self.sizes

        while not (ps and pe):
            if len(sizes) == 0:
                sizes += [size]
            ac += sizes[0]
            if ac > start:
                ps = i
            if ac > end:
                pe = i
            i += 1
            del sizes[0]
        parts, offset = (pe - ps) + 1, ps - 1
        return parts, offset

    async def _cache_parts(self, parts:int, offset:int) -> None:
        """Cache the needed parts for the operation"""
        for i in range(parts):
            i += offset
            try:
                if not self.cache[i]:
                    out = BytesIO()
                    attch = self.chunks[i].attachments[0]
                    await attch.save(out, seek_begin=False)
                    self.cache[i] = out.getvalue()
            except IndexError:
                break

    def readable(self):
        return True

    async def _read(self, size=-1) -> bytes:
        """
        Reading without the seek in the end

        Necessary for self.write
        """
        if self.chunks:
            if size < 0:
                size = self.size - size + 1
            fp = self.tell()
            parts, offset = self._get_parts(fp, size)
            start, end = offset, parts + offset
            end = -1 if end > len(self.cache) else end
            await self._cache_parts(parts, offset)
            return b''.join(self.cache[start:end])
        else:
            return b''

    async def read(self, size=-1) -> bytes:
        """Reads the discord file"""
        out = await self._read(size=size)
        self.seek(self.tell() + size)
        return out

    async def write(self, b: bytes) -> None:
        """Writes to a discord file"""
        fp = self.tell()
        bsize = len(b)

        if bsize > MAX_CHUNK_SIZE:
            while b:
                await self.write(b[:MAX_CHUNK_SIZE])
                b = b[MAX_CHUNK_SIZE:]
            return None

        parts, offset = self._get_parts(fp, bsize)
        print(fp, bsize, parts, offset)
        await self._cache_parts(parts, offset)

        end = parts + offset
        if len(self.cache) <= end:
            diff = end - len(self.cache)
            fill = [b'' for x in range(diff)]
            self.cache.extend(fill)

        for i in range(parts):
            i += offset
            arr = self.cache[i]
            sizes = self.sizes

            try:
                psize = sizes[i]
                start = fp - sum(sizes[:i])
                end = psize if bsize > psize else bsize
            except IndexError:
                start = 0
                end = bsize

            splitted = list(arr)
            splitted[start:end] = list(b[start:end])
            data = bytes(splitted)

            self.cache[i] = data
            f = discord.File(BytesIO(data), 
                             filename=self.filename.format(i=i))
            msg = await self.channel.send(file=f)
            if len(self.chunks) <= i:
                self.chunks.append(msg)
            else:
                await self.chunks[i].delete()
                self.chunks[i] = msg
            b = b[end:]
        self.size = bsize + fp
        self.seek(self.size)

    def writeable(self):
        return True

async def dfile(self, filename:str, **search_kwargs):
    """ 
    Helper function for find the file
    You can store the ids on a database and 
    make your own open function
    """
    splitted = filename.rsplit('.', 1)
    if len(splitted) == 2:
        name, ext = splitted
    else:
        name, ext = splitted, 'data'
    filename = f'BEATRICE_{name}_part{{i}}.{ext}'
    chunks = []
    async for x in self.history(**search_kwargs):
        if x.attachments:
            x_name = x.attachments[0].filename
            starts = x_name.startswith(f'BEATRICE_{name}')
            ends = x_name.endswith(f'.{ext}')
            if starts and ends:
                chunks.append(x)
    f = DiscordFile(filename, self, chunks)
    return f
