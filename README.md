# API endpoints

List of images for the current user (most recent first, limited to users following).
```
GET
/imgapi/api/images/
```
List of all posts (ordered by likes).
```
GET
/imgapi/api/posts/
```
List of all users (including information on the number of following and followers).
```
GET
/imgapi/api/users
```
Current user can like a post (image).
```
POST
/imgapi/api/images/like/<int:pk>/
```
A user can follow/unfollow another user.
```
POST
/imgapi/api/follow/<int:pk>/
POST
/imgapi/api/unfollow/<int:pk>/
```
User registration
```
POST
{'username': <username>, 'password': <password>, 'email': <email>}
/imgapi/api/register/
```
List of images created by current user / Upload image
```
GET
/imgapi/api/userimages/

POST
data = {'title': <title>, 'caption': <caption>}
files = {'image': (<file_name>, <bytes>)}
/imgapi/api/userimages/
```

# Installation
Clone the repository, cd into the directory, create a virtualenv, activate it and install requirements.txt.
```
git clone https://github.com/e/drfhedgehog.git
cd drfhedgehog/
virtualenv -p `which python3` venv
. ./venv/bin/activate
pip install -r requirements.txt 
```
```
marcos@logos:~/w> git clone https://github.com/e/drfhedgehog.git
Cloning into 'drfhedgehog'...
remote: Enumerating objects: 32, done.
remote: Counting objects: 100% (32/32), done.
remote: Compressing objects: 100% (24/24), done.
remote: Total 32 (delta 5), reused 32 (delta 5), pack-reused 0
Unpacking objects: 100% (32/32), done.
marcos@logos:~/w> cd drfhedgehog/
marcos@logos:~/w/drfhedgehog(master)> virtualenv -p `which python3` venv
Already using interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in /home/marcos/w/drfhedgehog/venv/bin/python3
Also creating executable in /home/marcos/w/drfhedgehog/venv/bin/python
Installing setuptools, pkg_resources, pip, wheel...done.
(venv) marcos@logos:~/w/drfhedgehog(master)> pip install -r requirements.txt 
```
The settings.py file is pointing to a sample sqlite database which is included in the repository so that you can start testing the api right away. It contains several users:

- admin password: admin
- user1 password: user1
- user2 password: user2
- user3 password: user3
- user4 password: user4

Some users are following others and they have some images with likes, so you can skip the "setting up the database part", fire up the development server, get a token with those credentials and start issuing requests with your favourite tool (Python, cURL, Postman...) right away, but here is how you would start from scratch:


# Setting up the database
Delete the sample database, create a new database, create a superuser, start the development server and then add some users and images. You can use the Django admin, or you can also use the API, because although it was not a requirement, there's an endpoint to upload images!
```
rm db.sqlite
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Create some users using the API, this is an example using the requests module but you can use any tool:
```
(venv) marcos@logos:~/w/drfhedgehog(master)> pip install ipython requests
```
```
(venv) marcos@logos:~/w/drfhedgehog(master)> ipython
Python 3.6.9 (default, Jul 17 2020, 12:50:27) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.16.1 -- An enhanced Interactive Python. Type '?' for help.

In [10]: import requests
    ...: register_url = 'http://localhost:8000/imgapi/api/register/'
    ...: data = {'username': 'user1', 'password': 'user1', 'email': 'user1@user1.com'}
    ...: response = requests.post(register_url, data=data)

In [11]: response
Out[11]: <Response [201]>

In [12]: response.content
Out[12]: b'{"id":4,"username":"user1","first_name":"","last_name":"","email":"user1@user1.com","followers":0,"following":0}'
```
```
import requests
register_url = 'http://localhost:8000/imgapi/api/register/'
data = {'username': 'user1', 'password': 'user1', 'email': 'user1@user1.com'}
response = requests.post(register_url, data=data)
data = {'username': 'user2', 'password': 'user2', 'email': 'user2@user2.com'}
response = requests.post(register_url, data=data)
data = {'username': 'user3', 'password': 'user3', 'email': 'user3@user3.com'}
response = requests.post(register_url, data=data)
data = {'username': 'user4', 'password': 'user4', 'email': 'user4@user4.com'}
response = requests.post(register_url, data=data)
```
Token authentication is enabled, and most endpoints require authentication, let's create a convenience function to get a token
```
def get_token(username, password):
    login_url = 'http://localhost:8000/imgapi/api-token-auth/'
    data = {'username': username, 'password': password}
    response = requests.post(login_url, data=data)
    if response.status_code == 200:
        return response.json()['token']
