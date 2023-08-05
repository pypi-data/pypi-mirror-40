from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)


class MediaFilePermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # If user is the owner allow everything.
        if obj.owner == request.user:
            return True
        perm = obj.shared_with.through.objects.filter(
            user=request.user, image=obj)
        if not perm:
            # If no other permission return false
            return False
        else:
            perm_obj = perm[0]
            if perm_obj.permission == 'v':
                # Allow only to view
                if request.method in permissions.SAFE_METHODS:
                    return True
                else:
                    return False
            else:
                # allow to do everything.
                return True
