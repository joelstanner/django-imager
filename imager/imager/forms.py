from django.forms import ModelForm
from imager_images.models import Photo, Album
from profiles.models import ImagerProfile


class PhotoForm(ModelForm):

    class Meta:
        model = Photo


class AlbumForm(ModelForm):

    class Meta:
        model = Album
        fields = ['title', 'description', 'photos', 'cover_photo']
        
    def __init__(self, *args, **kwargs):
        super(AlbumForm, self).__init__(*args, **kwargs)
        profile = ImagerProfile.objects.get(user=self.initial['user'])
        self.fields['photos'].queryset = Photo.objects.filter(profile=profile)
        self.fields['cover_photo'].queryset = Photo.objects.filter(profile=profile)