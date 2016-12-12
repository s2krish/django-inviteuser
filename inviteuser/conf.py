from appconf import AppConf
from django.conf import settings


class InvitationsConf(AppConf):
    EXPIRY = 3
    """How long before the invitation expires"""

    ACCEPT_REDIRECT = settings.LOGIN_URL
    """Where to redirect if invitation is valid/accepted"""

    AUTH_USER_REDIRECT = '/'
    """Where to redirect authenticated (loged in) user
    """

    ERROR_REDIRECT = 'invitations:accept-invite-error'
    """ Where to redirect if invitation is invalid/error """

    ADAPTER = 'invitations.adapters.BaseInvitationsAdapter'
    """ The adapter, setting ACCOUNT_ADAPTER overrides this default """

    class Meta:
        prefix = 'INVITATIONS'
        proxy = True
