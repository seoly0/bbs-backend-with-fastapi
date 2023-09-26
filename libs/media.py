from urllib.parse import urljoin

from minio import Minio

from settings import ENV


def is_image_type(type):
    return type.split("/")[0] == "image"


def save(path: str, file, content_type=None):
    try:
        client = Minio(f"{ENV.MINIO_HOST}:{ENV.MINIO_PORT}", ENV.MINIO_USER, ENV.MINIO_PASSWORD, secure=False)

        response = client.fput_object(
            "bbs",
            path,
            file,
            content_type=content_type
        )

        return urljoin(base=ENV.MEDIA_HOST, url=f"{response.bucket_name}/{response.object_name}")

    except Exception:
        return None


# TODO boto3로 poc
