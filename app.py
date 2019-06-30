from flask import Flask, abort, request, jsonify
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId


client = MongoClient('localhost', 27017)
db = client.restapi
app = Flask(__name__)

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


def encode(all):
    all_posts = []
    for i in all:
        ID = str(i['_id'])
        i['_id'] = ID
        all_posts.append(i)
    return all_posts


if __name__ == '__main__':
    app.run(debug=True)