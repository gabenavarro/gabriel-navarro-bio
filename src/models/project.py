from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ProjectTag:
    v: str

@dataclass
class Project:
    id: str
    blog_id: str
    title: str
    description: str
    image: str
    tags: List[str] = field(default_factory=list)
    disabled: bool = False
    views: int = 0
    likes: int = 0
    date: str = ""
    body: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        # Process tags if they are in the format returned by BigQuery [{'v': 'tag1'}, ...]
        raw_tags = data.get("tags", [])
        tags = []
        if isinstance(raw_tags, list):
            for tag in raw_tags:
                if isinstance(tag, dict) and "v" in tag:
                    tags.append(tag["v"])
                elif isinstance(tag, str):
                    tags.append(tag)
        
        return cls(
            id=data.get("id", ""),
            blog_id=data.get("blog_id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            image=data.get("image", ""),
            tags=tags,
            disabled=data.get("disabled", False),
            views=data.get("views", 0),
            likes=data.get("likes", 0),
            date=data.get("date", ""),
            body=data.get("body", "")
        )
