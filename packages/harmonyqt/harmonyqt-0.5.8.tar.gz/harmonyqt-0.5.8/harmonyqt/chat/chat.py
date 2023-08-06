# Copyright 2018 miruka
# This file is part of harmonyqt, licensed under GPLv2.

from typing import Callable, Dict

from cachetools import LFUCache
from kids.cache import cache
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from harmonyqt import main, main_window, message

CHAT_INIT_HOOKS: Dict[str, Callable[["Chat"], None]] = {}


class UserNotLoggedInError(Exception):
    def __init__(self, user_id: str) -> None:
        super().__init__(f"Not logged in to account {user_id!r}.")

class RoomNotJoinedError(Exception):
    def __init__(self, user_id: str, room_id: str) -> None:
        super().__init__(f"{user_id!r} is not part of the room {room_id!r}.")


@cache(use=LFUCache(maxsize=64))
class Chat(QWidget):
    def __init__(self, user_id: str, room_id: str) -> None:
        super().__init__()

        try:
            self.client = main_window().accounts[user_id]
        except KeyError:
            raise UserNotLoggedInError(user_id)

        try:
            self.room = self.client.rooms[room_id]
        except KeyError:
            raise RoomNotJoinedError(user_id, room_id)

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)

        # Because of circular import
        from .display import ChatMessageDisplay
        from .send_area import SendArea
        self.messages  = ChatMessageDisplay(self)
        self.send_area = SendArea(self)

        # Make messages scroller controllable by shortcuts even when user
        # focuses sendbox, see app().get_focused parent scroller detection.
        self.scroller = self.messages.scroller

        self.vbox.addWidget(self.messages)
        self.vbox.addWidget(self.send_area)

        for hook in CHAT_INIT_HOOKS.values():
            hook(self)


def redirect_message(msg: message.Message) -> None:
    if msg.receiver_id is None:  # local echo
        return

    chat = Chat(msg.receiver_id, msg.room_id)  # cache
    chat.messages.on_receive_from_server(msg)


main.HOOKS_INIT_2_BEFORE_LOGIN["Connect chat Message redirector"] = \
    lambda win: win.events.signals.new_message.connect(redirect_message)
