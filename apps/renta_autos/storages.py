from storages.backends.s3boto3 import S3Boto3Storage


class RentaAutoClientsAvatarDNIStorage(S3Boto3Storage):
   location = 'media'
   default_acl = 'private'
   file_overwrite = True