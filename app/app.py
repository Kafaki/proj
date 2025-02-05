from flask import Flask
from route import app_route

app = Flask(__name__)
app.register_blueprint(app_route)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)