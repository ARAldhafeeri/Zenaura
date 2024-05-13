from flask import Flask, send_file

from .zenaura.routes import ClientRoutes

app = Flask(__name__,
            static_folder="zenaura"
            )

@app.route(ClientRoutes.counter.value)
@app.route(ClientRoutes.home.value)
def root():
    return send_file('zenaura/index.html')