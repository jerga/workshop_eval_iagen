from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    doc_id: str
    title: str
    content: str
    source_path: str


@dataclass
class RetrievedDocument:
    document: Document
    score: float


@dataclass
class ToolCall:
    tool_name: str
    arguments: dict[str, Any]
    result: str


@dataclass
class AgentResult:
    answer: str
    retrieved_documents: list[RetrievedDocument] = field(default_factory=list)
    tool_calls: list[ToolCall] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
