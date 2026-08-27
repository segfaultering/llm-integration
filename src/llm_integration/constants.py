from enum import Enum

from llm_integration.config import settings

ENCODING: str = "utf-8"
SYS_PROMPT_FILE: str = "sent-clf-v1.md"
LOG_FILE: str = "app.logs"


class Paths(Enum):
    # Project
    ROOT_DIR = settings.app_root
    PROMPTS_DIR = settings.app_root / "prompts"
    EVALS_DIR = settings.app_root / "evals"
    LOGS_DIR = settings.app_root / "logs"
