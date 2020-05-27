import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from celery import shared_task
from rooms.models import RunRequest, LogEntry

RequestStatus = RunRequest.RequestStatus
LogEntryType = LogEntry.EntryType


@shared_task
def save_run_output(result, request_id):
    request = RunRequest.objects.get(id=request_id)

    if result['error']:
        request.error = result['error_msg']
        request.status = RequestStatus.ERROR
    else:
        request.status = RequestStatus.COMPLETED

    request.output = result['output']
    try:
        request.exec_time = float(result['exec_time'])
    except ValueError:
        pass
    except TypeError:
        pass
    request.save()

    entry = LogEntry(room=request.room,
                     type=LogEntryType.CODE_OUTPUT,
                     author_name='',
                     content=json.dumps({
                         'request_id': request.id,
                         'error': request.error,
                         'status': request.status,
                         'output': request.output,
                         'exec_time': request.exec_time,
                     }))
    entry.save()

    # announce new log entry to associated room
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'room_{request.room.room_id}',
        {
            'type': 'event.log.entry',
            'entry': entry.to_dict(),
        },
    )