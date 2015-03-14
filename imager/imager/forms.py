from django.forms import ModelForm
from imager_images.models import Photo
from profiles.models import ImagerProfile


class PhotoForm(ModelForm):

    class Meta:
        model = Photo
        exclude = ['profile']
