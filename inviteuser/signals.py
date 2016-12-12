from django.dispatch import Signal

invite_url_sent = Signal(providing_args=['invite_url_sent'])
invite_accepted = Signal(providing_args=['accepted_email'])

"""
@receiver(invite_url_sent, sender=Invitation)
def invite_url_sent(sender, instance, invite_url_sent, **kwargs):
    pass

@receiver(invite_accepted, sender=auth.models.AnonymousUser)
def invite_accepted(sender, instance, accepted_email, **kwargs):
    pass
"""
