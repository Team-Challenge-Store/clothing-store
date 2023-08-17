import requests

url = 'http://127.0.0.1:5000/register'
myobj = {'username': 'Ivan',
         'email': 'ivan@gmail.com',
         'password': '1234568'}

x = requests.post(url, json = myobj)

print(x.status_code == 201)