from peewee_async import Manager, PostgresqlDatabase
import os

# Налаштування бази даних PostgreSQL
database = PostgresqlDatabase(
    os.getenv('DB_NAME', 'iot_devices'),
    user=os.getenv('DB_USER', 'iot_user'),
    password=os.getenv('DB_PASS', 'yourpassword'),
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', 5432))
)

# Налаштування асинхронного менеджера
objects = Manager(database)

# Обов'язкове підключення aiopg
import aiopg  # це потрібно, щоб переконатися, що aiopg встановено і доступно


