from movieapp.db import get_credentials
from sqlalchemy import text, create_engine


def test_get_details(client):
    response = client.post('/index/customers', data={
        'clist': "Mary Smith",
    })
    assert response.status_code == 200


def test_add_cust_button(client):
    response = client.post('index/customers', data={
        'add_cust': 'Add Customer',
    })
    assert response.status_code == 200


def test_add_cust_to_db(client):
    response = client.post('index/customers', data={
        'a_store_id': '1',
        'a_first_name': "Test",
        'a_last_name': "Customer",
        'a_email': "Test@email.com",
        'a_active': '1',
        'a_address': "1234 Test Address",
        'a_city': "Newark",
        'a_district': "New Jersey",
        'a_postal_code': "09876",
        'a_phone': "9998887777",
    })
    assert response.status_code == 200


def test_delete_cust_from_db(client):
    credentials = get_credentials()
    engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/sakila".format(credentials['user_name'], credentials['password'], credentials['host_system'], credentials['port']))
    db = engine.connect()
    get_cust_id = db.execute(text('SELECT customer_id FROM customer WHERE first_name = "Test" AND last_name = "Customer"'))
    c_id_query = []
    for (customer_id) in get_cust_id:
        c_id_query.append({
            'customer_id': customer_id
        })
    
    cust_id = str(c_id_query[0]['customer_id'])
    cust_id = cust_id.strip('(),')
    response = client.post('index/customers', data={
        'store_id': '1',
        'customer_id': cust_id,
        'first_name': "Test",
        'last_name': "Customer",
        'email': "Test@email.com",
        'active': '1',
        'address': "1234 Test Address",
        'city': "Newark",
        'district': "New Jersey",
        'postal_code': "09876",
        'phone': "9998887777",
        'delete_cust': "Delete Customer",
    })
    assert response.status_code == 200

