from django.shortcuts import render
from models import ImagerProfile
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required


class ProfileDetailView(DetailView):
    model = ImagerProfile

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        if context['object'].user.pk != self.request.user.pk:
            if context['object'].name_priv:
                context['object'].user.username = 'PRIVATE'
            if context['object'].picture_priv:
                context['object'].picture = '/media/kitty.jpg'
            if context['object'].phone_priv:
                context['object'].phone = 'PRIVATE'
            if context['object'].birthday_priv:
                context['object'].birthday = 'PRIVATE'
        return context
