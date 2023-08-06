from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications_received')
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications_sent')
    object = models.URLField()
    type = models.CharField(max_length=255)
    summary = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField()
    class Meta:
        rdf_type = 'sib:source'
        permissions = (
            ('view_notification', 'Read'),
            ('control_notification', 'Control'),
        )
        auto_author = 'author_user'
        ordering = ['date']

    def __str__(self):
        return '{}'.format(self.type)
