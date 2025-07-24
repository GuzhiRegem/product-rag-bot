from typing import Literal, Optional, TypedDict


class MessageDict(TypedDict):
    role: Literal['user', 'assistant', 'system']
    content: str


class Conversation:
    """A class to manage a conversation with a series of messages."""
    def __init__(
        self,
        messages: Optional[list[MessageDict]] = None,
        system_message: Optional[str] = None
    ) -> None:
        self.__messages: list[MessageDict] = list()
        if system_message is not None:
            self.__messages.append({
                'role': 'system',
                'content': system_message
            })
        if messages is not None:
            self.__messages = messages.copy()

    @property
    def messages(self) -> list[MessageDict]:
        return self.__messages

    def add(
        self,
        role: Literal['user', 'assistant', 'system'],
        content: str
    ) -> "Conversation":
        message: MessageDict = {'role': role, 'content': content}
        self.__messages.append(message)
        return self
