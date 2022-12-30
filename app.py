from flask import Flask, request


app = Flask(__name__)
@app.route('/')
def requesta_data():
    return f"HOla, Estás usando {request.user_agent}"

if __name__ == '__main__':
    app.run(debug = True)  