from decouple import config

db_name = config("DB_NAME")
db_user = config("DB_USER")
db_password = config("DB_PASSWORD")
db_host = config("DB_HOST")
db_port = int(config("DB_PORT"))

secret_key = config("SECRET_KEY")

front_url = config("FRONT_URL")

smtp_server = config("SMTP_SERVER")
email_address = config("EMAIL_ADDRESS")
email_password = config("EMAIL_PASSWORD")