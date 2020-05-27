from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from celery import current_app

from rooms.models import RunRequest
from rooms.tasks import save_run_output


@receiver(post_save, sender=RunRequest)
def dispatch_run_task(sender, instance, created, **kwargs):
    if created:
        res = current_app.send_task(
            'tasks.sandbox.run_user_code',
            (instance.language.code, instance.code, instance.stdin),
            chain=[
                # Without the .set() this request goes to the default queue
                # instead of the queue defined in settings. WHY?!
                save_run_output.s(instance.id).set(queue='callbacks')
            ])
        instance.celery_task_id = res.task_id
        instance.save()
