from flask import Flask, send_file
from zenaura.main import router
from zenaura.routes import ClientRoutes


router
app = Flask(__name__,
            static_folder="zenaura"
            )

@app.route(ClientRoutes.counter.value)
@app.route(ClientRoutes.home.value)
def root():
    return send_file('zenaura/index.html')

if __name__ == "__main__":
    app.run()