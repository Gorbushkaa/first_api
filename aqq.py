import requests
#ПРОСМОТР ВСЕХ СТАТЕЙ
'''url = 'http://84.201.132.180/api/get_posts/'
res = requests.get(url)
print(res.text)'''

#НОВЫЙ ПОСТ
'''url = 'http://127.0.0.1:5000/api/new_post'
send = {"title": "sdf33333333234234222222222222222411113333d",
        "content": "w33324!"}
res = requests.post(url, json=send, auth=('Coder22', 'SuperCoder22'))
print(res.text)'''

#НОВЫЙ КОМЕНТАРИЙ
'''url = 'http://84.201.132.180/api/new_comment'
send = {'post_id': '5d1727bf1bc709519742b68c',
        'title': 'TIT3122353245235324',
        'content': 'COMMEasdfasdfasNT',}
res = requests.post(url, json=send, auth=('Sema', 'password1'))
print(res.text)'''

#ИЗМЕНИТЬ ПОСТ
'''url = 'http://127.0.0.1:5000/api/change/'
send = {'post_id': '5d18813e10398fc4540b90da',
        'title': '3123332131',
        'content': '333цйуу'}
res = requests.put(url, json=send, auth=('Sema', 'password1'))
print(res.text)'''

#УДАЛИТЬ КОМЕНТАРИЙ ИЛИ ПОСТ
'''url = 'http://127.0.0.1:5000/api/delete/'
send = {'post_id': '5d188300c39a1e4368a90df6',
        'choose': 'comment'}
res = requests.delete(url, json=send, auth=('Sema', 'password1'))
print(res.text)'''

#НОВЫЙ ПОЛЬЗОВАТЕЛЬ
'''url = 'http://127.0.0.1:5000/api/check_in/'
send = {"email": "as33dadd.com",
        "username": "Coder22",
        "password": "SuperCoder22"}

res = requests.post(url, json=send)

print(res.text)'''