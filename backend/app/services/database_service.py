import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal
from typing import List, Dict, Any
from app.config import Config
from app.utils.logger import logger

class DatabaseService:
    def __init__(self, config=Config):
        self.db_config = {
            'dbname': config.DB_NAME,
            'user': config.DB_USER,
            'password': config.DB_PASSWORD,
            'host': config.DB_HOST,
            'port': config.DB_PORT
        }

    def get_connection(self):
        return psycopg2.connect(**self.db_config)

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute SQL query and return results with type conversion"""
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                logger.debug(f"Executing SQL query: {query}")
                cursor.execute(query)
                results = cursor.fetchall()
                return self._convert_decimals(results)
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()

    def _convert_decimals(self, results: List[Dict]) -> List[Dict]:
        """Convert Decimal types to float for JSON serialization"""
        for row in results:
            for key, value in row.items():
                if isinstance(value, Decimal):
                    row[key] = float(value)
        return results

    def get_table_metadata(self) -> Dict[str, List]:
        """Retrieve database schema metadata"""
        query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        """
        results = self.execute_query(query)
        
        metadata = {}
        for row in results:
            table = row['table_name']
            if table not in metadata:
                metadata[table] = []
            metadata[table].append({
                'name': row['column_name'],
                'type': row['data_type']
            })
        return metadata