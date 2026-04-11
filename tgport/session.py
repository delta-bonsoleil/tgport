import hashlib
import json
import os
import uuid


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()[:12]


class SessionManager:
    """Maps (token_hash, chat_id) to Claude session UUIDs with file persistence."""

    def __init__(self, session_dir: str, token: str = ""):
        self._token_hash = _token_hash(token) if token else "default"
        os.makedirs(session_dir, exist_ok=True)
        self._path = os.path.join(session_dir, f"{self._token_hash}.json")
        self._sessions: dict[str, uuid.UUID] = {}
        self._load()

    def _key(self, chat_id: int) -> str:
        return f"{self._token_hash}:{chat_id}" if self._token_hash else str(chat_id)

    def _load(self):
        try:
            with open(self._path, encoding="utf-8") as f:
                data = json.load(f)
            self._sessions = {k: uuid.UUID(v) for k, v in data.items()}
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            self._sessions = {}

    def _save(self):
        tmp = self._path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({k: str(v) for k, v in self._sessions.items()}, f)
        os.replace(tmp, self._path)

    def get_or_create(self, chat_id: int) -> tuple[uuid.UUID, bool]:
        """Returns (session_uuid, is_new)."""
        key = self._key(chat_id)
        if key in self._sessions:
            return self._sessions[key], False
        sid = uuid.uuid4()
        self._sessions[key] = sid
        self._save()
        return sid, True

    def update(self, chat_id: int, session_id: str):
        """Update session ID from CLI response."""
        self._sessions[self._key(chat_id)] = uuid.UUID(session_id)
        self._save()

    def reset(self, chat_id: int) -> uuid.UUID:
        """Create a fresh session for this chat."""
        sid = uuid.uuid4()
        self._sessions[self._key(chat_id)] = sid
        self._save()
        return sid

    def is_known(self, chat_id: int) -> bool:
        return self._key(chat_id) in self._sessions
