import main

from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


def Message(message: str, data: object = None, status: bool = True, ):
    return jsonify({
        "success": status,
        "message": message,
        "data": data
    })


@app.route('/api/v1/generate', methods=['POST'])
def generate():

    tag = request.form.get('tag')
    if not tag:
        return Message(f"Value of 'tag' is required.")

    count = request.form.get('count', default=5)

    print(f"Tag: {tag}")
    print(f"Count: {count}")
    videos = main.run(tag, count)

    return Message(message="bon voyage", data=videos)


if __name__ == '__main__':
    app.run()