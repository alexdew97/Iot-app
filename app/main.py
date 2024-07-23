import logging
from aiohttp import web
from app.routes import add_user, add_location, add_device, get_devices, get_device, update_device, delete_device

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = web.Application()

# Налаштування маршрутів
app.add_routes([
    web.post('/users', add_user),
    web.post('/locations', add_location),
    web.post('/devices', add_device),
    web.get('/devices', get_devices),
    web.get('/devices/{id}', get_device),
    web.put('/devices/{id}', update_device),
    web.delete('/devices/{id}', delete_device)
])

if __name__ == "__main__":
    web.run_app(app)