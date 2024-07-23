import logging
from aiohttp import web
from app.models import ApiUser, Location, Device
from app.database import objects

logger = logging.getLogger(__name__)

async def add_user(request):
    try:
        data = await request.json()
        new_user = await objects.create(ApiUser, **data)
        logger.info(f"Added new user with ID: {new_user.id}")
        return web.json_response({'message': 'User added successfully!', 'user_id': new_user.id})
    except Exception as e:
        logger.error(f"Error adding user: {e}")
        return web.json_response({'message': 'Failed to add user'}, status=500)

async def add_location(request):
    try:
        data = await request.json()
        new_location = await objects.create(Location, **data)
        logger.info(f"Added new location with ID: {new_location.id}")
        return web.json_response({'message': 'Location added successfully!', 'location_id': new_location.id})
    except Exception as e:
        logger.error(f"Error adding location: {e}")
        return web.json_response({'message': 'Failed to add location'}, status=500)

async def add_device(request):
    try:
        data = await request.json()
        new_device = await objects.create(Device, **data)
        logger.info(f"Added new device with ID: {new_device.id}")
        return web.json_response({'message': 'Device added successfully!', 'device_id': new_device.id})
    except Exception as e:
        logger.error(f"Error adding device: {e}")
        return web.json_response({'message': 'Failed to add device'}, status=500)

async def get_devices(request):
    try:
        devices = await objects.execute(Device.select())
        output = [device.__data__ for device in devices]
        logger.info("Fetched all devices")
        return web.json_response({'devices': output})
    except Exception as e:
        logger.error(f"Error fetching devices: {e}")
        return web.json_response({'message': 'Failed to fetch devices'}, status=500)

async def get_device(request):
    try:
        device_id = int(request.match_info['id'])
        device = await objects.get(Device, Device.id == device_id)
        logger.info(f"Fetched device with ID: {device_id}")
        return web.json_response(device.__data__)
    except Exception as e:
        logger.error(f"Error fetching device with ID {device_id}: {e}")
        return web.json_response({'message': f'Failed to fetch device with ID {device_id}'}, status=500)

async def update_device(request):
    try:
        device_id = int(request.match_info['id'])
        device = await objects.get(Device, Device.id == device_id)
        data = await request.json()
        for key, value in data.items():
            setattr(device, key, value)
        await objects.update(device)
        logger.info(f"Updated device with ID: {device_id}")
        return web.json_response({'message': 'Device updated successfully!'})
    except Exception as e:
        logger.error(f"Error updating device with ID {device_id}: {e}")
        return web.json_response({'message': f'Failed to update device with ID {device_id}'}, status=500)

async def delete_device(request):
    try:
        device_id = int(request.match_info['id'])
        device = await objects.get(Device, Device.id == device_id)
        await objects.delete(device)
        logger.info(f"Deleted device with ID: {device_id}")
        return web.json_response({'message': 'Device deleted successfully!'})
    except Exception as e:
        logger.error(f"Error deleting device with ID {device_id}: {e}")
        return web.json_response({'message': f'Failed to delete device with ID {device_id}'}, status=500)