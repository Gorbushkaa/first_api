from flask import Flask, abort, request, jsonify
from pymongo import MongoClient
import datetime
client = MongoClient('localhost', 27017)
db = client.restapi
app = Flask(__name__)

@app.route('/api/get_posts/', methods=['GET'])
def check_posts():
    a = list(db.posts.find())
    return jsonify(a)


@app.route('/api/check_in/', methods=['POST'])
def create_user():
    content = request.json
    if len(content["email"]) <= 0 or len(content["username"]) <= 0 or len(content["password"]) <= 0:
        abort(400)
    else:
        result_email = db.users.find_one({'email': content['email']})
        print(result_email)
        if content['email'] not in result_email:
            result_username = db.users.find_one({'username': content['username']})['username']
            if not result_username:
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