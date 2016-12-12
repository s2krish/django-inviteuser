from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from .conf import settings

# from braces.views import LoginRequiredMixin

from .models import Invitation
# from .app_settings import app_settings
from .adapters import get_invitations_adapter


class AcceptInvite(TemplateView):
    def get(self, request, *args, **kwargs):
        self.object = invitation = self.get_object()

        # No invitation was found.
        if not invitation:
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'inviteuser/messages/invite_invalid.txt')
            return redirect(settings.INVITATIONS_ERROR_REDIRECT)

        # The invitation was previously accepted, redirect to the login
        # view.
        if invitation.accepted:
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'inviteuser/messages/invite_already_accepted.txt',
                {'email': invitation.email})
            return redirect(settings.INVITATIONS_ERROR_REDIRECT)

        # The key was expired.
        if invitation.key_expired():
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'inviteuser/messages/invite_expired.txt',
                {'email': invitation.email})
            return redirect(settings.INVITATIONS_ACCEPT_ERROR_REDIRECT)

        # The invitation is valid, Save invitation
        get_invitations_adapter().set_invitation(self.request, invitation.id)

        if request.user.is_authenticated:
            url = settings.INVITATIONS_AUTH_USER_REDIRECT
        else:
            # Save invitation
            url = settings.INVITATIONS_ACCEPT_REDIRECT

            if settings.INVITATIONS_ACCEPT_REDIRECT == settings.LOGIN_URL:
                url = '%s?next=%s' % (url, settings.INVITATIONS_AUTH_USER_REDIRECT)

        return redirect(url)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except Invitation.DoesNotExist:
            return None

    def get_queryset(self):
        return Invitation.objects.all()


class AcceptErrorView(TemplateView):
    template_name = 'inviteuser/invite_error.html'
