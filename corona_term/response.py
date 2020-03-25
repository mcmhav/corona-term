from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Field():
    """Corona field."""

    name: str
    type: str
    alias: str
    sqlType: str
    domain: Optional[str]
    defaultValue: Optional[str]


@dataclass
class Feature():
    """Corona feature."""

    attributes: Dict


@dataclass
class Response():
    """Corona response."""

    objectIdFieldName: str
    uniqueIdField: Dict
    globalIdFieldName: str
    geometryType: str
    spatialReference: Dict
    fields: List[Field]
    features: List[Feature]

    def __post_init__(self):
        self.features = [Feature(**feature) for feature in self.features]
