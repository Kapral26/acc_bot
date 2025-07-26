from enum import Enum


class ChatTypeEnum(Enum):
    private = "private"
    group = "group"
    supergroup = "supergroup"
    channel = "channel"