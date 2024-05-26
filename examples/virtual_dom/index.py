from flask import Flask, send_file, render_template
from zenaura.main import router, counters_page
from zenaura.routes import ClientRoutes
from zenaura.server import ZenauraServer


router
app = Flask(__name__,
            static_folder="zenaura"
            )

@app.route(ClientRoutes.counter.value)
@app.route(ClientRoutes.home.value)
def root():
    return send_file('zenaura/index.html')


@app.route('/ssr')
def ssr():    
    # Render the main HTML template with the rendered component
    return ZenauraServer.render(counters_page)


if __name__ == "__main__":
    app.run()