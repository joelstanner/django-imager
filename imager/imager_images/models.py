from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import profiles


class RandomImage(models.Manager):
    def get_queryset(self):
        return super(RandomImage, self).get_queryset().filter(published='pb').order_by('?')


@python_2_unicode_compatible
class Album(models.Model):
    '''Represent an individual album of photos'''

    profile = models.ForeignKey(profiles.models.ImagerProfile,
                                related_name='album_set')
    photos = models.ManyToManyField('Photo',
                                    symmetrical=False,
                                    related_name='album_set',
                                    blank=True,
                                    null=True)

    title = models.CharField(max_length=256, default='No Title')
    description = models.TextField(default='No Description')

    cover = models.ImageField(blank=True, null=True)

    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(null=True)

    PUBLIC = 'pb'
    PRIVATE = 'pv'
    SHARED = 'sh'

    PUBLISHED_CHOICES = (
        (PUBLIC, 'public'),
        (PRIVATE, 'private'),
        (SHARED, 'shared')
    )

    published = models.CharField(max_length=2,
                                 choices=PUBLISHED_CHOICES,
                                 default='pv')

    def add_photo(self, photo):
        if photo.profile != self.profile:
            raise AttributeError()
        self.photos.add(photo)

    def designate_cover(self, photo):
        self.cover = photo.photo

    def show_photos(self):
        return self.photos.all()

    def __str__(self):
        return (
            'Album Title: ' + self.title +
            '\nOwned by: ' + self.profile.user.username
        )


@python_2_unicode_compatible
class Photo(models.Model):
    '''Represent an individual photo'''

    PUBLIC = 'pb'
    PRIVATE = 'pv'
    SHARED = 'sh'

    PUBLISHED_CHOICES = (
        (PUBLIC, 'public'),
        (PRIVATE, 'private'),
        (SHARED, 'shared')
    )

    profile = models.ForeignKey(profiles.models.ImagerProfile,
                                related_name='photo_set')

    album = models.ManyToManyField(Album,
                                   related_name='photo_set',
                                   blank=True,
                                   null=True)

    photo = models.ImageField(blank=True, null=True)

    title = models.CharField(max_length=256, default='No Title')
    description = models.TextField(default='No Description')

    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField(null=True)

    published = models.CharField(max_length=2,
                                 choices=PUBLISHED_CHOICES,
                                 default='pv')
    objects = models.Manager()
    random_image = RandomImage()

    def __str__(self):
        return (
            'Photo Title: ' + self.title +
            '\nOwned by: ' + self.profile.user.username
        )