token1 = get_token('user1', 'user1')
token2 = get_token('user2', 'user2')
token3 = get_token('user3', 'user3')
token4 = get_token('user4', 'user4')
```
```
In [34]: def get_token(username, password):
    ...:     login_url = 'http://localhost:8000/imgapi/api-token-auth/'
    ...:     data = {'username': username, 'password': password}
    ...:     response = requests.post(login_url, data=data)
    ...:     if response.status_code == 200:
    ...:         return response.json()['token']
    ...: 

In [35]: token1 = get_token('user1', 'user1')
    ...: token2 = get_token('user2', 'user2')
    ...: token3 = get_token('user3', 'user3')
    ...: token4 = get_token('user4', 'user4')

In [36]: token1
Out[36]: '5b4a8954900b4473ff840e996595766b93ff8b0c'

In [37]: token2
Out[37]: '805dfa62af7631e1303f67d32d2635f785528448'

In [38]: token3
Out[38]: '523dd232fd7734523b2a7984a4f3de0594cc8089'

In [39]: token4
Out[39]: 'e986c77a8ad2cd90f057e0aff1e9322c338539d8'
```
You can now list all the users:
```
In [42]: url = 'http://localhost:8000/imgapi/api/users/'
In [48]: headers={'Authorization': ' '.join(['Token', token1])}
In [49]: r=requests.get(url, headers=headers)

In [50]: r
Out[50]: <Response [200]>

In [51]: r.json()
Out[51]: 
[{'id': 1,
  'username': 'admin',
  'first_name': '',
  'last_name': '',
  'email': 'admin@admin.com',
  'followers': 0,
  'following': 0},
 {'id': 4,
  'username': 'user1',
  'first_name': '',
  'last_name': '',
  'email': 'user1@user1.com',
  'followers': 0,
  'following': 0},
 {'id': 5,
  'username': 'user2',
  'first_name': '',
  'last_name': '',
  'email': 'user2@user2.com',
  'followers': 0,
  'following': 0},
 {'id': 6,
  'username': 'user3',
  'first_name': '',
  'last_name': '',
  'email': 'user3@user3.com',
  'followers': 0,
  'following': 0},
 {'id': 7,
  'username': 'user4',
  'first_name': '',
  'last_name': '',
  'email': 'user4@user4.com',
  'followers': 0,
  'following': 0}]
```
And upload images:
```
In [74]: with open('media/bird1.jpeg', 'rb') as f:
    ...:     img = f.read()
    ...: files = {'image': ('bird1.jpeg', img)}
    ...: url = 'http://localhost:8000/imgapi/api/userimages/'
    ...: headers={'Authorization': ' '.join(['Token', token1])}
    ...: data = {'title': 'image 1', 'caption': 'image 1'}
    ...: response = requests.post(url, data=data, files=files, headers=headers)

In [75]: response
Out[75]: <Response [201]>

In [76]: response.content
Out[76]: b'{"id":3,"title":"image 1","caption":"image 1","image":"/imgapi/media/bird1_4bOUOj6.jpeg","user":4,"likes_count":0,"created_at":"2020-09-12T22:48:31.833216Z"}'
```
But it's probably easier to do it through the Django admin.

# Usage examples
List of all users (including information on the number of following and followers).
```
In [24]: response=requests.get('http://localhost:8000/imgapi/api/users/', headers=headers)

In [25]: response
Out[25]: <Response [200]>

In [26]: response.json()
Out[26]: 
[{'id': 1,
  'username': 'admin',
  'first_name': '',
  'last_name': '',
  'email': 'admin@admin.com',
  'followers': 0,
  'following': 0},
 {'id': 2,
  'username': 'user1',
  'first_name': '',
  'last_name': '',
  'email': 'user1@user1.com',
  'followers': 0,
  'following': 0},
 {'id': 3,
  'username': 'user2',
  'first_name': '',
  'last_name': '',
  'email': 'user2@user2.com',
  'followers': 0,
  'following': 0},
 {'id': 4,
  'username': 'user3',
  'first_name': '',
  'last_name': '',
  'email': 'user3@user3.com',
  'followers': 0,
  'following': 0},
 {'id': 5,
  'username': 'user4',
  'first_name': '',
  'last_name': '',
  'email': 'user4@user4.com',
  'followers': 0,
  'following': 0}]

