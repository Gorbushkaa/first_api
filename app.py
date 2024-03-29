from flask import Flask, abort, request, jsonify, Response
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId
from functools import wraps
import hashlib

client = MongoClient('localhost', 27017)
db = client.restapi
app = Flask(__name__)


def check_auth(username, password):
    hashedPassword = hashlib.sha256(password.encode()).hexdigest()
    result = db.users.find_one({'username': username,
                                'password': hashedPassword})
    if result is not None:
        return str(result['_id'])


def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):#Создание декоратора basicauth
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        ID = check_auth(auth.username, auth.password)
        if not auth or ID is None:
            return authenticate()
        return f(ID, *args, **kwargs)
    return decorated


@app.route('/api/get_posts/', methods=['GET'])
def check_posts():#Выводит все посты
    posts = db.posts.find()
    return jsonify(lst(posts))


@app.route('/api/check_in/', methods=['POST'])
def create_user():#Cоздание нового пользователя
    content = request.json
    if len(content["email"]) <= 0 or len(content["username"]) <= 0 or len(content["password"]) <= 0:
        abort(400)
    else:
        result_email = db.users.find_one({'email': content['email']})
        if result_email is None:
            result_username = db.users.find_one({'username': content['username']})
            if result_username is None:
                h = hashlib.sha256(str.encode(content['password']))
                password = h.hexdigest()
                user = {'email': content['email'],
                        'username': content['username'],
                        'password': password
                        }
                db.users.insert_one(user)
                return 'Пользователь создан'
            else:
                return 'Такой username уже существует'
        else:
            return abort(400, 'Такой Email уже существует')


@app.route('/api/new_post', methods=['POST'])
@requires_auth
def create_article(ID):#Создание новой статьи
    content = request.json
    if len(content["title"]) <= 0 or len(content["content"]) <= 0:
        abort(400)
    else:
        article = {'author_id': ID,
                   'title': content["title"],
                   'content': content["content"],
                   'publication_datetime': datetime.datetime.utcnow()
                   }
        db.posts.insert_one(article)
        check = db.posts.find_one({'author_id': ID,
                                   'title': content["title"],
                                   'content': content["content"]})

        if check is not None:
            return "Пост добавлен"
        elif check is None:
            return "Ошибка добавления"



@app.route('/api/new_comment', methods=['POST'])
@requires_auth#Новый коментарий
def new_comment(ID):
    content = request.json
    if len(content["post_id"]) <= 0 or len(content["title"]) <= 0 or len(content["content"]) <= 0:
        abort(400)
    else:
        result = db.posts.find_one({'_id': ObjectId(content['post_id'])})
        if result is not None:
            comment = {'post_id': content["post_id"],
                       'author_id': ID,
                       'title': content["title"],
                       'content': content["content"],
                       'publication_datetime': datetime.datetime.utcnow()}
            db.comments.insert_one(comment)
            check = db.comments.find_one({'post_id': content["post_id"],
                                          'author_id': ID,
                                          'title': content["title"],
                                          'content': content["content"]})
            if check is not None:
                return "Коментарий добавлен"
            elif check is None:
                return "Ошибка добавления"
        else:
            return 404, 'Такого поста не существует'


@app.route('/api/change/', methods=['PUT'])
@requires_auth#Изменение статьи
def update_post(ID):
    content = request.json
    a = db.posts.find_one({'_id': ObjectId(content['post_id'])})
    if a is not None and ID == a['author_id']:
        if len(content['title']) <= 0:
            content['title'] = a['title']
        elif len(content['content']) <= 0:
            content['content'] = a['content']
        old = {'_id': ObjectId(content['post_id']),
                'content': a['content'],
               'title': a['title']}
        new = {"$set":{'content': content['content'],
               'title': content['title']}}
        db.posts.update_one(old, new)
        check = db.posts.find_one({'content': content['content'],
                                   'title': content['title']})
        if check is not None:
            return "Статья изменена"
        elif check is None:
            return "Ошибка изменения"

    else:
        return 404, 'Это не ваша статья или статья не найдена'


@app.route('/api/delete/', methods=['DELETE'])
@requires_auth#Удаление статьи или коментария
def delete(ID):
    content = request.json
    if content['choose'] == 'post':
        a = db.posts.find_one({'_id': ObjectId(content['post_id'])})
        if a is not None and a['author_id'] == ID:
            db.posts.remove({'_id': ObjectId(content['post_id'])})
            return 'Пост удален'
        else:
            return 404, 'Пост не найден или он не Ваш'
    elif content['choose'] == 'comment':
        a = db.comments.find_one({'_id': ObjectId(content['post_id'])})
        if a is not None and a['author_id'] == ID:
            db.comments.remove({'_id': ObjectId(content['post_id'])})
            return 'Коммент удален'
        else:
            return 404, 'Коммент не найден или он не Ваш'


def lst(all):
    all_posts = []
    for i in all:
        ID = str(i['_id'])
        i['_id'] = ID
        all_posts.append(i)
    return all_posts


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=True)