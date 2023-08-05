import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def default_auth(private_file):
    parent = private_file.parent_object
    user = private_file.request.user
    if parent.published:
        return True
    if not user.is_authenticated:
        return False
    if user == parent.owner:
        return True
    if parent.shared_with.filter(pk=user.pk).exists():
        return True
    if parent.collection:
        if parent.collection.owner == user:
            return True
        if parent.collection.shared_with.filter(pk=user.pk).exists():
            return True
    return False
