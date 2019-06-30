from flask import Flask, abort, request, jsonify, Response
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId
from functools import wraps

client = MongoClient('localhost', 27017)
db = client.restapi
app = Flask(__name__)

def check_auth(username, password):
    a = db.users.find_one({'username': username,
                      'password': password})
    ID = str(a['_id'])
    if a is not None:
        return True and ID
    if a is None:
        return False


def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/api/get_posts/', methods=['GET'])
def check_posts():
    posts = db.posts.find()
    return jsonify(encode(posts))


@app.route('/api/check_in/', methods=['POST'])

def create_user():
    content = request.json
    if len(content["email"]) <= 0 or len(content["username"]) <= 0 or len(content["password"]) <= 0:
        abort(400)
    else:
        result_email = db.users.find_one({'email': content['email']})
        if result_email is None:
            result_username = db.users.find_one({'username': content['username']})
            if result_username is None:
                user = {'email': content['email'],
                        'username': content['username'],
                        'password': content['password']
                        }
                db.users.insert_one(user)
                return 'Пользователь создан'
            else:
                return 'Такой username уже существует'
        else:
            return 'Такой Email уже существует'

@app.route('/api/new_post', methods=['POST'])
@requires_auth
def create_article():
    content = request.json
    if len(content["author_id"]) <= 0 or len(content["title"]) <= 0 or len(content["content"]) <= 0:
        abort(400)
    else:
        result = db.users.find_one({'_id': ObjectId(content['author_id'])})
        print(result)
        if result is None:
            return 'Зарегестрируйтесь'
        else:
            article = {'author_id': content["author_id"],
                       'title': content["title"],
                       'content': content["content"],
                       'publication_datetime': datetime.datetime.utcnow()
                       }
            db.posts.insert_one(article)
            return str("Пост добавлен")


@app.route('/api/new_comment', methods=['POST'])
@requires_auth
def new_comment():
    content = request.json
    if len(content["author_id"]) <= 0 or len(content["post_id"]) <= 0 or len(content["title"]) <= 0 or len(content["content"]) <= 0:
        abort(400)
    else:
        result = db.posts.find_one({'_id': ObjectId(content['post_id'])})
        if result is not None:
            result2 = db.users.find_one({'_id': ObjectId(content['author_id'])})
            if result2 is not None:
                comment = {'post_id': content["post_id"],
                           'author_id': content["author_id"],
                           'title': content["title"],
                           'content': content["content"],
                           'publication_datetime': datetime.datetime.utcnow()}
                db.comments.insert_one(comment)
                return "Коментарий добавлен"
            else:
                return 'Зарегистрируйтесь, чтобы оставить коментарий'

        else:
            return 'Такого поста не существует'


@app.route('/api/change/', methods=['PUT'])
@requires_auth
def update_post():

    content = request.json
    a = db.posts.find_one({'_id': ObjectId(content['post_id'])})
    if a is not None and content['author_id'] == a['author_id']:
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
        return "Статья изменена"
    else:
        return 'Это не ваша статья'


@app.route('/api/delete/', methods=['DELETE'])
@requires_auth
def delete():
    content = request.json
    if content['choose'] == 'post':
        a = db.posts.find_one({'_id': ObjectId(content['post_id'])})
        if a is not None:
            db.posts.remove({'_id': ObjectId(content['post_id'])})
            return 'Пост удален'
        else:
            return 'Пост не найден'
    elif content['choose'] == 'comment':
        a = db.comments.find_one({'_id': ObjectId(content['post_id'])})
        if a is not None:
            db.comments.remove({'_id': ObjectId(content['post_id'])})
            return 'Коммент удален'
        else:
            return 'Коммент не найден'


def encode(all):
    all_posts = []
    for i in all:
        ID = str(i['_id'])
        i['_id'] = ID
        all_posts.append(i)
    return all_posts


if __name__ == '__main__':
    app.run(debug=True)