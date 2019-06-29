from flask import Flask, abort, request, jsonify

from pymongo import MongoClient
import datetime
client = MongoClient('localhost', 27017)
db = client.restapi
app = Flask(__name__)

@app.route('/api/get_posts/', methods=['GET'])
def check_posts():
    a = db.posts.find()
    for post in a:
        return jsonify(post)


@app.route('/api/check_in/', methods=['POST'])
def create_user():
    content = request.json
    if len(content["email"]) <= 0 or len(content["username"]) <= 0 or len(content["password"]) <= 0:
        abort(400)
    else:
        try:
            print(db.users.find_one({'email': content['email']})['email'])
            return 'Пользователь с таким Email уже существует'
        except TypeError:
            try:
                print(db.users.find_one({'username': content['username']})['username'])
                return 'Пользователь с таким Username уже существует'
            except TypeError:
                user = {'email': content['email'],
                        'username': content['username'],
                        'password': content['password']
                        }
                db.users.insert_one(user)
                return 'Пользователь создан'


@app.route('/api/new_post', methods=['POST'])
def create_article():
    content = request.json
    if len(content["author_id"]) <= 0 or len(content["title"]) <= 0 or len(content["content"]) <= 0:
        abort(400)
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
        print(db.posts.find_one({'_id': content['post_id']})['email'])
        try:
            print(db.posts.find_one({'_id': content['post_id']})['_id'])
            try:
                print(db.users.find_one({'_id': content['author_id']})['_id'])
                comment = {'post_id': content["post_id"],
                           'author_id': content["author_id"],
                           'title': content["title"],
                           'content': content["content"],
                           'publication_datetime': datetime.datetime.utcnow()}
                db.comments.insert_one(comment)
            except TypeError:
                return 'Зарегистрируйтесь, чтобы оставить коментарий'

        except TypeError:
            return 'Такого поста не существует'



if __name__ == '__main__':
    app.run(debug=True)