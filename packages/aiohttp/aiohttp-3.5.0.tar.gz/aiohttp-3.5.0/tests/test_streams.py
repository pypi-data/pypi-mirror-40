"""Tests for streams.py"""

import asyncio
import re
from unittest import mock

import pytest

from aiohttp import streams


DATA = b'line1\nline2\nline3\n'


def chunkify(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i+n]


async def create_stream():
    loop = asyncio.get_event_loop()
    protocol = mock.Mock(_reading_paused=False)
    stream = streams.StreamReader(protocol, loop=loop)
    stream.feed_data(DATA)
    stream.feed_eof()
    return stream


@pytest.fixture
def protocol():
    return mock.Mock(_reading_paused=False)


class TestStreamReader:

    DATA = b'line1\nline2\nline3\n'

    def _make_one(self, *args, **kwargs):
        return streams.StreamReader(mock.Mock(_reading_paused=False),
                                    *args, **kwargs)

    async def test_create_waiter(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one(loop=loop)
        stream._waiter = loop.create_future
        with pytest.raises(RuntimeError):
            await stream._wait('test')

    def test_ctor_global_loop(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        stream = streams.StreamReader(mock.Mock(_reading_paused=False))

        assert stream._loop is loop

    async def test_at_eof(self) -> None:
        stream = self._make_one()
        assert not stream.at_eof()

        stream.feed_data(b'some data\n')
        assert not stream.at_eof()

        await stream.readline()
        assert not stream.at_eof()

        stream.feed_data(b'some data\n')
        stream.feed_eof()
        await stream.readline()
        assert stream.at_eof()

    async def test_wait_eof(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one()
        wait_task = loop.create_task(stream.wait_eof())

        async def cb():
            await asyncio.sleep(0.1)
            stream.feed_eof()

        loop.create_task(cb())
        await wait_task
        assert stream.is_eof()
        assert stream._eof_waiter is None

    async def test_wait_eof_eof(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one()
        stream.feed_eof()

        wait_task = loop.create_task(stream.wait_eof())
        await wait_task
        assert stream.is_eof()

    async def test_feed_empty_data(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'')
        stream.feed_eof()

        data = await stream.read()
        assert b'' == data

    async def test_feed_nonempty_data(self) -> None:
        stream = self._make_one()
        stream.feed_data(self.DATA)
        stream.feed_eof()

        data = await stream.read()
        assert self.DATA == data

    async def test_read_zero(self) -> None:
        # Read zero bytes.
        stream = self._make_one()
        stream.feed_data(self.DATA)

        data = await stream.read(0)
        assert b'' == data

        stream.feed_eof()
        data = await stream.read()
        assert self.DATA == data

    async def test_read(self) -> None:
        loop = asyncio.get_event_loop()
        # Read bytes.
        stream = self._make_one()
        read_task = loop.create_task(stream.read(30))

        def cb():
            stream.feed_data(self.DATA)
        loop.call_soon(cb)

        data = await read_task
        assert self.DATA == data

        stream.feed_eof()
        data = await stream.read()
        assert b'' == data

    async def test_read_line_breaks(self) -> None:
        # Read bytes without line breaks.
        stream = self._make_one()
        stream.feed_data(b'line1')
        stream.feed_data(b'line2')

        data = await stream.read(5)
        assert b'line1' == data

        data = await stream.read(5)
        assert b'line2' == data

    async def test_read_all(self) -> None:
        # Read all available buffered bytes
        stream = self._make_one()
        stream.feed_data(b'line1')
        stream.feed_data(b'line2')
        stream.feed_eof()

        data = await stream.read()
        assert b'line1line2' == data

    async def test_read_up_to(self) -> None:
        # Read available buffered bytes up to requested amount
        stream = self._make_one()
        stream.feed_data(b'line1')
        stream.feed_data(b'line2')

        data = await stream.read(8)
        assert b'line1lin' == data

        data = await stream.read(8)
        assert b'e2' == data

    async def test_read_eof(self) -> None:
        loop = asyncio.get_event_loop()
        # Read bytes, stop at eof.
        stream = self._make_one()
        read_task = loop.create_task(stream.read(1024))

        def cb():
            stream.feed_eof()
        loop.call_soon(cb)

        data = await read_task
        assert b'' == data

        data = await stream.read()
        assert data == b''

    async def test_read_eof_infinite(self) -> None:
        # Read bytes.
        stream = self._make_one()
        stream.feed_eof()

        with mock.patch('aiohttp.streams.internal_logger') as internal_logger:
            await stream.read()
            await stream.read()
            await stream.read()
            await stream.read()
            await stream.read()
            await stream.read()
        assert internal_logger.warning.called

    async def test_read_eof_unread_data_no_warning(self) -> None:
        # Read bytes.
        stream = self._make_one()
        stream.feed_eof()

        with mock.patch('aiohttp.streams.internal_logger') as internal_logger:
            await stream.read()
            await stream.read()
            await stream.read()
            await stream.read()
            await stream.read()
        with pytest.warns(DeprecationWarning):
            stream.unread_data(b'data')
        await stream.read()
        await stream.read()
        assert not internal_logger.warning.called

    async def test_read_until_eof(self) -> None:
        loop = asyncio.get_event_loop()
        # Read all bytes until eof.
        stream = self._make_one()
        read_task = loop.create_task(stream.read(-1))

        def cb():
            stream.feed_data(b'chunk1\n')
            stream.feed_data(b'chunk2')
            stream.feed_eof()
        loop.call_soon(cb)

        data = await read_task
        assert b'chunk1\nchunk2' == data

        data = await stream.read()
        assert b'' == data

    async def test_read_exception(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'line\n')

        data = await stream.read(2)
        assert b'li' == data

        stream.set_exception(ValueError())
        with pytest.raises(ValueError):
            await stream.read(2)

    async def test_readline(self) -> None:
        loop = asyncio.get_event_loop()
        # Read one line. 'readline' will need to wait for the data
        # to come from 'cb'
        stream = self._make_one()
        stream.feed_data(b'chunk1 ')
        read_task = loop.create_task(stream.readline())

        def cb():
            stream.feed_data(b'chunk2 ')
            stream.feed_data(b'chunk3 ')
            stream.feed_data(b'\n chunk4')
        loop.call_soon(cb)

        line = await read_task
        assert b'chunk1 chunk2 chunk3 \n' == line

        stream.feed_eof()
        data = await stream.read()
        assert b' chunk4' == data

    async def test_readline_limit_with_existing_data(self) -> None:
        # Read one line. The data is in StreamReader's buffer
        # before the event loop is run.

        stream = self._make_one(limit=2)
        stream.feed_data(b'li')
        stream.feed_data(b'ne1\nline2\n')

        with pytest.raises(ValueError):
            await stream.readline()
        # The buffer should contain the remaining data after exception
        stream.feed_eof()
        data = await stream.read()
        assert b'line2\n' == data

    async def test_readline_limit(self) -> None:
        loop = asyncio.get_event_loop()
        # Read one line. StreamReaders are fed with data after
        # their 'readline' methods are called.
        stream = self._make_one(limit=4)

        def cb():
            stream.feed_data(b'chunk1')
            stream.feed_data(b'chunk2\n')
            stream.feed_data(b'chunk3\n')
            stream.feed_eof()
        loop.call_soon(cb)

        with pytest.raises(ValueError):
            await stream.readline()
        data = await stream.read()
        assert b'chunk3\n' == data

    async def test_readline_nolimit_nowait(self) -> None:
        # All needed data for the first 'readline' call will be
        # in the buffer.
        stream = self._make_one()
        stream.feed_data(self.DATA[:6])
        stream.feed_data(self.DATA[6:])

        line = await stream.readline()
        assert b'line1\n' == line

        stream.feed_eof()
        data = await stream.read()
        assert b'line2\nline3\n' == data

    async def test_readline_eof(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'some data')
        stream.feed_eof()

        line = await stream.readline()
        assert b'some data' == line

    async def test_readline_empty_eof(self) -> None:
        stream = self._make_one()
        stream.feed_eof()

        line = await stream.readline()
        assert b'' == line

    async def test_readline_read_byte_count(self) -> None:
        stream = self._make_one()
        stream.feed_data(self.DATA)

        await stream.readline()

        data = await stream.read(7)
        assert b'line2\nl' == data

        stream.feed_eof()
        data = await stream.read()
        assert b'ine3\n' == data

    async def test_readline_exception(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'line\n')

        data = await stream.readline()
        assert b'line\n' == data

        stream.set_exception(ValueError())
        with pytest.raises(ValueError):
            await stream.readline()

    async def test_readexactly_zero_or_less(self) -> None:
        # Read exact number of bytes (zero or less).
        stream = self._make_one()
        stream.feed_data(self.DATA)

        data = await stream.readexactly(0)
        assert b'' == data
        stream.feed_eof()
        data = await stream.read()
        assert self.DATA == data

        stream = self._make_one()
        stream.feed_data(self.DATA)

        data = await stream.readexactly(-1)
        assert b'' == data
        stream.feed_eof()
        data = await stream.read()
        assert self.DATA == data

    async def test_readexactly(self) -> None:
        loop = asyncio.get_event_loop()
        # Read exact number of bytes.
        stream = self._make_one()

        n = 2 * len(self.DATA)
        read_task = loop.create_task(stream.readexactly(n))

        def cb():
            stream.feed_data(self.DATA)
            stream.feed_data(self.DATA)
            stream.feed_data(self.DATA)
        loop.call_soon(cb)

        data = await read_task
        assert self.DATA + self.DATA == data

        stream.feed_eof()
        data = await stream.read()
        assert self.DATA == data

    async def test_readexactly_eof(self) -> None:
        loop = asyncio.get_event_loop()
        # Read exact number of bytes (eof).
        stream = self._make_one(loop=loop)
        n = 2 * len(self.DATA)
        read_task = loop.create_task(stream.readexactly(n))

        def cb():
            stream.feed_data(self.DATA)
            stream.feed_eof()
        loop.call_soon(cb)

        with pytest.raises(asyncio.IncompleteReadError) as cm:
            await read_task
        assert cm.value.partial == self.DATA
        assert cm.value.expected == n
        assert (str(cm.value) ==
                '18 bytes read on a total of 36 expected bytes')
        data = await stream.read()
        assert b'' == data

    async def test_readexactly_exception(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'line\n')

        data = await stream.readexactly(2)
        assert b'li' == data

        stream.set_exception(ValueError())
        with pytest.raises(ValueError):
            await stream.readexactly(2)

    async def test_unread_data(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'line1')
        stream.feed_data(b'line2')
        stream.feed_data(b'onemoreline')

        data = await stream.read(5)
        assert b'line1' == data

        with pytest.warns(DeprecationWarning):
            stream.unread_data(data)

        data = await stream.read(5)
        assert b'line1' == data

        data = await stream.read(4)
        assert b'line' == data

        with pytest.warns(DeprecationWarning):
            stream.unread_data(b'line1line')

        data = b''
        while len(data) < 10:
            data += await stream.read(10)
        assert b'line1line2' == data

        data = await stream.read(7)
        assert b'onemore' == data

        with pytest.warns(DeprecationWarning):
            stream.unread_data(data)

        data = b''
        while len(data) < 11:
            data += await stream.read(11)
        assert b'onemoreline' == data

        with pytest.warns(DeprecationWarning):
            stream.unread_data(b'line')
        data = await stream.read(4)
        assert b'line' == data

        stream.feed_eof()
        with pytest.warns(DeprecationWarning):
            stream.unread_data(b'at_eof')
        data = await stream.read(6)
        assert b'at_eof' == data

    async def test_exception(self) -> None:
        stream = self._make_one()
        assert stream.exception() is None

        exc = ValueError()
        stream.set_exception(exc)
        assert stream.exception() is exc

    async def test_exception_waiter(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one()

        async def set_err():
            stream.set_exception(ValueError())

        t1 = loop.create_task(stream.readline())
        t2 = loop.create_task(set_err())

        await asyncio.wait([t1, t2])
        with pytest.raises(ValueError):
            t1.result()

    async def test_exception_cancel(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one()

        async def read_a_line():
            await stream.readline()

        t = loop.create_task(read_a_line())
        await asyncio.sleep(0)
        t.cancel()
        await asyncio.sleep(0)
        # The following line fails if set_exception() isn't careful.
        stream.set_exception(RuntimeError('message'))
        await asyncio.sleep(0)
        assert stream._waiter is None

    async def test_readany_eof(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one()
        read_task = loop.create_task(stream.readany())
        loop.call_soon(stream.feed_data, b'chunk1\n')

        data = await read_task
        assert b'chunk1\n' == data
        stream.feed_eof()
        data = await stream.read()
        assert b'' == data

    async def test_readany_empty_eof(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one()
        stream.feed_eof()
        read_task = loop.create_task(stream.readany())

        data = await read_task

        assert b'' == data

    async def test_readany_exception(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'line\n')

        data = await stream.readany()
        assert b'line\n' == data

        stream.set_exception(ValueError())
        with pytest.raises(ValueError):
            await stream.readany()

    async def test_read_nowait(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'line1\nline2\n')

        assert stream.read_nowait() == b'line1\nline2\n'
        assert stream.read_nowait() == b''
        stream.feed_eof()
        data = await stream.read()
        assert b'' == data

    async def test_read_nowait_n(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'line1\nline2\n')

        assert stream.read_nowait(4) == b'line'
        assert stream.read_nowait() == b'1\nline2\n'
        assert stream.read_nowait() == b''
        stream.feed_eof()
        data = await stream.read()
        assert b'' == data

    async def test_read_nowait_exception(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'line\n')
        stream.set_exception(ValueError())

        with pytest.raises(ValueError):
            stream.read_nowait()

    async def test_read_nowait_waiter(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one()
        stream.feed_data(b'line\n')
        stream._waiter = loop.create_future()

        with pytest.raises(RuntimeError):
            stream.read_nowait()

    async def test_readchunk(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one()

        def cb():
            stream.feed_data(b'chunk1')
            stream.feed_data(b'chunk2')
            stream.feed_eof()
        loop.call_soon(cb)

        data, end_of_chunk = await stream.readchunk()
        assert b'chunk1' == data
        assert not end_of_chunk

        data, end_of_chunk = await stream.readchunk()
        assert b'chunk2' == data
        assert not end_of_chunk

        data, end_of_chunk = await stream.readchunk()
        assert b'' == data
        assert not end_of_chunk

    async def test_readchunk_wait_eof(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one()

        async def cb():
            await asyncio.sleep(0.1)
            stream.feed_eof()

        loop.create_task(cb())
        data, end_of_chunk = await stream.readchunk()
        assert b"" == data
        assert not end_of_chunk
        assert stream.is_eof()

    async def test_begin_and_end_chunk_receiving(self) -> None:
        stream = self._make_one()

        stream.begin_http_chunk_receiving()
        stream.feed_data(b'part1')
        stream.feed_data(b'part2')
        stream.end_http_chunk_receiving()

        data, end_of_chunk = await stream.readchunk()
        assert b'part1part2' == data
        assert end_of_chunk

        stream.begin_http_chunk_receiving()
        stream.feed_data(b'part3')

        data, end_of_chunk = await stream.readchunk()
        assert b'part3' == data
        assert not end_of_chunk

        stream.end_http_chunk_receiving()

        data, end_of_chunk = await stream.readchunk()
        assert b'' == data
        assert end_of_chunk

        stream.feed_eof()

        data, end_of_chunk = await stream.readchunk()
        assert b'' == data
        assert not end_of_chunk

    async def test_end_chunk_receiving_without_begin(self) -> None:
        stream = self._make_one()
        with pytest.raises(RuntimeError):
            stream.end_http_chunk_receiving()

    async def test_readchunk_with_unread(self) -> None:
        """Test that stream.unread does not break controlled chunk receiving.
        """
        stream = self._make_one()

        # Send 2 chunks
        stream.begin_http_chunk_receiving()
        stream.feed_data(b'part1')
        stream.end_http_chunk_receiving()
        stream.begin_http_chunk_receiving()
        stream.feed_data(b'part2')
        stream.end_http_chunk_receiving()

        # Read only one chunk
        data, end_of_chunk = await stream.readchunk()

        # Try to unread a part of the first chunk
        with pytest.warns(DeprecationWarning):
            stream.unread_data(b'rt1')

        # The end_of_chunk signal was already received for the first chunk,
        # so we receive up to the second one
        data, end_of_chunk = await stream.readchunk()
        assert b'rt1part2' == data
        assert end_of_chunk

        # Unread a part of the second chunk
        with pytest.warns(DeprecationWarning):
            stream.unread_data(b'rt2')

        data, end_of_chunk = await stream.readchunk()
        assert b'rt2' == data
        # end_of_chunk was already received for this chunk
        assert not end_of_chunk

        stream.feed_eof()
        data, end_of_chunk = await stream.readchunk()
        assert b'' == data
        assert not end_of_chunk

    async def test_readchunk_with_other_read_calls(self) -> None:
        """Test that stream.readchunk works when other read calls are made on
        the stream.
        """
        stream = self._make_one()

        stream.begin_http_chunk_receiving()
        stream.feed_data(b'part1')
        stream.end_http_chunk_receiving()
        stream.begin_http_chunk_receiving()
        stream.feed_data(b'part2')
        stream.end_http_chunk_receiving()

        data = await stream.read(7)
        assert b'part1pa' == data

        data, end_of_chunk = await stream.readchunk()
        assert b'rt2' == data
        assert end_of_chunk

        stream.feed_eof()
        data, end_of_chunk = await stream.readchunk()
        assert b'' == data
        assert not end_of_chunk

    async def test_readchunk_separate_http_chunk_tail(self) -> None:
        """Test that stream.readchunk returns (b'', True) when end of
        http chunk received after body
        """
        loop = asyncio.get_event_loop()
        stream = self._make_one()

        stream.begin_http_chunk_receiving()
        stream.feed_data(b'part1')

        data, end_of_chunk = await stream.readchunk()
        assert b'part1' == data
        assert not end_of_chunk

        async def cb():
            await asyncio.sleep(0.1)
            stream.end_http_chunk_receiving()

        loop.create_task(cb())
        data, end_of_chunk = await stream.readchunk()
        assert b'' == data
        assert end_of_chunk

        stream.begin_http_chunk_receiving()
        stream.feed_data(b'part2')
        data, end_of_chunk = await stream.readchunk()
        assert b'part2' == data
        assert not end_of_chunk

        stream.end_http_chunk_receiving()
        stream.begin_http_chunk_receiving()
        stream.feed_data(b'part3')
        stream.end_http_chunk_receiving()

        data, end_of_chunk = await stream.readchunk()
        assert b'' == data
        assert end_of_chunk

        data, end_of_chunk = await stream.readchunk()
        assert b'part3' == data
        assert end_of_chunk

        stream.begin_http_chunk_receiving()
        stream.feed_data(b'part4')
        data, end_of_chunk = await stream.readchunk()
        assert b'part4' == data
        assert not end_of_chunk

        async def cb():
            await asyncio.sleep(0.1)
            stream.end_http_chunk_receiving()
            stream.feed_eof()

        loop.create_task(cb())
        data, end_of_chunk = await stream.readchunk()
        assert b'' == data
        assert end_of_chunk

        data, end_of_chunk = await stream.readchunk()
        assert b'' == data
        assert not end_of_chunk

    async def test___repr__(self) -> None:
        stream = self._make_one()
        assert "<StreamReader>" == repr(stream)

    async def test___repr__nondefault_limit(self) -> None:
        stream = self._make_one(limit=123)
        assert "<StreamReader low=123 high=246>" == repr(stream)

    async def test___repr__eof(self) -> None:
        stream = self._make_one()
        stream.feed_eof()
        assert "<StreamReader eof>" == repr(stream)

    async def test___repr__data(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'data')
        assert "<StreamReader 4 bytes>" == repr(stream)

    async def test___repr__exception(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one(loop=loop)
        exc = RuntimeError()
        stream.set_exception(exc)
        assert "<StreamReader e=RuntimeError()>" == repr(stream)

    async def test___repr__waiter(self) -> None:
        loop = asyncio.get_event_loop()
        stream = self._make_one()
        stream._waiter = loop.create_future()
        assert re.search(r"<StreamReader w=<Future pending[\S ]*>>",
                         repr(stream))
        stream._waiter.set_result(None)
        await stream._waiter
        stream._waiter = None
        assert "<StreamReader>" == repr(stream)

    async def test_unread_empty(self) -> None:
        stream = self._make_one()
        stream.feed_data(b'line1')
        stream.feed_eof()
        with pytest.warns(DeprecationWarning):
            stream.unread_data(b'')

        data = await stream.read(5)
        assert b'line1' == data
        assert stream.at_eof()


async def test_empty_stream_reader() -> None:
    s = streams.EmptyStreamReader()
    assert s.set_exception(ValueError()) is None
    assert s.exception() is None
    assert s.feed_eof() is None
    assert s.feed_data(b'data') is None
    assert s.at_eof()
    assert (await s.wait_eof()) is None
    assert await s.read() == b''
    assert await s.readline() == b''
    assert await s.readany() == b''
    assert await s.readchunk() == (b'', True)
    with pytest.raises(asyncio.IncompleteReadError):
        await s.readexactly(10)
    assert s.read_nowait() == b''


@pytest.fixture
async def buffer(loop):
    return streams.DataQueue(loop)


class TestDataQueue:

    def test_is_eof(self, buffer) -> None:
        assert not buffer.is_eof()
        buffer.feed_eof()
        assert buffer.is_eof()

    def test_at_eof(self, buffer) -> None:
        assert not buffer.at_eof()
        buffer.feed_eof()
        assert buffer.at_eof()
        buffer._buffer.append(object())
        assert not buffer.at_eof()

    def test_feed_data(self, buffer) -> None:
        item = object()
        buffer.feed_data(item, 1)
        assert [(item, 1)] == list(buffer._buffer)

    def test_feed_eof(self, buffer) -> None:
        buffer.feed_eof()
        assert buffer._eof

    async def test_read(self, buffer) -> None:
        loop = asyncio.get_event_loop()
        item = object()

        def cb():
            buffer.feed_data(item, 1)
        loop.call_soon(cb)

        data = await buffer.read()
        assert item is data

    async def test_read_eof(self, buffer) -> None:
        loop = asyncio.get_event_loop()

        def cb():
            buffer.feed_eof()
        loop.call_soon(cb)

        with pytest.raises(streams.EofStream):
            await buffer.read()

    async def test_read_cancelled(self, buffer) -> None:
        loop = asyncio.get_event_loop()
        read_task = loop.create_task(buffer.read())
        await asyncio.sleep(0)
        waiter = buffer._waiter
        assert asyncio.isfuture(waiter)

        read_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await read_task
        assert waiter.cancelled()
        assert buffer._waiter is None

        buffer.feed_data(b'test', 4)
        assert buffer._waiter is None

    async def test_read_until_eof(self, buffer) -> None:
        item = object()
        buffer.feed_data(item, 1)
        buffer.feed_eof()

        data = await buffer.read()
        assert data is item

        with pytest.raises(streams.EofStream):
            await buffer.read()

    async def test_read_exc(self, buffer) -> None:
        item = object()
        buffer.feed_data(item)
        buffer.set_exception(ValueError)

        data = await buffer.read()
        assert item is data

        with pytest.raises(ValueError):
            await buffer.read()

    async def test_read_exception(self, buffer) -> None:
        buffer.set_exception(ValueError())

        with pytest.raises(ValueError):
            await buffer.read()

    async def test_read_exception_with_data(self, buffer) -> None:
        val = object()
        buffer.feed_data(val, 1)
        buffer.set_exception(ValueError())

        assert val is (await buffer.read())
        with pytest.raises(ValueError):
            await buffer.read()

    async def test_read_exception_on_wait(self, buffer) -> None:
        loop = asyncio.get_event_loop()
        read_task = loop.create_task(buffer.read())
        await asyncio.sleep(0)
        assert asyncio.isfuture(buffer._waiter)

        buffer.feed_eof()
        buffer.set_exception(ValueError())

        with pytest.raises(ValueError):
            await read_task

    def test_exception(self, buffer) -> None:
        assert buffer.exception() is None

        exc = ValueError()
        buffer.set_exception(exc)
        assert buffer.exception() is exc

    async def test_exception_waiter(self, buffer) -> None:
        loop = asyncio.get_event_loop()

        async def set_err():
            buffer.set_exception(ValueError())

        t1 = loop.create_task(buffer.read())
        t2 = loop.create_task(set_err())

        await asyncio.wait([t1, t2])

        with pytest.raises(ValueError):
            t1.result()


async def test_feed_data_waiters(protocol) -> None:
    loop = asyncio.get_event_loop()
    reader = streams.StreamReader(protocol, loop=loop)
    waiter = reader._waiter = loop.create_future()
    eof_waiter = reader._eof_waiter = loop.create_future()

    reader.feed_data(b'1')
    assert list(reader._buffer) == [b'1']
    assert reader._size == 1
    assert reader.total_bytes == 1

    assert waiter.done()
    assert not eof_waiter.done()
    assert reader._waiter is None
    assert reader._eof_waiter is eof_waiter


async def test_feed_data_completed_waiters(protocol) -> None:
    loop = asyncio.get_event_loop()
    reader = streams.StreamReader(protocol, loop=loop)
    waiter = reader._waiter = loop.create_future()

    waiter.set_result(1)
    reader.feed_data(b'1')

    assert reader._waiter is None


async def test_feed_eof_waiters(protocol) -> None:
    loop = asyncio.get_event_loop()
    reader = streams.StreamReader(protocol, loop=loop)
    waiter = reader._waiter = loop.create_future()
    eof_waiter = reader._eof_waiter = loop.create_future()

    reader.feed_eof()
    assert reader._eof

    assert waiter.done()
    assert eof_waiter.done()
    assert reader._waiter is None
    assert reader._eof_waiter is None


async def test_feed_eof_cancelled(protocol) -> None:
    loop = asyncio.get_event_loop()
    reader = streams.StreamReader(protocol, loop=loop)
    waiter = reader._waiter = loop.create_future()
    eof_waiter = reader._eof_waiter = loop.create_future()

    waiter.set_result(1)
    eof_waiter.set_result(1)

    reader.feed_eof()

    assert waiter.done()
    assert eof_waiter.done()
    assert reader._waiter is None
    assert reader._eof_waiter is None


async def test_on_eof(protocol) -> None:
    loop = asyncio.get_event_loop()
    reader = streams.StreamReader(protocol, loop=loop)

    on_eof = mock.Mock()
    reader.on_eof(on_eof)

    assert not on_eof.called
    reader.feed_eof()
    assert on_eof.called


async def test_on_eof_empty_reader() -> None:
    reader = streams.EmptyStreamReader()

    on_eof = mock.Mock()
    reader.on_eof(on_eof)

    assert on_eof.called


async def test_on_eof_exc_in_callback(protocol) -> None:
    loop = asyncio.get_event_loop()
    reader = streams.StreamReader(protocol, loop=loop)

    on_eof = mock.Mock()
    on_eof.side_effect = ValueError

    reader.on_eof(on_eof)
    assert not on_eof.called
    reader.feed_eof()
    assert on_eof.called
    assert not reader._eof_callbacks


async def test_on_eof_exc_in_callback_empty_stream_reader() -> None:
    reader = streams.EmptyStreamReader()

    on_eof = mock.Mock()
    on_eof.side_effect = ValueError

    reader.on_eof(on_eof)
    assert on_eof.called


async def test_on_eof_eof_is_set(protocol) -> None:
    loop = asyncio.get_event_loop()
    reader = streams.StreamReader(protocol, loop=loop)
    reader.feed_eof()

    on_eof = mock.Mock()
    reader.on_eof(on_eof)
    assert on_eof.called
    assert not reader._eof_callbacks


async def test_on_eof_eof_is_set_exception(protocol) -> None:
    loop = asyncio.get_event_loop()
    reader = streams.StreamReader(protocol, loop=loop)
    reader.feed_eof()

    on_eof = mock.Mock()
    on_eof.side_effect = ValueError

    reader.on_eof(on_eof)
    assert on_eof.called
    assert not reader._eof_callbacks


async def test_set_exception(protocol) -> None:
    loop = asyncio.get_event_loop()
    reader = streams.StreamReader(protocol, loop=loop)
    waiter = reader._waiter = loop.create_future()
    eof_waiter = reader._eof_waiter = loop.create_future()

    exc = ValueError()
    reader.set_exception(exc)

    assert waiter.exception() is exc
    assert eof_waiter.exception() is exc
    assert reader._waiter is None
    assert reader._eof_waiter is None


async def test_set_exception_cancelled(protocol) -> None:
    loop = asyncio.get_event_loop()
    reader = streams.StreamReader(protocol, loop=loop)
    waiter = reader._waiter = loop.create_future()
    eof_waiter = reader._eof_waiter = loop.create_future()

    waiter.set_result(1)
    eof_waiter.set_result(1)

    exc = ValueError()
    reader.set_exception(exc)

    assert waiter.exception() is None
    assert eof_waiter.exception() is None
    assert reader._waiter is None
    assert reader._eof_waiter is None


async def test_set_exception_eof_callbacks(protocol) -> None:
    loop = asyncio.get_event_loop()
    reader = streams.StreamReader(protocol, loop=loop)

    on_eof = mock.Mock()
    reader.on_eof(on_eof)

    reader.set_exception(ValueError())
    assert not on_eof.called
    assert not reader._eof_callbacks


async def test_stream_reader_lines() -> None:
    line_iter = iter(DATA.splitlines(keepends=True))
    async for line in await create_stream():
        assert line == next(line_iter, None)
    pytest.raises(StopIteration, next, line_iter)


async def test_stream_reader_chunks_complete() -> None:
    """Tests if chunked iteration works if the chunking works out
    (i.e. the data is divisible by the chunk size)
    """
    chunk_iter = chunkify(DATA, 9)
    async for data in (await create_stream()).iter_chunked(9):
        assert data == next(chunk_iter, None)
    pytest.raises(StopIteration, next, chunk_iter)


async def test_stream_reader_chunks_incomplete() -> None:
    """Tests if chunked iteration works if the last chunk is incomplete"""
    chunk_iter = chunkify(DATA, 8)
    async for data in (await create_stream()).iter_chunked(8):
        assert data == next(chunk_iter, None)
    pytest.raises(StopIteration, next, chunk_iter)


async def test_data_queue_empty() -> None:
    """Tests that async looping yields nothing if nothing is there"""
    loop = asyncio.get_event_loop()
    buffer = streams.DataQueue(loop)
    buffer.feed_eof()

    async for _ in buffer:  # NOQA
        assert False


async def test_data_queue_items() -> None:
    """Tests that async looping yields objects identically"""
    loop = asyncio.get_event_loop()
    buffer = streams.DataQueue(loop)

    items = [object(), object()]
    buffer.feed_data(items[0], 1)
    buffer.feed_data(items[1], 1)
    buffer.feed_eof()

    item_iter = iter(items)
    async for item in buffer:
        assert item is next(item_iter, None)
    pytest.raises(StopIteration, next, item_iter)


async def test_stream_reader_iter_any() -> None:
    it = iter([b'line1\nline2\nline3\n'])
    async for raw in (await create_stream()).iter_any():
        assert raw == next(it)
    pytest.raises(StopIteration, next, it)


async def test_stream_reader_iter() -> None:
    it = iter([b'line1\n',
               b'line2\n',
               b'line3\n'])
    async for raw in await create_stream():
        assert raw == next(it)
    pytest.raises(StopIteration, next, it)


async def test_stream_reader_iter_chunks_no_chunked_encoding() -> None:
    it = iter([b'line1\nline2\nline3\n'])
    async for data, end_of_chunk in (await create_stream()).iter_chunks():
        assert (data, end_of_chunk) == (next(it), False)
    pytest.raises(StopIteration, next, it)


async def test_stream_reader_iter_chunks_chunked_encoding(protocol) -> None:
    loop = asyncio.get_event_loop()
    stream = streams.StreamReader(protocol, loop=loop)
    for line in DATA.splitlines(keepends=True):
        stream.begin_http_chunk_receiving()
        stream.feed_data(line)
        stream.end_http_chunk_receiving()
    stream.feed_eof()

    it = iter([b'line1\n', b'line2\n', b'line3\n'])
    async for data, end_of_chunk in stream.iter_chunks():
        assert (data, end_of_chunk) == (next(it), True)
    pytest.raises(StopIteration, next, it)
