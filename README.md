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
