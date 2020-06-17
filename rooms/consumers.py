import json
from urllib.parse import parse_qsl
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder

from asgiref.sync import async_to_sync
from colorama import Fore, Back, Style
from channels.generic.websocket import JsonWebsocketConsumer

from rooms.models import Room, LogEntry, RunRequest, Language

LogEntryType = LogEntry.EntryType


class RoomConsumer(JsonWebsocketConsumer):
    # WebSocket event handlers

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_exists = Room.objects.filter(room_id=self.room_id).exists()
        self.group_name = f'room_{self.room_id}'

        if not self.room_exists:
            self.close()
            return

        self.query = dict(parse_qsl(
            self.scope['query_string'].decode('utf-8')))
        self.username = self.query['username'].strip()

        async_to_sync(self.channel_layer.group_add)(self.group_name,
                                                    self.channel_name)
        self.accept()
        # send user pre-join room logs
        self.get_logs(None)
        self.create_log_entry(f'{self.username} joined the room',
                              LogEntryType.USER_JOIN)
        with transaction.atomic():
            room = self.room_object_locked()
            room.participants += 1
            room.save()

    def receive_json(self, content):
        command = content.get('command', None)
        handler = self.get_handler(command)
        if handler:
            try:
                return handler(content)
            except Exception as e:
                self.send_json({
                    'type': 'event',
                    'event': 'error',
                    'data': f'[{e.__class__.__name__}] {e}'
                })
                return
        self.send_json({
            'type': 'event',
            'event': 'error',
            'data': 'Command not found.'
        })

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name,
                                                        self.channel_name)
        # This won't be called if the server just crashed or restarted.
        # TODO: Should this be in __del__() instead?
        if self.room_exists:
            self.create_log_entry(f'{self.username} left the room',
                                  LogEntryType.USER_LEAVE)
            with transaction.atomic():
                room = self.room_object_locked()
                room.participants -= 1
                room.save()

    # ORM helper methods

    def create_log_entry(self, content, type, announce=True):
        entry = LogEntry(room=self.room_object,
                         type=type,
                         author_name=self.username,
                         content=content)
        entry.save()
        if announce:
            async_to_sync(self.channel_layer.group_send)(self.group_name, {
                'type': 'event.log.entry',
                'entry': entry.to_dict(),
            })
        return entry

    def room_object_locked(self):
        return Room.objects.select_for_update().get(room_id=self.room_id)

    @property
    def room_object(self):
        return Room.objects.get(room_id=self.room_id)

    def create_run_request(self, language, code, stdin, create_entry=True):
        try:
            language = Language.objects.get(code=language)
        except Language.DoesNotExist:
            raise Exception('Unsupported language')
        request = RunRequest(room=self.room_object,
                             language=language,
                             code=code,
                             stdin=stdin)
        request.save()

        if create_entry:
            self.create_log_entry(
                f'{self.username} made a run request', LogEntryType.USER_RUN)

    # Command handlers

    def get_handler(self, command):
        handlers = {
            'get-logs': self.get_logs,
            'send-message': self.send_message,
            'run': self.run,
            'join-call': self.join_call,
            'leave-call': self.leave_call,
        }
        return handlers.get(command)

    def get_logs(self, data):
        entries = [
            entry.to_dict() for entry in self.room_object.get_logs()
        ]
        response = {
            'type': 'event',
            'event': 'logs',
            'data': entries,
        }
        self.send_json(response)

    def send_message(self, data):
        message = data['message'].strip()
        self.create_log_entry(message, type=LogEntryType.USER_MSG)

    def run(self, data):
        self.create_run_request(data['language'], data['code'], data['stdin'])

    def join_call(self, data):
        message = f'{self.username} joined the video call'
        self.create_log_entry(message, type=LogEntryType.USER_JOIN_CALL)

    def leave_call(self, data):
        message = f'{self.username} left the video call'
        self.create_log_entry(message, type=LogEntryType.USER_LEAVE_CALL)

    # Event handlers

    def event_log_entry(self, event):
        entry = event['entry']
        if isinstance(entry, LogEntry):
            entry = entry.to_dict()
        self.send_json({
            'type': 'event',
            'event': 'new-entry',
            'data': entry,
        })

    # Helper methods

    @classmethod
    def encode_json(cls, obj):
        return json.dumps(obj, cls=DjangoJSONEncoder)
