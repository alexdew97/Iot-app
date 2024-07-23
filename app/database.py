from peewee_async import Manager, PostgresqlDatabase
import os

# Налаштування бази даних PostgreSQL
database = PostgresqlDatabase(
    'iot_devices',
    user='iot_user',
    password='yourpassword',
    host=os.getenv('DB_HOST', 'localhost'),
    port=5432
)

# Налаштування асинхронного менеджера
objects = Manager(database)