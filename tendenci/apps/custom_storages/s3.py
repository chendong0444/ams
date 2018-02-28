from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

from s3_folder_storage.s3 import DefaultStorage, StaticStorage

class ThemeStorage(S3Boto3Storage):
    """
    Storage for uploaded theme files.
    The folder is defined in settings.THEME_S3_PATH
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = settings.THEME_S3_PATH
        super(DefaultStorage, self).__init__(*args, **kwargs)
