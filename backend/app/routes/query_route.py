from flask import Blueprint, request, jsonify
from app.services.database_service import DatabaseService
from app.services.llm_service import LLMService
from app.services.visualization_service import VisualizationService
from app.models.data_models import QueryResult
from app.utils.logger import logger

query_bp = Blueprint('query', __name__, url_prefix='/api/v1')
db_service = DatabaseService()
llm_service = LLMService()
viz_service = VisualizationService()

@query_bp.route('/query', methods=['POST'])
def handle_query():
    """Main query processing endpoint"""
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        viz_preference = data.get('visualization')

        if not prompt:
            return jsonify({
                "success": False,
                "error": "Missing required 'prompt' field"
            }), 400

        # Generate and execute SQL
        metadata = db_service.get_table_metadata()
        sql_query = llm_service.generate_sql(prompt, metadata)
        raw_data = db_service.execute_query(sql_query)

        # Process results
        result = viz_service.process_data(
            prompt,
            raw_data,
            viz_preference,
            llm_service
        )

        return jsonify({
            "success": result.success,
            "visualization_type": result.visualization_type.value,
            "data": result.processed_data,
            "raw": result.raw_data,
            "human_readable": result.human_readable
        })

    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e),
            "human_readable": f"Error processing request: {str(e)}"
        }), 500