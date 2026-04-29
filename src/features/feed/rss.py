"""Build RSS 2.0 feed XML from a list of Project objects.

Pure stdlib XML construction (no feedgen, no lxml). Caps at 50 items per
the RSS spec convention; CDATA-wraps title/description to avoid escaping.
"""

from datetime import datetime, timezone
from email.utils import format_datetime
from typing import List

from src.models.project import Project

SITE_URL = "https://gabriel.navarro.bio"
SITE_TITLE = "Gabriel Navarro"
SITE_DESCRIPTION = "Posts on computational biology, foundation models, and infrastructure."


def _project_link(project: Project, base: str = SITE_URL) -> str:
    """Prefer slug-based URL; fall back to UUID for legacy/empty-slug rows."""
    if project.slug:
        return f"{base}/blogs/slug/{project.slug}"
    return f"{base}/blogs/{project.id}"


def _format_pub_date(date_str: str) -> str:
    """Convert an ISO 8601 string (BigQuery format) to RFC 822 for RSS."""
    if not date_str:
        return ""
    # BigQuery serializes timestamps with trailing Z; normalize for fromisoformat
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        return ""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return format_datetime(dt)


def _item_xml(project: Project) -> str:
    pub_date = _format_pub_date(project.date)
    categories = "\n      ".join(f"<category>{tag}</category>" for tag in project.tags)
    return f"""    <item>
      <title><![CDATA[{project.title}]]></title>
      <link>{_project_link(project)}</link>
      <guid isPermaLink="false">{project.id}</guid>
      <pubDate>{pub_date}</pubDate>
      <description><![CDATA[{project.description}]]></description>
      {categories}
    </item>"""


def build_rss_feed(projects: List[Project], site_url: str = SITE_URL) -> str:
    """Render an RSS 2.0 feed for the given projects (cap 50 items)."""
    last_build = format_datetime(datetime.now(timezone.utc))
    items = "\n".join(_item_xml(p) for p in projects[:50])
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SITE_TITLE}</title>
    <link>{site_url}/blogs</link>
    <description>{SITE_DESCRIPTION}</description>
    <language>en-us</language>
    <lastBuildDate>{last_build}</lastBuildDate>
    <atom:link href="{site_url}/feed.xml" rel="self" type="application/rss+xml" />
{items}
  </channel>
</rss>
"""
