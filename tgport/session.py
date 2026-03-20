import uuid


class SessionManager:
    """Maps Telegram chat_id to Claude session UUIDs."""

    def __init__(self):
        self._sessions: dict[int, uuid.UUID] = {}

    def get_or_create(self, chat_id: int) -> tuple[uuid.UUID, bool]:
        """Returns (session_uuid, is_new)."""
        if chat_id in self._sessions:
            return self._sessions[chat_id], False
        sid = uuid.uuid4()
        self._sessions[chat_id] = sid
        return sid, True

    def reset(self, chat_id: int) -> uuid.UUID:
        """Create a fresh session for this chat."""
        sid = uuid.uuid4()
        self._sessions[chat_id] = sid
        return sid

    def is_known(self, chat_id: int) -> bool:
        return chat_id in self._sessions
