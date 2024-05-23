from flask import Flask, send_file
from zenaura.main import router
from zenaura.routes import ClientRoutes
from zenaura.client.component import  persist_server_cache


app = Flask(__name__,
            static_folder="zenaura"
            )

@app.route(ClientRoutes.counter.value)
@app.route(ClientRoutes.home.value)
def root():
    return send_file('zenaura/index.html')

if __name__ == "__main__":
    persist_server_cache()
    app.run()