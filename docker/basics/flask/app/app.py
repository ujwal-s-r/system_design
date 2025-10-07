from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_docker():
    return '<h1>Hello from your first Dockerized App!</h1>'

if __name__ == '__main__':
    # Note: Using 0.0.0.0 makes the server accessible from outside the container
    app.run(host='0.0.0.0', port=5000)