import json
import os
import uuid


class SessionManager:
    """Maps Telegram chat_id to Claude session UUIDs with file persistence."""

    def __init__(self, path: str | None = None):
        self._path = path or os.path.expanduser("~/workspace/projects/tgport/sessions.json")
        self._sessions: dict[int, uuid.UUID] = {}
        self._load()

    def _load(self):
        try:
            with open(self._path, encoding="utf-8") as f:
                data = json.load(f)
            self._sessions = {int(k): uuid.UUID(v) for k, v in data.items()}
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            self._sessions = {}

    def _save(self):
        tmp = self._path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({str(k): str(v) for k, v in self._sessions.items()}, f)
        os.replace(tmp, self._path)

    def get_or_create(self, chat_id: int) -> tuple[uuid.UUID, bool]:
        """Returns (session_uuid, is_new)."""
        if chat_id in self._sessions:
            return self._sessions[chat_id], False
        sid = uuid.uuid4()
        self._sessions[chat_id] = sid
        self._save()
        return sid, True

    def update(self, chat_id: int, session_id: str):
        """Update session ID from CLI response."""
        self._sessions[chat_id] = uuid.UUID(session_id)
        self._save()

    def reset(self, chat_id: int) -> uuid.UUID:
        """Create a fresh session for this chat."""
        sid = uuid.uuid4()
        self._sessions[chat_id] = sid
        self._save()
        return sid

    def is_known(self, chat_id: int) -> bool:
        return chat_id in self._sessions
