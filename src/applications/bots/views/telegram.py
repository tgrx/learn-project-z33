import json
from typing import NamedTuple

import requests
from django.conf import settings
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View

from applications.bots.apis import TG_API


class ChatT(NamedTuple):
    id: str


class MessageT(NamedTuple):
    id: str
    text: str
    chat: ChatT


class TelegramBotView(View):
    def _receive_message_from_user(self) -> MessageT:
        payload = json.loads(self.request.body)

        message = payload["message"]
        message_id = message["message_id"]
        text: str = message["text"]

        chat = message["chat"]
        chat_id = chat["id"]

        chat = ChatT(id=chat_id)
        message = MessageT(chat=chat, id=message_id, text=text)

        return message

    def _send_message_to_user(self, chat_id: str, text: str):
        api_url = TG_API.format(token=settings.TG_BOT_TOKEN, method="sendMessage")

        payload = {
            "chat_id": chat_id,
            "text": text,
        }

        tg_response = requests.post(api_url, json=payload)
        print(tg_response.status_code)
        print(tg_response.json())

    def post(self, _request: HttpRequest):
        try:
            message = self._receive_message_from_user()

            reply = message.text.upper()

            self._send_message_to_user(message.chat.id, reply)

        finally:
            return HttpResponse(content="")

    @staticmethod
    def register(_request: HttpRequest):
        api_url = TG_API.format(token=settings.TG_BOT_TOKEN, method="setWebhook")
        my_bot_path = reverse_lazy("bots:bot-telegram")
        my_bot_url = f"https://{settings.HOST}{my_bot_path}"
        tg_response = requests.post(api_url, data={"url": my_bot_url})

        return HttpResponse(
            content=json.dumps(tg_response.json()), content_type="application/json"
        )
