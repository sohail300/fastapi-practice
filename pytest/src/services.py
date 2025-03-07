import requests

db = {
    1: 'Sohail',
    2: 'Rohan',
    3: 'Rohit'
}

def get_users_from_db(id):
    return db[id]

def get_users_from_api():
    response = requests.get('https://jsonplaceholder.typicode.com/users')

    if response.status_code == 200:
        return response.json()
    
    raise requests.HTTPError