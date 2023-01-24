from datetime import datetime
from timebank import app
import unittest
import json


# Funkcia pre login
def login_user(self, phone, password):
    tester = app.test_client(self)
    response = tester.post("/api/v1/user/login", json={
        'phone': phone,
        'password': password
    })
    return response


# Funkcia pre register
def register_user(self, phone, password, password_val, user_name):
    tester = app.test_client(self)
    response = tester.post("/api/v1/user-create", json={
        'phone': phone,
        'password': password,
        'password_val': password_val,
        'user_name': user_name
    })
    return response


# Testy
class Test(unittest.TestCase):
    def test0101(self):  # Vytvor user 1 so spravnymi udajmi
        response = register_user(self, "+421 900 000001", "test1", "test1", "Testinguser1")
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test0102(self):  # Overenie existencie user 1
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert res[0]['id'] == 1
        assert res[0]['phone'] == "+421 900 000001"
        assert res[0]['user_name'] == "Testinguser1"
        assert res[0]['time_account'] == 0

    def test0103(self):  # Vytvor user 2 so spravnymi udajmi
        response = register_user(self, "+421 900 000002", "test2", "test2", "Testinguser2")
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test0104(self):  # Overenie existencie user 2
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/2")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert res[0]['id'] == 2
        assert res[0]['phone'] == "+421 900 000002"
        assert res[0]['user_name'] == "Testinguser2"
        assert res[0]['time_account'] == 0

    def test0105(self):
        response = register_user(self, "+421 900 000003", "test3", "test3",
                                 "Testinguser3")  # Vytvor user 3 so spravnymi udajmi
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test0106(self):  # Overenie existencie user 3
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/3")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert res[0]['id'] == 3
        assert res[0]['phone'] == "+421 900 000003"
        assert res[0]['user_name'] == "Testinguser3"
        assert res[0]['time_account'] == 0

    def test0111(self):  # Test na overenie informacii s get all users
        tester = app.test_client(self)
        response = tester.get("/api/v1/users")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert type(res[0]) is dict
        assert type(res[1]) is dict
        assert type(res[2]) is dict
        assert 'id' in res[0]
        assert type(res[0]['id']) is int
        assert 'phone' in res[0]
        assert type(res[0]['phone']) is str
        assert 'user_name' in res[0]
        assert type(res[0]['user_name']) is str
        assert 'time_account' in res[0]
        assert type(res[0]['time_account']) is int

    def test0121(self):
        response = register_user(self, "+421 900 000001", "test2", "test2",
                                 "Testinguser3")  # Test o vytvorenie usera s rovnakym telefonnym cislom
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 405)

    def test0122(self):
        response = register_user(self, "+421900000001", "test2", "test2",
                                 "Testinguser3")  # Test o vytvorenie usera s nespravnym formatom telefonneho cisla
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test0123(self):
        response = register_user(self, "+421 900 000002", "test2", "test1",
                                 "Testinguser3")  # Test o vytvorenie usera s roznymi heslami
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test0124(self):
        response = register_user(self, "+ppp ppp pppppp", "test2", "test2",
                                 "Testinguser3")  # Test o vytvorenie usera s nespravnym formatom telefonneho cisla
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test0125(self):  # Vytvorenie usera bez user_name
        tester = app.test_client(self)
        response = tester.post("/api/v1/user-create", json={
            'phone': '+421 900 000004',
            'password': 'test4',
            'password_val': 'test4',
        })
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test0126(self):  # Vytvorenie usera bez phone
        tester = app.test_client(self)
        response = tester.post("/api/v1/user-create", json={
            'password': 'test4',
            'password_val': 'test4',
            'user_name': 'Testinguser4'
        })
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test0127(self):  # Vytvorenie usera bez password
        tester = app.test_client(self)
        response = tester.post("/api/v1/user-create", json={
            'phone': '+421 900 000004',
            'user_name': 'Testinguser4'
        })
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test0128(self):  # Test na overenie informacii z neexistujuceho usera
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/4")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test0129(self):  # Test na vytvorenie pouzivatela s velmi dlhym username
        tester = app.test_client(self)
        response = tester.post("/api/v1/user-create", json={
            'phone': '+421 900 000004',
            'user_name': 'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',
            'password': 'testing',
            'password_val': 'testing'
        })
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0201(self):  # Test prihlasenie user 1
        response = login_user(self, "+421 900 000001", "test1")
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)

    def test0202(self):  # Test prihlasenie user 2
        response = login_user(self, "+421 900 000002", "test2")
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)

    def test0203(self):  # Test prihlasenie user 3
        response = login_user(self, "+421 900 000003", "test3")
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)

    def test0211(self):  # Test prihlasenie usera s nespravnym heslom
        response = login_user(self, "+421 900 000001", "test2")
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)

    def test0212(self):  # Test prihlasenie s neexistujucim telefonnym cislom
        response = login_user(self, "+421 900 000000", "test1")
        self.assertEqual(response.content_type, "application/json")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)

    def test0221(self):  # Prihlasenie bez password
        tester = app.test_client(self)
        response = tester.post("/api/v1/user/login", json={
            'phone': '+421 900 000004',
        })
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test0222(self):  # Prihlasenie bez phone
        tester = app.test_client(self)
        response = tester.post("/api/v1/user/login", json={
            'password': 'test1',
        })
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)

    def test0301(self):  # Vytvorenie service pre user 1
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/service-create", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing1',
            estimate=1
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test0302(self):  # Skontroluj vytvorenie servisu
        tester = app.test_client(self)
        response = tester.get("/api/v1/service/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert res[0]['id'] == 1
        assert res[0]['title'] == 'Testing1'
        assert res[0]['estimate'] == 1
        assert res[0]['avg_rating'] is None

    def test0303(self):  # Vytvorenie service pre user 2
        login = login_user(self, "+421 900 000002", "test2")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/service-create", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing2',
            estimate=2
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test0304(self):  # Skontroluj vytvorenie servisu
        tester = app.test_client(self)
        response = tester.get("/api/v1/service/2")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert res[0]['id'] == 2
        assert res[0]['title'] == 'Testing2'
        assert res[0]['estimate'] == 2
        assert res[0]['avg_rating'] is None

    def test0305(self):  # Service Search
        tester = app.test_client(self)
        response = tester.get("/api/v1/service-search?ord=asc&field=title&s=tes")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert res[0]['id'] == 1
        assert res[0]['title'] == 'Testing1'
        assert res[0]['estimate'] == 1
        assert res[0]['avg_rating'] is None

    def test0311(self):  # Test na overenie informacii s get all services
        tester = app.test_client(self)
        response = tester.get("/api/v1/services")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert type(res[0]) is dict
        assert type(res[1]) is dict
        assert 'id' in res[0]
        assert type(res[0]['id']) is int
        assert 'title' in res[0]
        assert type(res[0]['title']) is str
        assert 'estimate' in res[0]
        if res[0]['estimate'] is not None:
            assert type(res[0]['estimate']) is int
        assert 'avg_rating' in res[0]
        if res[0]['avg_rating'] is not None:
            assert type(res[0]['avg_rating']) is int

    def test0321(self):  # Test na vytvorenie service bez title
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/service-create", headers={'Authorization': 'Bearer ' + token}, data=dict(
            estimate=1
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0322(self):  # Test na vytvorenie service s estimate v nespravnom formate
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/service-create", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing1',
            estimate='p'
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0323(self):  # Test na vytvorenie service s title vacsim ako 1000
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/service-create", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title="iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii",
            estimate=1
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0324(self):  # Test na overenie informacii z neexistujuceho servisu
        tester = app.test_client(self)
        response = tester.get("/api/v1/service/3")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test0325(self):  # Vytvorenie service pre neprihlaseneho usera
        tester = app.test_client(self)
        response = tester.post("/api/v1/service-create", data=dict(
            title='Testing1',
            estimate=1
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test0326(self):  # Test na vytvorenie service s estimate v zapornom tvare
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/service-create", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing1',
            estimate=-1
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0327(self):  # Test na vytvorenie service s estimate s prilis velkou hodnotou
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/service-create", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing1',
            estimate=31
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0328(self):  # Test na vytvorenie service s estimate s desatinnou hodnotou
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/service-create", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing1',
            estimate=1.1
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0401(self):  # Test na vytvorenie serviceregister s user 3 na service 1
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/serviceregister-create",
                               headers={'Authorization': 'Bearer ' + token}, data=dict(service_id=1))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test0402(self):  # Test na kontrolu udajov v serviceregister 1
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister/1")
        res = json.loads(response.data.decode('utf8'))
        assert res[0]['id'] == 1
        assert res[0]['hours'] is None
        assert res[0]['service_status'] == 'inprogress'
        assert res[0]['end_time'] is None
        assert res[0]['rating'] is None

    def test0403(self):  # Test na vytvorenie serviceregister s user 3 na service 2
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/serviceregister-create",
                               headers={'Authorization': 'Bearer ' + token}, data=dict(service_id=2))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test0404(self):  # Test na kontrolu udajov v serviceregister 2
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister/2")
        res = json.loads(response.data.decode('utf8'))
        assert res[0]['id'] == 2
        assert res[0]['hours'] is None
        assert res[0]['service_status'] == 'inprogress'
        assert res[0]['end_time'] is None
        assert res[0]['rating'] is None

    def test0411(self):  # Test na overenie informacii zo serviceregister
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf8'))
        assert type(res[0]) is dict
        assert type(res[1]) is dict
        assert 'id' in res[0]
        assert type(res[0]['id']) is int
        assert 'hours' in res[0]
        if res[0]['hours'] is not None:
            assert type(res[0]['hours']) is int
        assert 'service_status' in res[0]
        assert type(res[0]['service_status']) is str
        assert 'end_time' in res[0]
        if res[0]['end_time'] is not None:
            assert type(res[0]['end_time']) is str
        assert 'rating' in res[0]
        if res[0]['rating'] is not None:
            assert type(res[0]['rating']) is int

    def test0421(self):  # Test na vytvorenie serviceregister s user 1 na service 1
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/serviceregister-create",
                               headers={'Authorization': 'Bearer ' + token}, data=dict(service_id=1))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0422(self):  # Test na vytvorenie serviceregister s user 1 na neexistujuci service 3
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/serviceregister-create",
                               headers={'Authorization': 'Bearer ' + token}, data=dict(service_id=3))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0423(self):  # Test na vytvorenie serviceregister s user 1 na service s neznamymo oznacenim 'p'
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/serviceregister-create",
                               headers={'Authorization': 'Bearer ' + token}, data=dict(service_id='p'))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0424(self):  # Test na nacitanie neexistujuceho serviceregister
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister/3")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test0425(self):  # Test na vytvorenie serviceregister na service 1 s neprihlasenym userom
        tester = app.test_client(self)
        response = tester.post("/api/v1/serviceregister-create", data=dict(service_id=1))
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test0501(self):  # Test na ukoncenie serviceregister
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1/5/3", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test0502(self):  # Test na overenie informacii zo serviceregister
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf8'))
        assert type(res[0]) is dict
        assert 'id' in res[0]
        assert type(res[0]['id']) is int
        assert 'hours' in res[0]
        if res[0]['hours'] is not None:
            assert type(res[0]['hours']) is int
        assert 'service_status' in res[0]
        assert type(res[0]['service_status']) is str
        assert 'end_time' in res[0]
        if res[0]['end_time'] is not None:
            assert type(res[0]['end_time']) is str
        assert 'rating' in res[0]
        if res[0]['rating'] is not None:
            assert type(res[0]['rating']) is int
        assert res[0]['id'] == 1
        assert res[0]['hours'] == 5
        assert res[0]['service_status'] == 'ended'
        assert datetime.strptime(str(res[0]['end_time']), "%a, %d %b %Y %H:%M:%S %Z")
        assert res[0]['rating'] == 3

    def test0521(self):  # Test na ukoncenie serviceregister na neexistujuci serviceregister
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/3/5/3", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test0522(self):  # Test na ukoncenie serviceregister na neexistujuci serviceregister 'p'
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/p/5/3", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0523(self):  # Test na ukoncenie serviceregister s hours -1
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/2/-1/3", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0524(self):  # Test na ukoncenie serviceregister s hours 31
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/2/31/3", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0525(self):  # Test na ukoncenie serviceregister s hours 'p'
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/2/p/3", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0526(self):  # Test na ukoncenie serviceregister s hours 1.1
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/2/1.1/3", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0531(self):  # Test na ukoncenie serviceregister s rating -1
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/2/5/-1", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0532(self):  # Test na ukoncenie serviceregister s rating 'p'
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/2/5/p", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0533(self):  # Test na ukoncenie serviceregister s rating 6
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/2/5/6", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0534(self):  # Test na ukoncenie serviceregister s rating 6
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/2/5/1.1", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0541(self):  # Test na ukoncenie serviceregister s neprihlasenym userom
        tester = app.test_client(self)
        response = tester.put("/api/v1/serviceregister/2/5/3")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test0542(self):  # Test na vyhladanie servise podla ratingu
        tester = app.test_client(self)
        response = tester.get("/api/v1/find_service_rating?s=1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test0543(self):  # Test na vyhladanie servise podla ratingu s prilis vysokym ratingom
        tester = app.test_client(self)
        response = tester.get("/api/v1/find_service_rating?s=5")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test0544(self):  # Test na vyhladanie servise podla ratingu s nespravnym ratingom
        tester = app.test_client(self)
        response = tester.get("/api/v1/find_service_rating?s=p")
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0601(self):  # Test na zmenu udajov v registerservice
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1",
                              headers={'Authorization': 'Bearer ' + token}, data=dict(
                                                                                hours=7,
                                                                                end_time='2020-01-01',
                                                                                rating=5
                                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test0602(self):  # Test na overenie informacii zo serviceregister po edite
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf8'))
        assert res[0]['id'] == 1
        assert res[0]['hours'] == 7
        assert res[0]['service_status'] == 'ended'
        assert datetime.strptime(str(res[0]['end_time']), "%a, %d %b %Y %H:%M:%S %Z")
        assert res[0]['rating'] == 5

    def test0621(self):  # Test na zmenu udajov v serviceregister na neexistujucom serviseregister
        login = login_user(self, "+421 900 000003", "test3")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/5",
                              headers={'Authorization': 'Bearer ' + token}, data=dict())
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test0622(self):  # Test na zmenu udajov v hodin v nespravnom formate
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1",
                              headers={'Authorization': 'Bearer ' + token}, data=dict(
                                                                                hours='p',
                                                                                end_time='2020-01-01',
                                                                                rating=4
                                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0623(self):  # Test na zmenu udajov v hodin v zapornom formate
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1",
                              headers={'Authorization': 'Bearer ' + token}, data=dict(
                                                                                hours=-1,
                                                                                end_time='2020-01-01',
                                                                                rating=4
                                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0624(self):  # Test na zmenu udajov v hodin s prilis velkou hodnotou
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1",
                              headers={'Authorization': 'Bearer ' + token}, data=dict(
                                                                                hours=31,
                                                                                end_time='2020-01-01',
                                                                                rating=4
                                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0625(self):  # Test na zmenu udajov v hodin s prilis velkou hodnotou
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1",
                              headers={'Authorization': 'Bearer ' + token}, data=dict(
                                                                                hours=1.1,
                                                                                end_time='2020-01-01',
                                                                                rating=4
                                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0631(self):  # Test na zmenu udajov datumu v nespravnom formate
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1",
                              headers={'Authorization': 'Bearer ' + token}, data=dict(
                                                                                hours=1,
                                                                                end_time='2020-01-32',
                                                                                rating=4
                                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0632(self):  # Test na zmenu udajov datumu v nespravnom formate
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1",
                              headers={'Authorization': 'Bearer ' + token}, data=dict(
                                                                                hours=1,
                                                                                end_time='popo-po-po',
                                                                                rating=4
                                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0641(self):  # Test na zmenu udajov ratingu v nespravnom formate
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1",
                              headers={'Authorization': 'Bearer ' + token}, data=dict(
                                                                                hours=1,
                                                                                end_time='2020-01-31',
                                                                                rating='p'
                                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0642(self):  # Test na zmenu udajov ratingu mimo ratingu
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1",
                              headers={'Authorization': 'Bearer ' + token}, data=dict(
                                                                                hours=1,
                                                                                end_time='2020-01-31',
                                                                                rating=-1
                                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0643(self):  # Test na zmenu udajov ratingu mimo ratingu
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1",
                              headers={'Authorization': 'Bearer ' + token}, data=dict(
                                                                                hours=1,
                                                                                end_time='2020-01-31',
                                                                                rating=6
                                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0644(self):  # Test na zmenu udajov ratingu mimo ratingu
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/serviceregister/1",
                              headers={'Authorization': 'Bearer ' + token}, data=dict(
                                                                                hours=1,
                                                                                end_time='2020-01-31',
                                                                                rating=1.1
                                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0651(self):  # Test na zmenu udajov v registerservice s neprihlasenym userom
        tester = app.test_client(self)
        response = tester.put("/api/v1/serviceregister/1", data=dict(
                                                                hours=7,
                                                                end_time='2020-01-01',
                                                                rating=5
                                                                ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test0700(self):  # Test na vymazanie serviceregister 1 s neprihlasenym userom
        tester = app.test_client(self)
        response = tester.delete("/api/v1/serviceregister/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test0701(self):  # Test na vymazanie serviceregister 1
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/serviceregister/1", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test0702(self):  # Test na kontrolu vymazania serviceregister 2
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test0703(self):  # Test na vymazanie serviceregister 1
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/serviceregister/2", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test0704(self):  # Test na kontrolu vymazania serviceregister 2
        tester = app.test_client(self)
        response = tester.get("/api/v1/serviceregister/2")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test0705(self):  # Test na vymazanie neexistujuceho serviceregister
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/serviceregister/3", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test0801(self):  # Test na upravu service
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/service/1", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing_edit',
            estimate=5
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test0802(self):  # Test na kontrolu udajov po edite
        tester = app.test_client(self)
        response = tester.get("/api/v1/service/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert res[0]['id'] == 1
        assert res[0]['title'] == 'Testing_edit'
        assert res[0]['estimate'] == 5
        assert res[0]['avg_rating'] == 3

    def test0821(self):  # Test na upravu servisu s estimate v nespravnom tvare
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/service/1", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing_edit',
            estimate=-1
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0822(self):  # Test na upravu servisu s estimate v nespravnom tvare
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/service/1", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing_edit',
            estimate='p'
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0823(self):  # Test na upravu servisu s estimate s prilis velkou hodnotou
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/service/1", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing_edit',
            estimate=31
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0824(self):  # Test na upravu servisu s estimate s prilis velkou hodnotou
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/service/1", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='Testing_edit',
            estimate=1.1
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0831(self):  # Test na upravu title s poctom znakov na 1000
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/service/1", headers={'Authorization': 'Bearer ' + token}, data=dict(
            title='iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test0832(self):  # Test na upravu service s neprihlasenym pouzivatelom
        tester = app.test_client(self)
        response = tester.put("/api/v1/service/1", data=dict(
            title='Testing_edit',
            estimate=5
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test0900(self):  # Vymazanie service 1 s neprihlasenym userom
        tester = app.test_client(self)
        response = tester.delete("/api/v1/service/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test0901(self):  # Vymazanie service 1
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/service/1", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test0902(self):  # Kontrola vymazania
        tester = app.test_client(self)
        response = tester.get("/api/v1/service/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test0903(self):  # Vymazanie service 2
        login = login_user(self, "+421 900 000002", "test2")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/service/2", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test0904(self):  # Kontrola vymazania
        tester = app.test_client(self)
        response = tester.get("/api/v1/service/2")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test1001(self):  # User profile
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.get("/api/v1/user/profile", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert res[0]['id'] == 1
        assert res[0]['phone'] == "+421 900 000001"
        assert res[0]['user_name'] == "Testinguser1"
        assert res[0]['time_account'] == 5

    def test1002(self):  # User profile s neprihlasenym userom
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/profile")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test1101(self):  # Change password
        tester = app.test_client(self)
        response = tester.put("/api/v1/user/3/set-password", data=dict(
            password='testing',
            password_val='testing'
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test1102(self):  # Change password s rozlicnymi heslami
        tester = app.test_client(self)
        response = tester.put("/api/v1/user/3/set-password", data=dict(
            password='testing',
            password_val='testing2'
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test1103(self):  # Change password s chybajucimi heslami
        tester = app.test_client(self)
        response = tester.put("/api/v1/user/3/set-password", data=dict(dummy='dummy'))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test1104(self):  # Change password s chybajucim heslom na validaciu
        tester = app.test_client(self)
        response = tester.put("/api/v1/user/3/set-password", data=dict(password='testing'))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test1105(self):  # Change password na neexistujucom pouzivatelovi
        tester = app.test_client(self)
        response = tester.put("/api/v1/user/4/set-password", data=dict(
            password='testing',
            password_val='testing'
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test1201(self):  # Logout
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.post("/api/v1/user/logout", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)
        self.assertEqual(response.content_type, "application/json")

    def test1202(self):  # Logout s neprihlasenym pouzivatelom
        tester = app.test_client(self)

        response = tester.post("/api/v1/user/logout")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test1301(self):  # Edit User:
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/user/3", headers={'Authorization': 'Bearer ' + token}, data=dict(
            phone="+421 900 999999",
            user_name='Antonio'

        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test1302(self):  # Kontrola editu usera
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/3")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        res = json.loads(response.data.decode('utf-8'))
        assert res[0]['id'] == 3
        assert res[0]['phone'] == "+421 900 999999"
        assert res[0]['user_name'] == "Antonio"
        assert res[0]['time_account'] == 0

    def test1303(self):  # Edit User s telefonnym cislom v nespravnom tvare
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/user/3", headers={'Authorization': 'Bearer ' + token}, data=dict(
            phone="+421900999999",
            user_name='Antonio'

        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test1304(self):  # Edit User s telefonnym cislom v nespravnom tvare
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/user/3", headers={'Authorization': 'Bearer ' + token}, data=dict(
            phone="+ppp ppp pppppp",
            user_name='Antonio'

        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test1311(self):  # Edit User s prilis dlhym username
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.put("/api/v1/user/3", headers={'Authorization': 'Bearer ' + token}, data=dict(
            phone="+421 900 999999",
            user_name='iiiiiiiiiiiiiiiiiiiiiiiiiiiiiii'

        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 400)
        self.assertEqual(response.content_type, "application/json")

    def test1401(self):  # User history log
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.get("/api/v1/user/history-log", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test1402(self):  # User history log s neprihlasenym pouzivatelom
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/history-log")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test1501(self):  # User services
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.get("/api/v1/user/services", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")

    def test1502(self):  # User services s neprihlasenym pouzivatelom
        tester = app.test_client(self)

        response = tester.get("/api/v1/user/services")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test1600(self):  # Vymazanie usera 3 s neprihlasenym pouzivatelom
        tester = app.test_client(self)
        response = tester.delete("/api/v1/user/3")
        statuscode = response.status_code
        self.assertEqual(statuscode, 401)
        self.assertEqual(response.content_type, "application/json")

    def test1601(self):  # Vymazanie usera 3
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/user/3", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test1602(self):  # Kontrola vymazania usera 3
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/3")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test1603(self):  # Vymazanie usera 2
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/user/2", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test1604(self):  # Kontrola vymazania usera 2
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/2")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")

    def test1605(self):  # Vymazanie usera 1
        login = login_user(self, "+421 900 000001", "test1")
        tester = app.test_client(self)
        token = login.json['access_token']
        response = tester.delete("/api/v1/user/1", headers={'Authorization': 'Bearer ' + token})
        statuscode = response.status_code
        self.assertEqual(statuscode, 204)
        self.assertEqual(response.content_type, "application/json")

    def test1606(self):  # Kontrola vymazania usera 1
        tester = app.test_client(self)
        response = tester.get("/api/v1/user/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 404)
        self.assertEqual(response.content_type, "application/json")


# Spustenie testov
if __name__ == "__main__":
    unittest.main()
