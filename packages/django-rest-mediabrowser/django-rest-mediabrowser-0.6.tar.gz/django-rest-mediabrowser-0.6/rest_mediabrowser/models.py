from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from .appconfig import MB_STORAGE
# Create your models here.


PERMISSION_LEVELS = (('e', 'Edit'),
                     ('v', 'View'),)


def image_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/images/{1}'.format(instance.owner.id, filename)


def file_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/files/{1}'.format(instance.owner.id, filename)


class Collection(models.Model):
    """
    A collection to share in with ease
    """
    name = models.CharField(_("name"), max_length=500)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=_("user"),
                              related_name="collections",
                              on_delete=models.CASCADE)

    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(
        "shared_with"), related_name="shared_collections", through="rest_mediabrowser.CollectionPermission")

    def __str__(self):
        return f'{self.name}'


class MediaImage(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=_("owner"),
                              related_name="media_images",
                              on_delete=models.CASCADE)
    collection = models.ForeignKey("rest_mediabrowser.Collection",
                                   verbose_name=_("collection"),
                                   related_name="image_files",
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    tags = TaggableManager(blank=True)
    description = models.CharField(
        _("description"), max_length=500, blank=True)
    alt_text = models.CharField(
        _("alternative text"), max_length=100, blank=True)
    height = models.IntegerField(_("height"), blank=True, null=True)
    width = models.IntegerField(_("width"), blank=True, null=True)
    image = models.ImageField(_("image"), upload_to=image_upload_path,
                              height_field='height', width_field='width', max_length=500, storage=MB_STORAGE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(
        "shared_with"), related_name="shared_images", through="rest_mediabrowser.ImagePermission")
    published = models.BooleanField(_("Status"), default=False)

    def __str__(self):
        return f'{self.id}-{self.description}'


class MediaFile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=_("owner"),
                              related_name="media_files",
                              on_delete=models.CASCADE)
    collection = models.ForeignKey("rest_mediabrowser.Collection",
                                   verbose_name=_("collection"),
                                   related_name="media_files",
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    tags = TaggableManager()
    description = models.CharField(
        _("description"), max_length=500, blank=True)
    file = models.FileField(
        _("file"), upload_to=file_upload_path, max_length=500, storage=MB_STORAGE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(
        "shared_with"), related_name="shared_files", through="rest_mediabrowser.FilePermission")
    published = models.BooleanField(_("Status"), default=False)

    def __str__(self):
        return f'{self.id}-{self.description}'


class ImagePermission(models.Model):
    image = models.ForeignKey(
        "rest_mediabrowser.MediaImage", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    permission = models.CharField(
        _("permission"), max_length=2, choices=PERMISSION_LEVELS)\


    class Meta:
        unique_together = (("user", "image"),)


class FilePermission(models.Model):
    file = models.ForeignKey(
        "rest_mediabrowser.MediaFile", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    permission = models.CharField(
        _("permission"), max_length=2, choices=PERMISSION_LEVELS)

    class Meta:
        unique_together = (("user", "file"),)


class CollectionPermission(models.Model):
    collection = models.ForeignKey(
        "rest_mediabrowser.Collection", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    permission = models.CharField(
        _("permission"), max_length=2, choices=PERMISSION_LEVELS)

    class Meta:
        unique_together = (("user", "collection"),)
