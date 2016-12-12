from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.db.models import Q

from .conf import settings


class InvitationManager(models.Manager):

    def all_expired(self):
        return self.filter(self.expired_q())

    def all_valid(self):
        return self.exclude(self.expired_q())

    def get_or_create(self, **kwargs):
        objects = self.filter(
            email=kwargs.get('email'),
            inviter=kwargs.get('inviter'),
            accepted=False)
        if objects:
            obj = objects.first()
            created = True
        else:
            obj = self.create(**kwargs)
            created = False

        return obj, created

    def expired_q(self):
        sent_threshold = timezone.now() - timedelta(
            days=settings.INVITATION_EXPIRY)
        q = Q(accepted=True) | Q(sent__lt=sent_threshold)
        return q

    def delete_expired_confirmations(self):
        self.all_expired().delete()
