'''
Main bigquery table
CREATE OR REPLACE TABLE `noble-office-299208.portfolio.gn-blog` (
  id STRING,
  blog_id STRING,
  title STRING,
  date TIMESTAMP,
  body STRING,
  views INT64,
  likes INT64,
  tags ARRAY<STRING>
)
OPTIONS(
  description = 'Table containing content with id, title, date, body, views, likes, and tags'
);

A minimal BigQuery client using google-api-core and avoiding the full SDK.
'''

import time
from google.auth import default
from google.auth.transport.requests import AuthorizedSession


class BigQueryClient:
    """A minimal BigQuery client using the REST API."""
    
    API_URL = "https://bigquery.googleapis.com/bigquery/v2"
    
    def __init__(
        self, 
        project_id=None
    ):
        """
        Initialize the BigQuery client.
        
        ### Args:
            - project_id: The Google Cloud project ID to use. If not provided, 
            it will be inferred from the credentials.
        """
        # Get credentials from the GOOGLE_APPLICATION_CREDENTIALS env var
        self.credentials, self._default_project_id = default(
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        self.project_id = project_id or self._default_project_id
        self.session = AuthorizedSession(self.credentials)
    
    def query(
        self, 
        sql, 
        params=None, 
        location="us-central1", 
        timeout_ms=30000, 
        dry_run=False, 
        max_results=100
    ):
        """
        Execute a SQL query on BigQuery.
        
        ### Args:
            - sql: The SQL query to execute.
            - params: Optional dict of query parameters.
            - location: The location to run the query in.
            - timeout_ms: Query timeout in milliseconds.
            - dry_run: If True, validate the query but do not execute it.
            - max_results: Maximum number of rows to return.
            
        ### Returns:
            - A list of dictionaries representing the query results.

        ### Example:
        ```python
        client = BigQueryClient()
        data = client.query("SELECT * FROM `noble-office-299208.portfolio.blog` LIMIT 1000")
        print(data)
        >>> <data.from.query>
        ```
        """
        # Setup the query job configuration
        query_job = {
            "query": sql,
            "useLegacySql": False,
            "location": location,
            "timeoutMs": timeout_ms,
            "dryRun": dry_run,
            "maxResults": max_results
        }
        
        # Add parameters if provided
        if params:
            query_parameters = []
            for name, value in params.items():
                param_type, param_value = self._get_parameter_type_and_value(value)
                query_parameters.append({
                    "name": name,
                    "parameterType": {"type": param_type},
                    "parameterValue": param_value
                })
            
            query_job["parameterMode"] = "NAMED"
            query_job["queryParameters"] = query_parameters
        
        # Execute the query
        url = f"{self.API_URL}/projects/{self.project_id}/queries"
        response = self.session.post(url, json=query_job)
        response.raise_for_status()
        query_response = response.json()
        
        # Check if the query is complete
        if not query_response.get("jobComplete", False) and not dry_run:
            job_id = query_response["jobReference"]["jobId"]
            return self._poll_query_results(job_id, location)
        
        # For dry run, just return whether the query is valid
        if dry_run:
            return {"isValid": True, "totalBytes": query_response.get("totalBytesProcessed")}
        
        # Process and return the results
        return self._process_query_results(query_response)
    
    def _poll_query_results(self, job_id, location):
        """
        Poll for query results until the job is complete.
        
        Args:
            job_id: The BigQuery job ID.
            location: The location the job is running in.
            
        Returns:
            The query results.
        """
        url = f"{self.API_URL}/projects/{self.project_id}/queries/{job_id}"
        params = {"location": location}
        
        while True:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            query_response = response.json()
            
            if query_response.get("jobComplete", False):
                return self._process_query_results(query_response)
            
            # Wait before polling again
            time.sleep(1)
    
    def _process_query_results(self, query_response):
        """
        Process the BigQuery response into a list of dictionaries.
        
        Args:
            query_response: The BigQuery response JSON.
            
        Returns:
            A list of dictionaries with the query results.
        """
        # Extract schema and rows
        schema = query_response.get("schema", {}).get("fields", [])
        rows = query_response.get("rows", [])
        
        # Convert to list of dictionaries
        result = []
        for row in rows:
            item = {}
            for i, cell in enumerate(row.get("f", [])):
                field_name = schema[i]["name"]
                field_type = schema[i]["type"]
                value = cell["v"]
                
                # Convert types as needed
                if field_type == "INTEGER":
                    value = int(value) if value is not None else None
                elif field_type == "FLOAT":
                    value = float(value) if value is not None else None
                elif field_type == "BOOLEAN":
                    value = value.lower() == "true" if value is not None else None
                
                item[field_name] = value
            
            result.append(item)
        
        return result
    
    def _get_parameter_type_and_value(self, value):
        """
        Get the BigQuery parameter type and value for a Python value.
        
        Args:
            value: The Python value to convert.
            
        Returns:
            Tuple of (type_string, parameter_value_dict)
        """
        if isinstance(value, bool):
            return "BOOL", {"value": "true" if value else "false"}
        elif isinstance(value, int):
            return "INT64", {"value": str(value)}
        elif isinstance(value, float):
            return "FLOAT64", {"value": str(value)}
        elif isinstance(value, list):
            # Handle array type
            if not value:
                return "ARRAY", {"arrayValues": []}
            
            # Use the type of the first element for the entire array
            item_type, _ = self._get_parameter_type_and_value(value[0])
            array_values = []
            
            for item in value:
                _, item_value = self._get_parameter_type_and_value(item)
                array_values.append(item_value)
            
            return "ARRAY", {
                "arrayValues": array_values,
                "arrayType": {"type": item_type}
            }
        else:
            # Default to string for other types
            return "STRING", {"value": str(value)}
    
    def create_dataset(self, dataset_id, location="US", description=None):
        """
        Create a new dataset in BigQuery.
        
        Args:
            dataset_id: The ID of the dataset to create.
            location: The location for the dataset.
            description: Optional description for the dataset.
            
        Returns:
            The response from the BigQuery API.
        """
        url = f"{self.API_URL}/projects/{self.project_id}/datasets"
        
        body = {
            "datasetReference": {
                "projectId": self.project_id,
                "datasetId": dataset_id
            },
            "location": location
        }
        
        if description:
            body["description"] = description
        
        response = self.session.post(url, json=body)
        response.raise_for_status()
        return response.json()
    
    def create_table(self, dataset_id, table_id, schema, description=None):
        """
        Create a new table in BigQuery.
        
        Args:
            dataset_id: The ID of the dataset to create the table in.
            table_id: The ID of the table to create.
            schema: The schema of the table as a list of field dictionaries.
            description: Optional description for the table.
            
        Returns:
            The response from the BigQuery API.
        """
        url = f"{self.API_URL}/projects/{self.project_id}/datasets/{dataset_id}/tables"
        
        body = {
            "tableReference": {
                "projectId": self.project_id,
                "datasetId": dataset_id,
                "tableId": table_id
            },
            "schema": {
                "fields": schema
            }
        }
        
        if description:
            body["description"] = description
        
        response = self.session.post(url, json=body)
        response.raise_for_status()
        return response.json()