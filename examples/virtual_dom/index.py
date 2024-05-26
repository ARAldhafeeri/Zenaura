from flask import Flask, send_file, render_template
from public.main import router, counters_page
from public.routes import ClientRoutes
from zenaura.server import ZenauraServer

app = Flask(__name__,
            static_folder="public"
            )

@app.route(ClientRoutes.counter.value)
@app.route(ClientRoutes.home.value)
def root():
    return send_file('public/index.html')


@app.route('/ssr')
def ssr():    
    # Render the main HTML template with the rendered component
    return ZenauraServer.render(counters_page)


if __name__ == "__main__":
    app.run()