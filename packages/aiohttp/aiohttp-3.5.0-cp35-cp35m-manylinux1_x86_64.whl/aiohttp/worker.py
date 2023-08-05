"""Async gunicorn worker for aiohttp.web"""

import asyncio
import os
import re
import signal
import sys
from contextlib import suppress
from types import FrameType
from typing import Any, Optional  # noqa

from gunicorn.config import AccessLogFormat as GunicornAccessLogFormat
from gunicorn.workers import base

from aiohttp import web

from .helpers import set_result
from .web_log import AccessLogger


try:
    import ssl
    SSLContext = ssl.SSLContext  # noqa
except ImportError:  # pragma: no cover
    ssl = None  # type: ignore
    SSLContext = object  # type: ignore


__all__ = ('GunicornWebWorker',
           'GunicornUVLoopWebWorker',
           'GunicornTokioWebWorker')


class GunicornWebWorker(base.Worker):

    DEFAULT_AIOHTTP_LOG_FORMAT = AccessLogger.LOG_FORMAT
    DEFAULT_GUNICORN_LOG_FORMAT = GunicornAccessLogFormat.default

    def __init__(self, *args: Any, **kw: Any) -> None:  # pragma: no cover
        super().__init__(*args, **kw)

        self._runner = None  # type: Optional[web.AppRunner]
        self._task = None  # type: Optional[asyncio.Task[None]]
        self.exit_code = 0
        self._notify_waiter = None  # type: Optional[asyncio.Future[bool]]

    def init_process(self) -> None:
        # create new event_loop after fork
        asyncio.get_event_loop().close()

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        super().init_process()

    def run(self) -> None:
        access_log = self.log.access_log if self.cfg.accesslog else None
        params = dict(
            logger=self.log,
            keepalive_timeout=self.cfg.keepalive,
            access_log=access_log,
            access_log_format=self._get_valid_log_format(
                self.cfg.access_log_format))
        if asyncio.iscoroutinefunction(self.wsgi):  # type: ignore
            self.wsgi = self.loop.run_until_complete(
                self.wsgi())  # type: ignore
        self._runner = web.AppRunner(self.wsgi, **params)
        self.loop.run_until_complete(self._runner.setup())
        self._task = self.loop.create_task(self._run())

        with suppress(Exception):  # ignore all finalization problems
            self.loop.run_until_complete(self._task)
        if sys.version_info >= (3, 6):
            if hasattr(self.loop, 'shutdown_asyncgens'):
                self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        self.loop.close()

        sys.exit(self.exit_code)

    async def _run(self) -> None:
        ctx = self._create_ssl_context(self.cfg) if self.cfg.is_ssl else None

        runner = self._runner
        assert runner is not None
        server = runner.server
        assert server is not None
        for sock in self.sockets:
            site = web.SockSite(
                runner, sock, ssl_context=ctx,
                shutdown_timeout=self.cfg.graceful_timeout / 100 * 95)
            await site.start()

        # If our parent changed then we shut down.
        pid = os.getpid()
        try:
            while self.alive:  # type: ignore
                self.notify()

                cnt = server.requests_count
                if self.cfg.max_requests and cnt > self.cfg.max_requests:
                    self.alive = False
                    self.log.info("Max requests, shutting down: %s", self)

                elif pid == os.getpid() and self.ppid != os.getppid():
                    self.alive = False
                    self.log.info("Parent changed, shutting down: %s", self)
                else:
                    await self._wait_next_notify()
        except BaseException:
            pass

        await runner.cleanup()

    def _wait_next_notify(self) -> 'asyncio.Future[bool]':
        self._notify_waiter_done()

        loop = self.loop
        assert loop is not None
        self._notify_waiter = waiter = loop.create_future()
        self.loop.call_later(1.0, self._notify_waiter_done, waiter)

        return waiter

    def _notify_waiter_done(self, waiter: 'asyncio.Future[bool]'=None) -> None:
        if waiter is None:
            waiter = self._notify_waiter
        if waiter is not None:
            set_result(waiter, True)

        if waiter is self._notify_waiter:
            self._notify_waiter = None

    def init_signals(self) -> None:
        # Set up signals through the event loop API.

        self.loop.add_signal_handler(signal.SIGQUIT, self.handle_quit,
                                     signal.SIGQUIT, None)

        self.loop.add_signal_handler(signal.SIGTERM, self.handle_exit,
                                     signal.SIGTERM, None)

        self.loop.add_signal_handler(signal.SIGINT, self.handle_quit,
                                     signal.SIGINT, None)

        self.loop.add_signal_handler(signal.SIGWINCH, self.handle_winch,
                                     signal.SIGWINCH, None)

        self.loop.add_signal_handler(signal.SIGUSR1, self.handle_usr1,
                                     signal.SIGUSR1, None)

        self.loop.add_signal_handler(signal.SIGABRT, self.handle_abort,
                                     signal.SIGABRT, None)

        # Don't let SIGTERM and SIGUSR1 disturb active requests
        # by interrupting system calls
        signal.siginterrupt(signal.SIGTERM, False)
        signal.siginterrupt(signal.SIGUSR1, False)

    def handle_quit(self, sig: int, frame: FrameType) -> None:
        self.alive = False

        # worker_int callback
        self.cfg.worker_int(self)

        # wakeup closing process
        self._notify_waiter_done()

    def handle_abort(self, sig: int, frame: FrameType) -> None:
        self.alive = False
        self.exit_code = 1
        self.cfg.worker_abort(self)
        sys.exit(1)

    @staticmethod
    def _create_ssl_context(cfg: Any) -> 'SSLContext':
        """ Creates SSLContext instance for usage in asyncio.create_server.

        See ssl.SSLSocket.__init__ for more details.
        """
        if ssl is None:  # pragma: no cover
            raise RuntimeError('SSL is not supported.')

        ctx = ssl.SSLContext(cfg.ssl_version)
        ctx.load_cert_chain(cfg.certfile, cfg.keyfile)
        ctx.verify_mode = cfg.cert_reqs
        if cfg.ca_certs:
            ctx.load_verify_locations(cfg.ca_certs)
        if cfg.ciphers:
            ctx.set_ciphers(cfg.ciphers)
        return ctx

    def _get_valid_log_format(self, source_format: str) -> str:
        if source_format == self.DEFAULT_GUNICORN_LOG_FORMAT:
            return self.DEFAULT_AIOHTTP_LOG_FORMAT
        elif re.search(r'%\([^\)]+\)', source_format):
            raise ValueError(
                "Gunicorn's style options in form of `%(name)s` are not "
                "supported for the log formatting. Please use aiohttp's "
                "format specification to configure access log formatting: "
                "http://docs.aiohttp.org/en/stable/logging.html"
                "#format-specification"
            )
        else:
            return source_format


class GunicornUVLoopWebWorker(GunicornWebWorker):

    def init_process(self) -> None:
        import uvloop

        # Close any existing event loop before setting a
        # new policy.
        asyncio.get_event_loop().close()

        # Setup uvloop policy, so that every
        # asyncio.get_event_loop() will create an instance
        # of uvloop event loop.
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        super().init_process()


class GunicornTokioWebWorker(GunicornWebWorker):

    def init_process(self) -> None:  # pragma: no cover
        import tokio

        # Close any existing event loop before setting a
        # new policy.
        asyncio.get_event_loop().close()

        # Setup tokio policy, so that every
        # asyncio.get_event_loop() will create an instance
        # of tokio event loop.
        asyncio.set_event_loop_policy(tokio.EventLoopPolicy())

        super().init_process()
