import boto3
from loguru import logger
from config import (
    S3_ENDPOINT,
    S3_BUCKET,
    S3_ACCESS_KEY_ID,
    S3_SECRET_ACCESS_KEY,
    S3_REGION,
)
import uuid

session = boto3.session.Session()

s3 = session.client(
    service_name="s3",
    region_name=S3_REGION,
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
)

def upload_file(file_path: str, prefix: str = "uploads/") -> str:
    """
    Загружает файл в S3 и возвращает публичный URL
    """
    file_key = f"{prefix}{uuid.uuid4()}.jpg"
    logger.debug(f"Начало загрузки файла в S3: {file_key}")
    try:
        s3.upload_file(file_path, S3_BUCKET, file_key, ExtraArgs={"ACL": "public-read"})
        url = f"{S3_ENDPOINT}/{S3_BUCKET}/{file_key}"
        logger.success(f"Файл успешно загружен в S3: {url}")
        return url
    except Exception as e:
        logger.error(f"Ошибка загрузки файла в S3: {e}")
        raise