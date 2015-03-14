from django import forms
from django.forms import ModelForm
from django.db import models
from imager_images.models import Photo, Album
from profiles.models import ImagerProfile


class PhotoForm(ModelForm):

    class Meta:
        model = Photo
        exclude = []


class AlbumForm(ModelForm):

    class Meta:
        model = Album
        fields = ['title', 'description', 'photos', 'cover_photo']

    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        profile = ImagerProfile.objects.get(user=self.initial['user'])
        self.fields['photos'].queryset = Photo.objects.filter(profile=profile)
        self.fields['cover_photo'].queryset = Photo.objects.filter(profile=profile)


class ProfileForm(ModelForm):
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email = forms.EmailField(label='Email', required=False)

    class Meta:
        model = ImagerProfile
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        obj = super(ProfileForm, self).save(*args, **kwargs)
        obj.user.first_name = self.data['first_name']
        obj.user.last_name = self.data['last_name']
        obj.user.email = self.data['email']
        obj.user.save()
        return obj