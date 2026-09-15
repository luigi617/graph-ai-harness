from __future__ import annotations

from typing import ClassVar, Protocol, runtime_checkable


@runtime_checkable
class Plugin(Protocol):
    """Common base of every plugin protocol: each declares a ``kind``. Used to
    bound the type-keyed registry lookups (``get``/``all``) so they resolve a
    plugin by its protocol type and return that exact type."""

    kind: ClassVar[str]
