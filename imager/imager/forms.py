from django.forms import ModelForm
from imager_images.models import Photo, Album
from profiles.models import ImagerProfile


class PhotoForm(ModelForm):

    class Meta:
        model = Photo


class AlbumForm(ModelForm):

    class Meta:
        model = Album
