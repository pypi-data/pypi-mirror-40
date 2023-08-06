# coding: UTF-8

from ctypes import c_long, c_uint, pointer

from .aio_block import AIOBlock
from .aio_event import AIOEvent
from .raw import IOEvent, Timespec, aio_context_t, io_cancel, io_destroy, io_getevents, io_setup, io_submit, iocb_p


def create_c_array(c_type, elements, length: int = None):
    elements_tup = tuple(elements)
    if length is None:
        length = len(elements_tup)
    return (c_type * length)(*elements_tup)


class AIOContext:
    __slots__ = ('_ctx', '_max_jobs')

    def __init__(self, max_jobs: int) -> None:
        self._ctx = aio_context_t()  # type: aio_context_t
        self._max_jobs = max_jobs  # type: int

        io_setup(c_uint(max_jobs), pointer(self._ctx))

    def __del__(self) -> None:
        self.close()

    @property
    def closed(self) -> bool:
        return self._ctx.value is 0

    def close(self) -> None:
        """will block on the completion of all operations that could not be canceled"""
        if not self.closed:
            io_destroy(self._ctx)
            self._ctx = aio_context_t()

    def cancel(self, block: AIOBlock) -> AIOEvent:
        result = IOEvent()

        # noinspection PyProtectedMember
        io_cancel(self._ctx, pointer(block._iocb), pointer(result))

        return AIOEvent(result)

    def submit(self, *blocks: AIOBlock) -> int:
        # noinspection PyProtectedMember
        return io_submit(
                self._ctx,
                c_long(len(blocks)),
                create_c_array(iocb_p, (pointer(block._iocb) for block in blocks))
        )

    def get_events(self, min_jobs: int, max_jobs: int, timeout_ns: int = 0) -> tuple:
        event_buf = create_c_array(IOEvent, (), max_jobs)

        completed_jobs = io_getevents(
                self._ctx,
                c_long(min_jobs),
                c_long(max_jobs),
                event_buf,
                pointer(Timespec(*divmod(timeout_ns, 1000000000))) if timeout_ns > 0 else None
        )

        return tuple(AIOEvent(event) for event in event_buf[:completed_jobs])

    def __enter__(self) -> 'AIOContext':
        return self

    def __exit__(self, t, value, traceback) -> None:
        self.close()
