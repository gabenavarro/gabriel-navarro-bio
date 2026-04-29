from typing import List, Optional
from src.services.gcp.bigquery import BigQueryClient
from src.models.project import Project
from src.config.settings import settings


class ProjectService:
    def __init__(self):
        self.client = BigQueryClient(project_id=settings.GOOGLE_PROJECT_ID)

    def get_all_projects(self, limit: int = 1000, include_disabled: bool = False) -> List[Project]:
        """Fetches all projects from BigQuery.

        By default, rows where `disabled = true` are filtered out at the SQL
        layer. Pass `include_disabled=True` for admin/preview use cases that
        need to see hidden posts as well.
        """
        if include_disabled:
            query = (
                f"SELECT * FROM `{settings.BIGQUERY_TABLE}` ORDER BY date DESC LIMIT {int(limit)}"
            )
        else:
            query = (
                f"SELECT * FROM `{settings.BIGQUERY_TABLE}` "
                f"WHERE disabled = false ORDER BY date DESC LIMIT {int(limit)}"
            )
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

    def get_project_by_slug(self, slug: str) -> Optional[Project]:
        """Look up a project by its slug. Client-side scan over all projects.

        BigQuery's gn-blog table does not yet have a slug column. Until the one-time
        ALTER TABLE + backfill runs, slugs only exist Python-side via from_dict's
        fallback to slugify(title). For ~20 posts a client-side scan is trivially
        fast; for >100 we'd want a SQL WHERE slug = @slug instead.
        """
        for project in self.get_all_projects(limit=1000, include_disabled=False):
            if project.slug == slug:
                return project
        return None

    def get_projects_by_tag(self, tag: str, include_disabled: bool = False) -> List[Project]:
        """Fetches projects filtered by tag.

        By default, rows where `disabled = true` are filtered out at the SQL
        layer. Pass `include_disabled=True` to bypass the filter.
        """
        # BigQuery array filtering
        where_disabled = "" if include_disabled else " AND disabled = false"
        query = (
            f"SELECT * FROM `{settings.BIGQUERY_TABLE}` "
            f"WHERE @tag IN UNNEST(tags){where_disabled} ORDER BY date DESC"
        )
        params = {"tag": tag}
        results = self.client.query(sql=query, params=params)

        if isinstance(results, dict):
            results = [results]

        return [Project.from_dict(r) for r in results]
