from __future__ import annotations

import os
from typing import Any

import boto3
from dotenv import load_dotenv

from core.message import Message
from core.response import Response
from plugins.providers.base import BaseProvider
from protocols.tool import Tool

DEFAULT_REGION = "us-east-1"


class BedrockProvider(BaseProvider):
    def __init__(
        self,
        model: str,
        region: str | None = None,
        api_key: str | None = None,
        max_tokens: int = 1024,
        **params,
    ) -> None:
        super().__init__(model, **params)
        load_dotenv()
        self.region = region or os.getenv("AWS_REGION") or DEFAULT_REGION
        self.api_key = api_key or os.getenv("AWS_BEARER_TOKEN_BEDROCK")
        self.max_tokens = max_tokens
        self._client: Any = None

    def _get_client(self) -> Any:
        if self._client is None:
            if self.api_key:
                os.environ["AWS_BEARER_TOKEN_BEDROCK"] = self.api_key
            self._client = boto3.client("bedrock-runtime", region_name=self.region)
        return self._client

    def _generate(self, history: list[Message], tools: list[Tool]) -> Response:
        system, messages = self._to_converse(history)
        kwargs: dict[str, Any] = {
            "modelId": self.model,
            "messages": messages,
            "inferenceConfig": {"maxTokens": self.max_tokens, **self.params},
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["toolConfig"] = {"tools": [self._tool_spec(t) for t in tools]}
        response = self._get_client().converse(**kwargs)
        return self._parse(response)

    @staticmethod
    def _to_converse(history: list[Message]) -> tuple[list[dict], list[dict]]:
        system: list[dict] = []
        messages: list[dict] = []
        pending_results: list[dict] = []

        def flush_results() -> None:
            if pending_results:
                messages.append({"role": "user", "content": list(pending_results)})
                pending_results.clear()

        for m in history:
            if m.role == "tool":
                # Batch consecutive tool results into one user turn, each linked
                # back to its call via toolUseId.
                pending_results.append(
                    {
                        "toolResult": {
                            "toolUseId": m.tool_use_id,
                            "content": [{"text": m.content}],
                        }
                    }
                )
                continue

            flush_results()
            if m.role == "system":
                system.append({"text": m.content})
            elif m.role == "user":
                messages.append({"role": "user", "content": [{"text": m.content}]})
            elif m.role == "assistant":
                blocks: list[dict] = []
                if m.content:
                    blocks.append({"text": m.content})
                for call in m.tool_calls:
                    blocks.append(
                        {
                            "toolUse": {
                                "toolUseId": call.get("id"),
                                "name": call.get("name"),
                                "input": call.get("arguments", {}),
                            }
                        }
                    )
                messages.append({"role": "assistant", "content": blocks})

        flush_results()
        return system, messages

    @staticmethod
    def _tool_spec(tool: Tool) -> dict:
        return {
            "toolSpec": {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": {
                    "json": tool.parameters or {"type": "object", "properties": {}}
                },
            }
        }

    @staticmethod
    def _parse(response: dict) -> Response:
        blocks = response.get("output", {}).get("message", {}).get("content", [])
        text_parts: list[str] = []
        tool_calls: list[dict] = []
        for block in blocks:
            if "text" in block:
                text_parts.append(block["text"])
            elif "toolUse" in block:
                use = block["toolUse"]
                tool_calls.append(
                    {
                        "id": use.get("toolUseId"),
                        "name": use.get("name"),
                        "arguments": use.get("input", {}),
                    }
                )
        return Response(text="".join(text_parts), tool_calls=tool_calls)
