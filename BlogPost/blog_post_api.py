from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from flaskext.mysql import MySQL
from collections import defaultdict

blog_post_api = Blueprint('blog_post_api', __name__)


# Establish connection for database (this has to be closed manually)
def connection():
    mysql = MySQL()

    current_app.config['MYSQL_DATABASE_USER'] = 'root'
    current_app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
    current_app.config['MYSQL_DATABASE_DB'] = 'blog'
    current_app.config['MYSQL_DATABASE_HOST'] = 'localhost'

    mysql.init_app(current_app)

    conn = mysql.connect()
    cursor = conn.cursor()

    return conn, cursor


@blog_post_api.route("/api/blogpost", methods=['POST', 'GET'])
@cross_origin(origin="*", headers=['Content-Type', 'Authorization'])
def handle_blog_post():
    conn, cursor = connection()

    if request.method == 'POST':
        data = request.json
        post, date = data["blog_post"], data["date"]

        sql_statement = (
            "INSERT INTO POSTS (blog_post, date_posted) "
            "VALUES (%s, %s)"
        )
        cursor.execute(sql_statement, (post, date))

        json = jsonify({
            "data": {
                "blog_post": post,
                "date_posted": date
            },
            "status": "completed"
        })
    else:
        result = defaultdict()

        sql_statement = (
            "SELECT * FROM POSTS"
        )
        cursor.execute(sql_statement)

        for blog_post, date_posted in cursor:
            result[date_posted] = blog_post

        json = jsonify(result)

    conn.commit()
    conn.close()

    return json

