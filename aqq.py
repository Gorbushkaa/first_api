import requests
from requests.auth import HTTPBasicAuth
'''url = 'http://127.0.0.1:5000/api/new_comment'
send = {'post_id': '5d1727bf1bc709519742b68c',
        'author_id': '5d166e719b1b7d1188d608af',
        'title': 'TITLE',
        'content': 'COMMENT',
        }'''
"""url = 'http://127.0.0.1:5000/api/change_post/'
send = {'post_id': '5d18815010398fc4540b90db',
        'author_id': '5d166e719b1b7d1188d608af',
        'title': 'a32332af',
        'content': '333',
        }"""


'''url = 'http://127.0.0.1:5000/api/delete/'
send = {'post_id': '5d1882e133e705f0605538aa',
        'choose': 'comment'}'''

url = 'http://127.0.0.1:5000/api/get_posts/'

'''url = 'http://127.0.0.1:5000/api/new_post'
send = {"author_id": "5d166e719b1b7d1188d608af",
        "title": "ОПИСАНИЕ",
        "content": "ПОСТ22"}'''

'''url = 'http://127.0.0.1:5000/api/check_in/'
send = {"email": "g111212gg@gmail.com",
        "username": "asd33122ada",
        "password": "Seasd"}'''

res = requests.get(url, auth=('Sema', 'password1'))

print(res.text)