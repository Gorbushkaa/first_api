import requests
url = 'http://127.0.0.1:5000/api/new_comment'
send = {'post_id': '5d167cde53ae0bc2f740ad5b',
        'author_id': '5d166e719b1b7d1188d608af',
        'title': 'TITLE',
        'content': 'COMMENT',
        }


'''url = 'http://127.0.0.1:5000/api/get_posts/'''

'''url = 'http://127.0.0.1:5000/api/new_post'
send = {"author_id": "ID Автора",
        "title": "ОПИСАНИЕ",
        "content": "ПОСТ22"}'''
"""
url = 'http://127.0.0.1:5000/api/check_in/'
send = {"email": "ggg@gmail.com",
        "username": "asd22ada",
        "password": "Seasd"}"""

res = requests.post(url, json=send)

print(res.text)