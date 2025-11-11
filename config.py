from decouple import config

BOT_TOKEN = config("BOT_TOKEN")

DATABASE_URL = config(
    "DATABASE_URL",
    default="postgresql://postgres:postgres@localhost:5432/expenses_db"
)

S3_ENDPOINT = config("S3_ENDPOINT")
S3_BUCKET = config("S3_BUCKET")
S3_ACCESS_KEY_ID = config("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = config("S3_SECRET_ACCESS_KEY")
S3_REGION = config("S3_REGION", default="ru-central1")