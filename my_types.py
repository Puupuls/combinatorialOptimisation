# Risinājumam nepieciešamie datu tipi
from __future__ import annotations

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Point:
    x: float
    y: float
    value: float = 1


@dataclass_json
@dataclass
class Domain:
    points: list[Point] = field(default_factory=list)
    distances: list[list[int]] = field(default_factory=list)
    time_limit = 10
    start_point_idx: int = 0
    finish_point_idx: int = 0
    solutions: list[Solution] = field(default_factory=list)


@dataclass_json
@dataclass
class GraphNode:
    point: Point
    links: list[GraphNode] = field(default_factory=list)


@dataclass_json
@dataclass
class Solution:
    links: list[list[int]] = field(default_factory=list)
    cost: float = 0
    best_path_len: float = 0
    best_path_steps: int = 0
    cost_parts: dict[str, float] = field(default_factory=dict)
