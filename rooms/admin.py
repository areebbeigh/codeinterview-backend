from django import forms
from django.contrib import admin

from rooms.wdigets import CodeEditor
from rooms.models import Room, LogEntry, RunRequest, Language


class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'room_uuid',
        'author_name',
        'type',
        'created',
    )
    readonly_fields = (
        'room_uuid',
        'author_name',
        'content',
        'created',
    )
    exclude = ('room', )
    ordering = ('-created', )

    def room_uuid(self, obj):
        if obj.room is None:
            return None
        return obj.room.room_id


class LanguageAdminForm(forms.ModelForm):
    model = Language

    class Meta:
        fields = '__all__'
        widgets = {
            'template': CodeEditor(),
        }


class LanguageAdmin(admin.ModelAdmin):
    form = LanguageAdminForm
    list_display = (
        'name',
        'code',
    )


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_id',
        'participants',
        'created',
    )
    readonly_fields = (
        'room_id',
        'participants',
        'created',
    )
    ordering = ('-participants', )


class RunRequestAdmin(admin.ModelAdmin):
    list_display = (
        'room_uuid',
        'status',
        'exec_time',
        'created',
    )
    readonly_fields = (
        'room',
        'celery_task_id',
        'status',
        'language',
        'code',
        'stdin',
        'output',
        'error',
        'exec_time',
        'created',
    )
    order = ('-created', )

    def room_uuid(self, obj):
        if obj.room is None:
            return None
        return obj.room.room_id


admin.site.register(Room, RoomAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(RunRequest, RunRequestAdmin)
admin.site.register(Language, LanguageAdmin)