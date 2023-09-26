# Risinājumam nepieciešamie datu tipi
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


@dataclass_json
@dataclass
class Solution:
    domain: Domain
    links: list[list[int]] = field(default_factory=list)
    cost: float = 0
