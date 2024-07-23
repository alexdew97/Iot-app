from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from app.main import app
from app.models import ApiUser, Location, Device
from app.database import database, objects

class MyAppTestCase(AioHTTPTestCase):
    async def get_application(self):
        # Підключення до тестової бази даних
        self.database = database
        self.database.init('iot_devices_test', user='iot_user', password='yourpassword', host='localhost', port=5432)
        self.objects = objects

        # Створення таблиць для тестів
        self.database.connect()
        self.database.create_tables([ApiUser, Location, Device])
        self.database.close()

        return app

    def tearDown(self):
        # Видалення таблиць після тестів
        self.database.connect()
        self.database.drop_tables([ApiUser, Location, Device])
        self.database.close()

    @unittest_run_loop
    async def test_add_user(self):
        payload = {'name': 'Test User', 'email': 'test@example.com', 'password': 'testpassword'}
        resp = await self.client.post('/users', json=payload)
        assert resp.status == 200
        text = await resp.json()
        assert 'user_id' in text

    @unittest_run_loop
    async def test_add_location(self):
        payload = {'name': 'Test Location'}
        resp = await self.client.post('/locations', json=payload)
        assert resp.status == 200
        text = await resp.json()
        assert 'location_id' in text

    @unittest_run_loop
    async def test_add_device(self):
        user_payload = {'name': 'Test User', 'email': 'test@example.com', 'password': 'testpassword'}
        location_payload = {'name': 'Test Location'}
        user_resp = await self.client.post('/users', json=user_payload)
        user_data = await user_resp.json()
        user_id = user_data['user_id']
        location_resp = await self.client.post('/locations', json=location_payload)
        location_data = await location_resp.json()
        location_id = location_data['location_id']
        device_payload = {'name': 'Test Device', 'type': 'Test Type', 'login': 'testlogin', 'password': 'testpassword', 'location_id': location_id, 'api_user_id': user_id}
        resp = await self.client.post('/devices', json=device_payload)
        assert resp.status == 200
        text = await resp.json()
        assert 'device_id' in text

    @unittest_run_loop
    async def test_get_devices(self):
        user_payload = {'name': 'Test User', 'email': 'test@example.com', 'password': 'testpassword'}
        location_payload = {'name': 'Test Location'}
        user_resp = await self.client.post('/users', json=user_payload)
        user_data = await user_resp.json()
        user_id = user_data['user_id']
        location_resp = await self.client.post('/locations', json=location_payload)
        location_data = await location_resp.json()
        location_id = location_data['location_id']
        device_payload = {'name': 'Test Device', 'type': 'Test Type', 'login': 'testlogin', 'password': 'testpassword', 'location_id': location_id, 'api_user_id': user_id}
        await self.client.post('/devices', json=device_payload)
        resp = await self.client.get('/devices')
        assert resp.status == 200
        text = await resp.json()
        assert 'devices' in text

    @unittest_run_loop
    async def test_update_device(self):
        user_payload = {'name': 'Test User', 'email': 'test@example.com', 'password': 'testpassword'}
        location_payload = {'name': 'Test Location'}
        user_resp = await self.client.post('/users', json=user_payload)
        user_data = await user_resp.json()
        user_id = user_data['user_id']
        location_resp = await self.client.post('/locations', json=location_payload)
        location_data = await location_resp.json()
        location_id = location_data['location_id']
        device_payload = {'name': 'Test Device', 'type': 'Test Type', 'login': 'testlogin', 'password': 'testpassword', 'location_id': location_id, 'api_user_id': user_id}
        device_resp = await self.client.post('/devices', json=device_payload)
        device_data = await device_resp.json()
        device_id = device_data['device_id']
        update_payload = {'name': 'Updated Device'}
        resp = await self.client.put(f'/devices/{device_id}', json=update_payload)
        assert resp.status == 200
        text = await resp.json()
        assert text['message'] == 'Device updated successfully!'

    @unittest_run_loop
    async def test_delete_device(self):
        user_payload = {'name': 'Test User', 'email': 'test@example.com', 'password': 'testpassword'}
        location_payload = {'name': 'Test Location'}
        user_resp = await self.client.post('/users', json=user_payload)
        user_data = await user_resp.json()
        user_id = user_data['user_id']
        location_resp = await self.client.post('/locations', json=location_payload)
        location_data = await location_resp.json()
        location_id = location_data['location_id']
        device_payload = {'name': 'Test Device', 'type': 'Test Type', 'login': 'testlogin', 'password': 'testpassword', 'location_id': location_id, 'api_user_id': user_id}
        device_resp = await self.client.post('/devices', json=device_payload)
        device_data = await device_resp.json()
        device_id = device_data['device_id']
        resp = await self.client.delete(f'/devices/{device_id}')
        assert resp.status == 200
        text = await resp.json()
        assert text['message'] == 'Device deleted successfully!'