from dataclasses import dataclass
from enum import Enum
from typing import Optional

class MessageType(Enum):
    USER = "user"        # normal chat message
    CONTROL = "control"  # server commands like shutdown
    SYSTEM = "system"    # server info, join/leave, etc.

@dataclass
class Message:
    from_user: Optional[str]  # sender username, None if server
    to_user: Optional[str]    # target username, None for broadcast
    type: MessageType          # type of message
    content: str               # actual message text
