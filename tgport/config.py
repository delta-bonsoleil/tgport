import json
import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise RuntimeError(f"Environment variable {key} is required")
    return val


# マルチBot設定
# BOTS='[{"bot_token": "111:AAA...", "agent": "teddy"}, {"bot_token": "222:BBB...", "agent": ""}]'
# 未設定の場合は TELEGRAM_BOT_TOKEN + CLAUDE_AGENT にフォールバック
def _load_bots() -> list[dict]:
    raw = os.getenv("BOTS")
    if raw:
        try:
            bots = json.loads(raw)
            if isinstance(bots, list) and all("token" in b for b in bots):
                return bots
        except json.JSONDecodeError:
            pass
    return [{"token": _require("TELEGRAM_BOT_TOKEN"), "agent": os.getenv("CLAUDE_AGENT", "")}]


BOTS: list[dict] = _load_bots()
BOT_TOKEN: str = BOTS[0]["token"]  # 後方互換（既存コードとの互換性のため）

ALLOWED_USER_IDS: set[int] = {
    int(uid.strip())
    for uid in _require("ALLOWED_USER_IDS").split(",")
    if uid.strip()
}

CLAUDE_WORK_DIR: str = os.getenv("CLAUDE_WORK_DIR", os.path.expanduser("~"))
CLAUDE_MAX_TURNS: int = int(os.getenv("CLAUDE_MAX_TURNS", "3"))
CLAUDE_MAX_BUDGET_USD: float = float(os.getenv("CLAUDE_MAX_BUDGET_USD", "1.0"))
CLAUDE_SKIP_PERMISSIONS: bool = os.getenv("CLAUDE_SKIP_PERMISSIONS", "").lower() in ("1", "true", "yes")
DOWNLOAD_DIR: str = os.getenv("DOWNLOAD_DIR", os.path.expanduser("~/workspace/assets/downloads"))
EDIT_INTERVAL: float = float(os.getenv("EDIT_INTERVAL", "1.5"))
RESPONSE_TIMEOUT: int = int(os.getenv("RESPONSE_TIMEOUT", "300"))
LOG_DIR: str = os.getenv("LOG_DIR", os.path.expanduser("~/workspace/projects/tgport/logs"))
CLAUDE_MODEL: str = os.getenv("CLAUDE_MODEL", "sonnet")  # e.g. sonnet, opus, haiku
CLAUDE_EFFORT: str = os.getenv("CLAUDE_EFFORT", "low")  # low, medium, high, max
CLAUDE_TOOLS: str = os.getenv("CLAUDE_TOOLS", "")  # e.g. "Bash,Read,Edit,Write,Glob,Grep" (empty = all)
CLAUDE_DISABLE_SLASH: bool = os.getenv("CLAUDE_DISABLE_SLASH", "").lower() in ("1", "true", "yes")
LOG_RETENTION_DAYS: int = int(os.getenv("LOG_RETENTION_DAYS", "14"))
