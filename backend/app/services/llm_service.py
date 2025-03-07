import ollama
import groq
from typing import Optional
from app.config import Config
from app.utils.logger import logger
import json

class LLMService:
    def __init__(self, model: str = Config.LLM_MODEL):
        self.model = model
        self.use_groq = bool(Config.GROQ_API_KEY)
        if self.use_groq:
            # Initialize Groq client if API key exists
            self.client = groq.Groq(api_key=Config.GROQ_API_KEY)

    def generate_sql(self, prompt: str, metadata: dict) -> str:
        """Generate SQL query from natural language prompt"""
        sql_prompt = f"""
        Query: {prompt}
    
        You are a highly intelligent agent designed to interact with SQL databases. 
        Your primary responsibility is to analyze the provided input question and generate a syntactically correct SQL query based solely on the given table and column metadata: {json.dumps(metadata, indent=2)}. 
        Ensure the query strictly adheres to the structure and constraints of the metadata. 
        If any table or column mentioned in the query is missing or invalid, adapt and rewrite the query accordingly. 
        Your output should be a precise and concise SQL query, free from any additional text, formatting, or punctuation such as triple backticks or brackets. 
        Focus on generating accurate and optimized SQL queries to retrieve the required information effectively.

        Rules:
        1. Use only existing tables/columns
        2. Prefer explicit JOINs over implicit
        3. Include necessary WHERE clauses
        4. Return plain SQL without markdown
        """
        
        try:
            if self.use_groq:
                response = self.client.chat.completions.create(
                    messages=[{'role': 'user', 'content': sql_prompt}],
                    model=self.model
                )
                raw_response = response.choices[0].message.content
            else:
                response = ollama.chat(
                    model=self.model,
                    messages=[{'role': 'user', 'content': sql_prompt}]
                )
                raw_response = response.message.content

            return self._clean_sql_response(raw_response)
        except Exception as e:
            logger.error(f"SQL generation failed: {str(e)}")
            raise

    def _clean_sql_response(self, response: str) -> str:
        """Remove markdown formatting and trim whitespace"""
        return response.strip().strip('`').strip()

    def determine_visualization(self, prompt: str, data_sample: list, preference: Optional[str]) -> str:
        """Determine appropriate visualization type using LLM"""
        viz_prompt = f"""
        Analyze this query and data to determine the best visualization type:
        Query: {prompt}
        Data sample: {json.dumps(data_sample, indent=2)}
        User preference: {preference or 'none'}
        
        Available types: table, graph, pie
        Consider:
        1. Data types (categorical vs numerical)
        2. Number of data points
        3. User's stated preference
        4. Common visualization best practices
    
        Respond ONLY with the visualization type (table, graph, or pie)
        """
        
        try:
            if self.use_groq:
                response = self.client.chat.completions.create(
                    messages=[{'role': 'user', 'content': viz_prompt}],
                    model=self.model
                )
                viz_type = response.choices[0].message.content.strip().lower()
            else:
                response = ollama.chat(
                    model=self.model,
                    messages=[{'role': 'user', 'content': viz_prompt}]
                )
                viz_type = response.message.content.strip().lower()

            return viz_type
        except Exception as e:
            logger.error(f"Visualization determination failed: {str(e)}")
            return "table"

    def generate_summary(self, prompt: str, data_sample: list, viz_type: str) -> str:
        """Generate human-readable data summary using LLM"""
        summary_prompt = f"""
        Create a concise, natural language summary of these SQL query results.
        Original query: {prompt}
        Visualization type: {viz_type}
        Data sample: {json.dumps(data_sample, indent=2)}
        
        Include:
        1. Brief description of the data structure
        2. Key findings/numbers
        3. Notable trends/patterns
        4. Data quality notes (if any)
    
        Keep response under 150 words. Use plain text format
        """
        
        try:
            if self.use_groq:
                response = self.client.chat.completions.create(
                    messages=[{'role': 'user', 'content': summary_prompt}],
                    model=self.model
                )
                summary = response.choices[0].message.content.strip()
            else:
                response = ollama.chat(
                    model=self.model,
                    messages=[{'role': 'user', 'content': summary_prompt}]
                )
                summary = response.message.content.strip()

            return summary
        except Exception as e:
            logger.error(f"Summary generation failed: {str(e)}")
            return "Summary unavailable - please review raw data"