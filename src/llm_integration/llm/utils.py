from pathlib import Path

from pydantic import ValidationError

from llm_integration.constants import ENCODING, SYS_PROMPT_FILE, Paths


def get_sys_prompt() -> str:
    prompt_file: Path = Paths.PROMPTS_DIR.value / SYS_PROMPT_FILE
    return prompt_file.read_text(encoding=ENCODING)


def make_repair_prompt(
    sys_prompt: str, user_prompt: str, error: ValidationError
) -> tuple[str, str]:
    new_sys_prompt = """
        Your previous answer was rejected for this reason. 
        Make the necessary corrections, and produce the correct output.
    """

    new_user_prompt = f""" 
        # ORIGINAL SYSTEM PROMPT

        {sys_prompt}

        # ORIGINAL USER PROMPT

        {user_prompt}

        # ERROR

        {error}
    """

    return new_sys_prompt, new_user_prompt
