import os
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
import boto3
import botocore


from PIL import Image


BASE_DIR = settings.BASE_DIR


# Initializate s3 Bucker
if settings.DEBUG == False:
	s3 = boto3.resource(
	's3',
	aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
	aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
	)

	bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)

def get_file_obj(path, format, file_type='img'):
	buffer = BytesIO()


	if settings.DEBUG:
		file_path = os.path.join(BASE_DIR, path)
		if os.path.exists(file_path):
			if file_type == 'img':
				file_obj = Image.open(file_path)

	else:
		try:
			s3.Object(settings.AWS_STORAGE_BUCKET_NAME, path).load()
		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == '404':
				print("Don't found path for that avatar")
				pass
			else:
				print("Fatal error.")
				pass
		else:
			f_object = bucket.Object(path)
			object_as_streaming_body = f_object.get()["Body"]
			object_as_bytes = object_as_streaming_body.read()
			object_as_file_like = BytesIO(object_as_bytes)
			if file_type == 'img':
				file_obj = Image.open(object_as_file_like)


	file_obj.save(buffer, format=format)
	buffer.seek(0)
	if file_type == 'img':
		content_file = ContentFile(buffer.read())


	return content_file