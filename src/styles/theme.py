from src.config import settings

THEME_CSS = f"""
:root {{
    --primary-color: {settings.COLORS["primary"]};
    --secondary-color: {settings.COLORS["secondary"]};
    --category-omics: {settings.COLORS["omics"]};
    --category-machine-learning: {settings.COLORS["machine-learning"]};
    --category-infrastructure: {settings.COLORS["infrastructure"]};
    --category-visualization: {settings.COLORS["visualization"]};
    --white: {settings.COLORS["white"]};
    --black: {settings.COLORS["black"]};
}}
"""
