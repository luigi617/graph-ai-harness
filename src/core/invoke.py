from __future__ import annotations

import asyncio
import inspect


async def invoke(fn, *args, **kwargs):
    """Call a plugin method that may be written as either ``def`` or ``async def``.
    """
    if inspect.iscoroutinefunction(fn):
        return await fn(*args, **kwargs)
    return await asyncio.to_thread(fn, *args, **kwargs)
