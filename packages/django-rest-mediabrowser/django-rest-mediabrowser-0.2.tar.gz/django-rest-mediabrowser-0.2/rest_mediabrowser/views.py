from django.shortcuts import render
from private_storage.views import PrivateStorageDetailView
from django.utils.module_loading import import_string
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from . import appconfig
from .models import *
from .serializers import *
from .permissions import *
# Create your views here.
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class MediaStorageImageView(PrivateStorageDetailView):
    storage = appconfig.MB_STORAGE
    can_access_file = staticmethod(import_string(
        appconfig.MEDIA_BROWSER_AUTH_FUNCTION))
    model = MediaImage
    model_file_field = 'image'


class MediaStorageFileView(PrivateStorageDetailView):
    storage = appconfig.MB_STORAGE
    can_access_file = staticmethod(import_string(
        appconfig.MEDIA_BROWSER_AUTH_FUNCTION))
    model = MediaFile
    model_file_field = 'file'


class CollectionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, CollectionPermission, )
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)


class SharedCollectionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, CollectionPermission, )
    queryset = Collection.objects.all()
    serializer_class = SharedCollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user:
            return self.request.user.shared_collections.all()
        else:
            return Collection.objects.none()


class MediaImageViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, MediaImagePermission, )
    queryset = MediaImage.objects.all()
    serializer_class = MediaImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return MediaImage.objects.filter(owner=self.request.user)


class MediaFileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, MediaFilePermission, )
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return MediaFile.objects.filter(owner=self.request.user)


class SharedMediaImageViewSet(mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    queryset = MediaImage.objects.all()
    serializer_class = SharedMediaImageSerializer
    permission_classes = (IsAuthenticated, MediaImagePermission, )

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user:
            return self.request.user.shared_images.all()
        else:
            return MediaImage.objects.none()


class SharedMediaFileViewSet(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, MediaImagePermission, )
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        if self.request.user:
            return self.request.user.shared_files.all()
        else:
            return MediaFile.objects.none()
