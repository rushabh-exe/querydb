from typing import Dict, List, Any, Optional
from app.models.data_models import VisualizationType, QueryResult
from app.utils.logger import logger

class VisualizationService:
    def __init__(self):
        self.converters = {
            VisualizationType.TABLE: self.convert_to_table,
            VisualizationType.GRAPH: self.convert_to_graph,
            VisualizationType.PIE_CHART: self.convert_to_pie_chart
        }

    def process_data(
        self,
        prompt: str,
        raw_data: List[Dict[str, Any]],
        preference: Optional[str],
        llm_service
    ) -> QueryResult:
        """Process raw data into visualization-ready format"""
        try:
            viz_type = self._determine_visualization_type(
                prompt, 
                raw_data, 
                preference,
                llm_service
            )
            
            processed_data = self.converters[viz_type](raw_data)
            summary = llm_service.generate_summary(
                prompt, 
                raw_data[:3], 
                viz_type.value
            )
            
            return QueryResult(
                raw_data=raw_data,
                visualization_type=viz_type,
                processed_data=processed_data,
                human_readable=summary
            )
            
        except Exception as e:
            logger.error(f"Data processing failed: {str(e)}")
            return QueryResult(
                raw_data=raw_data,
                visualization_type=VisualizationType.TABLE,
                processed_data=self.convert_to_table(raw_data),
                human_readable=f"Error: {str(e)}",
                success=False
            )

    def _determine_visualization_type(
        self,
        prompt: str,
        data: List[Dict],
        preference: Optional[str],
        llm_service
    ) -> VisualizationType:
        """Determine visualization type with fallback logic"""
        if preference:
            try:
                return VisualizationType(preference.lower())
            except ValueError:
                logger.warning(f"Invalid visualization preference: {preference}")

        # Get LLM suggestion if no valid preference
        llm_suggestion = llm_service.determine_visualization(
            prompt,
            data[:2] if data else [],
            preference
        )
        
        try:
            return VisualizationType(llm_suggestion)
        except ValueError:
            logger.warning(f"Invalid LLM visualization suggestion: {llm_suggestion}")
            return VisualizationType.TABLE

    @staticmethod
    def convert_to_table(data: List[Dict]) -> Dict[str, Any]:
        """Convert raw data to table format"""
        if not data:
            return {"columns": [], "rows": []}
        
        columns = [{
            "name": key,
            "type": type(value).__name__
        } for key, value in data[0].items()]
        
        return {
            "columns": columns,
            "rows": [dict(row) for row in data]
        }

    @staticmethod
    def convert_to_graph(data: List[Dict]) -> Dict[str, Any]:
        """Convert raw data to graph format"""
        if not data:
            return {"type": "graph", "data": [], "config": {}}
        
        keys = list(data[0].keys())
        return {
            "type": "graph",
            "data": data,
            "config": {
                "xAxis": keys[0],
                "yAxis": keys[1] if len(keys) > 1 else keys[0],
                "graphType": "line"
            }
        }

    @staticmethod
    def convert_to_pie_chart(data: List[Dict]) -> Dict[str, Any]:
        """Convert raw data to pie chart format"""
        if not data:
            return {"type": "pie", "data": []}
        
        keys = list(data[0].keys())
        return {
            "type": "pie",
            "data": [{
                "label": str(row[keys[0]]),
                "value": float(row[keys[1]]) if len(keys) > 1 else 1
            } for row in data]
        }