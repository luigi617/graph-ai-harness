from __future__ import annotations


class Registry:
    def __init__(self) -> None:
        self._plugins: list[object] = []

    def add(self, plugin: object) -> None:
        if not hasattr(plugin, "kind"):
            raise TypeError(
                f"{type(plugin).__name__} is not a plugin (no 'kind' attribute)"
            )
        self._plugins.append(plugin)

    def get(self, kind: str) -> object | None:
        for plugin in reversed(self._plugins):
            if getattr(plugin, "kind", None) == kind:
                return plugin
        return None

    def all(self, kind: str) -> list[object]:
        return [p for p in self._plugins if getattr(p, "kind", None) == kind]

    def kinds(self) -> set[str]:
        return {getattr(p, "kind") for p in self._plugins}
