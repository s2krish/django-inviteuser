'''
Module used for inviting user for registration. This is forked from
[bee-keeper/django-invitations](https://github.com/bee-keeper/django-invitations).

# General Concept/steps for inviting user
1. Sent invitation
2. User click invitation link and comes to site
3. For valid invitation, accept invitation and do whatever further.

## Some use case scenarion when user accept invitation

1. You may want to reward bonus for accepting user
2. You may want to assign speical group team to acceping user.

I have added few features:

1. Pass additional variable to `send_invitation` using `**kwargs`
2. Remove unique key for `email` field. This allow multiple inveter to send
   invitation to same email.
2. Save additional data in invitation table
3. Remove `SendInvite` and `SendInvite`. My main object was to makt this module
   as pure interface.


# Installation

```
pip install django-inviteuser

# Add to settings.py, INSTALLED_APPS
'inviteuser',

# Append to urls.py
url(r'^inviteuser/', include('inviteuser.urls', namespace='inviteuser')),
```

# Uses

```
import inviteuser

# Send invitation

inviteuser.invite(request, invitee_email, inviter, **kwargs):

# Get invitation. if user comes to site by valid invitation link
# This will return invitation object.

inviteuser.get(request)

# Acept invitation
inviteuser.accept(request, obj, accepted_email, **kwargs)

```

'''


def invite(request, invitee_email, inviter, **kwargs):
    '''Send the invitation

    :param reqeust: Django Request instance
    :param invitee_email: Email address where you want send invitation
    :param inviter: User object, inviter
    :param kwargs: Additional kwargs

    :return invitation: Invitation object
    '''

    from invitations.models import Invitation

    invitation = Invitation.create(invitee_email, inviter=inviter)
    invitation.send_invitation(request, **kwargs)

    return invitation


def accept(request, obj, accepted_email, **kwargs):
    '''Accept the invitation

    :param reqeust: Django Request instance
    :param obj: Invitation object (return by `invitations.get`)
    :param kwargs: Any variable that you want to include in conformation email
    '''
    return obj.accept(request, accepted_email, **kwargs)


def get(request):
    '''Returns invitation

    :param reqeust: Django Request instance

    :return invitation: Invitation object
    '''

    from invitations.models import Invitation
    from invitations.adapters import get_invitations_adapter

    invitation_id = get_invitations_adapter().get_invitation(request)

    obj = Invitation.objects.get(id=invitation_id)
    return obj


def unset(request):
    '''Unset invitation

    :param reqeust: Django Request instance
    '''
    from invitations.adapters import get_invitations_adapter
    get_invitations_adapter().unset_invitation(request)


def get_auth_user_redirect():
    '''Returns AUTH_USER_REDIRECT url

    :return reqeust: Redirect URL for authenticated user
    '''
    from .conf import settings
    return settings.INVITATIONS_AUTH_USER_REDIRECT


def set(request, invitation_id):
    '''Set invitation (rarely used)

    :param invitation_id: Invitation id
    '''
    from invitations.adapters import get_invitations_adapter
    get_invitations_adapter().set_invitation(request, invitation_id)
