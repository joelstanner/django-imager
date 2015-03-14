from django.forms import ModelForm
from imager_images.models import Photo, Album
from profiles.models import ImagerProfile


class PhotoForm(ModelForm):

    class Meta:
        model = Photo


class AlbumForm(ModelForm):

    class Meta:
        model = Album

    def __init__(self, *args, **kwargs):
        print "hello"
        super(AlbumForm, self).__init__(args, kwargs)