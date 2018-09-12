from flask import Flask
from flask_cors import CORS
from BlogPost import blog_post_api as bp_api

app = Flask(__name__)

# This allows us to abstract our independent endpoints
# for different functions within the api
app.register_blueprint(bp_api.blog_post_api)
cors = CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