In [27]: 
```
A user can follow/unfollow another user.
```
In [27]: response=requests.post('http://localhost:8000/imgapi/api/follow/2/', headers=headers
    ...: )

In [28]: response
Out[28]: <Response [200]>

In [29]: response.content
Out[29]: b'{"Message":"You are now following user1"}'

In [30]: response=requests.post('http://localhost:8000/imgapi/api/follow/3/', headers=headers)

In [31]: response.content
Out[31]: b'{"Message":"You are now following user2"}'

In [32]: response=requests.post('http://localhost:8000/imgapi/api/follow/4/', headers=headers)

In [33]: response.content
Out[33]: b'{"Message":"You are now following user3"}'

In [34]: response=requests.post('http://localhost:8000/imgapi/api/follow/5/', headers=headers)

In [35]: response.json()
Out[35]: {'Message': 'You are now following user4'}

In [36]: response=requests.post('http://localhost:8000/imgapi/api/follow/5/', headers=headers)

In [37]: response
Out[37]: <Response [200]>

In [38]: response.json()
Out[38]: {'Message': 'You are already following user4'}

In [39]: response=requests.post('http://localhost:8000/imgapi/api/unfollow/5/', headers=headers)

In [40]: response.json()
Out[40]: {'Message': 'You are no longer following user4'}

In [41]: 
```
Current user can like a post (image).
```

In [41]: response=requests.post('http://localhost:8000/imgapi/api/images/like/1/', headers=headers)

In [42]: response.json()
Out[42]: {'Message': 'Now you like image with id 1'}

In [43]: response=requests.post('http://localhost:8000/imgapi/api/images/like/2/', headers=headers)

In [44]: response.json()
Out[44]: {'Message': 'You already like image with id 2'}

In [45]: response=requests.post('http://localhost:8000/imgapi/api/images/like/3/', headers=headers)

In [46]: response.json()
Out[46]: {'Message': 'You already like image with id 3'}

In [47]: response=requests.post('http://localhost:8000/imgapi/api/images/like/5/', headers=headers)

In [48]: response.json()
Out[48]: {'Message': 'Now you like image with id 5'}

In [49]: 
```
List of all posts (ordered by likes).
```
In [49]: response=requests.get('http://localhost:8000/imgapi/api/posts/', headers=headers)

In [50]: response.json()
Out[50]: 
[{'id': 2,
  'title': 'bird2',
  'caption': 'bird2',
  'image': 'http://localhost:8000/imgapi/media/bird2_scyxiDe.jpeg',
  'user': 3,
  'likes_count': 5,
  'created_at': '2020-09-13T16:54:04.704134Z'},
 {'id': 3,
  'title': 'bird3',
  'caption': 'bird3',
  'image': 'http://localhost:8000/imgapi/media/bird3_TucciFg.jpeg',
  'user': 3,
  'likes_count': 5,
  'created_at': '2020-09-13T16:54:19.189794Z'},
 {'id': 4,
  'title': 'bird4',
  'caption': 'bird4',
  'image': 'http://localhost:8000/imgapi/media/bird4.jpeg',
  'user': 3,
  'likes_count': 5,
  'created_at': '2020-09-13T16:54:34.778798Z'},
 {'id': 1,
  'title': 'bird1',
  'caption': 'bird1',
  'image': 'http://localhost:8000/imgapi/media/bird1_jh2gyjB.jpeg',
  'user': 2,
  'likes_count': 1,
  'created_at': '2020-09-13T16:53:40.051934Z'},
 {'id': 5,
  'title': 'bird5',
  'caption': 'bird5',
  'image': 'http://localhost:8000/imgapi/media/bird6_t1iEAGI.jpeg',
  'user': 5,
  'likes_count': 1,
  'created_at': '2020-09-13T16:54:49.889913Z'}]

In [51]: 
```
List of images created by current user / Upload image
```
In [51]: response=requests.get('http://localhost:8000/imgapi/api/userimages/', headers=headers)

In [52]: response.json()
Out[52]: 
[{'id': 1,
  'title': 'bird1',
  'caption': 'bird1',
  'image': '/imgapi/media/bird1_jh2gyjB.jpeg',
  'user': 2,
  'likes_count': 1,
  'created_at': '2020-09-13T16:53:40.051934Z'}]

In [53]: 
```
