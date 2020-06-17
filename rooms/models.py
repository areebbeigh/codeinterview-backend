import json
import uuid
import calendar

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from jsonfield import JSONField


class LogEntry(models.Model):
    class EntryType:
        USER_JOIN = 'UJ'
        USER_LEAVE = 'UL'
        USER_RUN = 'UR'
        USER_MSG = 'UM'
        USER_JOIN_CALL = 'UJC'
        USER_LEAVE_CALL = 'ULC'
        LOG_MSG = 'LM'
        CODE_OUTPUT = 'CO'

    types = [
        (EntryType.USER_JOIN, 'User Join'),
        (EntryType.USER_LEAVE, 'User Leave'),
        (EntryType.USER_RUN, 'User Run'),
        (EntryType.USER_MSG, 'User Message'),
        (EntryType.USER_JOIN_CALL, 'User Join Call'),
        (EntryType.USER_LEAVE_CALL, 'User Leave Call'),
        (EntryType.LOG_MSG, 'Log Message'),
        (EntryType.CODE_OUTPUT, 'Code Output'),
    ]

    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=types)
    author_name = models.CharField(max_length=20, blank=True)
    content = models.TextField(editable=False, max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Entry ({self.id})'

    @property
    def timestamp(self):
        """UTC timestamp of self.created datetime.datetime field"""
        return calendar.timegm(self.created.utctimetuple())

    def to_dict(self):
        rv = {
            'timestamp': self.timestamp,
            'type': self.type,
            'author': self.author_name,
        }
        if self.type == self.EntryType.CODE_OUTPUT:
            rv['content'] = json.loads(self.content)
        else:
            rv['content'] = self.content
        return rv


class Room(models.Model):
    room_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # Since we're not concerned about user authentication, we'll just store member IDs
    # in a JSONField for every room
    # metadata = JSONField()
    participants = models.IntegerField(default=0, auto_created=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Room ({self.room_id})'

    def get_logs(self):
        return LogEntry.objects.filter(room__room_id=self.room_id)


class RunRequest(models.Model):
    class RequestStatus:
        QUEUED = 'QD'
        ERROR = 'ER'
        COMPLETED = 'CP'

    status_types = [
        (RequestStatus.QUEUED, 'Queued'),
        (RequestStatus.COMPLETED, 'Completed'),
        (RequestStatus.ERROR, 'Error'),
    ]
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
    celery_task_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=3,
                              choices=status_types,
                              default=RequestStatus.QUEUED)
    language = models.ForeignKey('Language', on_delete=models.DO_NOTHING)
    code = models.TextField()
    stdin = models.TextField(blank=True)
    output = models.TextField(blank=True)
    error = models.TextField(blank=True)
    exec_time = models.FloatField(null=True, verbose_name='Execution time')
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'RunRequest ({self.id})'


class Language(models.Model):
    name = models.CharField(verbose_name='Display Name', max_length=50)
    code = models.CharField(verbose_name='Language code',
                            max_length=50,
                            db_index=True)
    template = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.name} ({self.code})'