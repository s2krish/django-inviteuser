import datetime
import json

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

from .managers import InvitationManager
from .conf import settings
from .adapters import get_invitations_adapter
from . import signals


@python_2_unicode_compatible
class Invitation(models.Model):

    email = models.EmailField(verbose_name=_('e-mail address'),
                              max_length=254)
    accepted = models.BooleanField(verbose_name=_('accepted'), default=False)
    created = models.DateTimeField(verbose_name=_('created'),
                                   default=timezone.now)
    key = models.CharField(verbose_name=_('key'), max_length=64, unique=True)
    sent = models.DateTimeField(verbose_name=_('sent'), null=True)
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True)
    params = models.TextField(blank=True)

    objects = InvitationManager()

    def __str__(self):
        return "Invite: {0}".format(self.email)

    @classmethod
    def create(cls, email, inviter=None):
        key = get_random_string(64).lower()
        instance, _ = cls._default_manager.get_or_create(
            email=email,
            key=key,
            inviter=inviter)
        return instance

    def key_expired(self):
        expiration_date = (
            self.sent + datetime.timedelta(
                days=settings.INVITATIONS_EXPIRY))
        return expiration_date <= timezone.now()

    def _get_corrent_site(self, **kwargs):
        current_site = (kwargs['site'] if 'site' in kwargs
                        else Site.objects.get_current())
        return current_site

    def send_invitation(self, request, **kwargs):
        current_site = self._get_corrent_site(**kwargs)
        invite_url = reverse('invitations:accept-invite',
                             args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)

        ctx = RequestContext(request, {
            'invite_url': invite_url,
            'site_name': current_site.name,
            'email': self.email,
            'key': self.key,
            'inviter': self.inviter,
        })

        ctx.update(kwargs)

        email_template = 'invitations/email/email_invite'

        get_invitations_adapter().send_mail(
            email_template,
            self.email,
            ctx)
        self.sent = timezone.now()
        self.params = json.dumps({k: str(v) for k, v in kwargs.iteritems()})
        self.save()

        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            invite_url_sent=invite_url)

    def accept(self, request, accepted_email, **kwargs):
        '''Accept the invitation

        :param request: Request object
        :param accepted_email: The email address used to signup/accept by user.
                               It can be different from email where invitaiton
                               was sent.
        :param kwargs: Keyword arguments

        '''
        self.accepted = True
        self.save()

        current_site = self._get_corrent_site(**kwargs)
        invite_url = reverse('invitations:accept-invite',
                             args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)

        ctx = RequestContext(request, {
            'invite_url': invite_url,
            'site_name': current_site.name,
            'email': self.email,
            'accepted_email': accepted_email,
            'inviter': self.inviter
        })

        ctx.update(kwargs)

        email_template = 'invitations/email/email_accept'

        get_invitations_adapter().send_mail(
            email_template,
            self.inviter.email,
            ctx)

        # send signal
        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            accepted_email=accepted_email)

        get_invitations_adapter().unset_invitation(request)


    def cancel(self, request):
        get_invitations_adapter().unset_invitation(request)
