from django.shortcuts import render
from models import ImagerProfile
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required


class ProfileDetailView(DetailView):
    model = ImagerProfile

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        if context['object'].user.pk != self.request.user.id:

            pass
        return context
