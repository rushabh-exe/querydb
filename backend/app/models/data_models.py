from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

class VisualizationType(Enum):
    TABLE = "table"
    GRAPH = "graph"
    PIE_CHART = "pie"

@dataclass
class QueryResult:
    raw_data: List[Dict[str, Any]]
    visualization_type: VisualizationType
    processed_data: Dict[str, Any]
    human_readable: str
    success: bool = True
    error: Optional[str] = None