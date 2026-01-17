import logging
import uuid

import boto3  # type: ignore
from botocore.exceptions import BotoCoreError, ClientError  # type: ignore

from app.core.config import settings

logger = logging.getLogger(__name__)


def upload_image(file_name: str) -> str:
    """
    Upload an image to AWS S3 and return its URL.
    :param file_name: The name of the file to upload.
    :return: The URL of the uploaded image.
    :raises ValueError: If the upload fails.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    try:
        unique_name = f"{uuid.uuid4()}-{file_name}"

        # s3_client.upload_file(file_path, settings.AWS_S3_BUCKET, unique_name)

        image_url = (
            f"https://{settings.AWS_S3_BUCKET}.s3."
            f"{settings.AWS_REGION}.amazonaws.com/{unique_name}"
        )

        return image_url

    except (BotoCoreError, ClientError) as e:
        logger.error("S3 upload failed: %s", e)
        raise ValueError("Failed to upload image to S3") from e
