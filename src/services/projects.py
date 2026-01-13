from typing import List, Optional
from src.lib.google.bigquery import BigQueryClient
from src.models.project import Project
from src.config import settings


class ProjectService:
    def __init__(self):
        self.client = BigQueryClient(project_id=settings.GOOGLE_PROJECT_ID)

    def get_all_projects(self, limit: int = 1000) -> List[Project]:
        """Fetches all projects from BigQuery."""
        query = f"SELECT * FROM `{settings.BIGQUERY_TABLE}` LIMIT {limit}"
        results = self.client.query(sql=query)

        if isinstance(results, dict):
            results = [results]

        return [Project.from_dict(r) for r in results]

    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Fetches a single project by its ID."""
        # Using parameterized query for security
        query = f"SELECT * FROM `{settings.BIGQUERY_TABLE}` WHERE id = @project_id"
        params = {"project_id": project_id}
        results = self.client.query(sql=query, params=params)

        if results and isinstance(results, list):
            return Project.from_dict(results[0])
        elif results and isinstance(results, dict):
            return Project.from_dict(results)

        return None

    def get_projects_by_tag(self, tag: str) -> List[Project]:
        """Fetches projects filtered by tag."""
        # BigQuery array filtering
        query = f"SELECT * FROM `{settings.BIGQUERY_TABLE}` WHERE @tag IN UNNEST(tags)"
        params = {"tag": tag}
        results = self.client.query(sql=query, params=params)

        if isinstance(results, dict):
            results = [results]

        return [Project.from_dict(r) for r in results]
