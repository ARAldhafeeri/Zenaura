import argparse
import os
import shutil
import json
from datetime import datetime
from zenaura import version, zenaura_logger

config = {
    "type": "app",
    "schema_version": 1,
    "runtimes": [],
    "interpreters": [
        {
            "src": "https://cdn.jsdelivr.net/pyodide/dev/full/",
            "name": "pyodide-0.22.1",
            "lang": "python"
        }
    ],
    "packages": [
        "zenaura=={version}"
    ],
    "fetch": [
        {
            "files": [
                "./public/main.py"
            ]
        }
    ],
    "plugins": [],
    "pyscript": {
        "version": "2022.12.1.dev",
        "time": datetime.utcnow().isoformat() + "Z"
    }
}

# Inject the version dynamically

config["packages"] = [pkg.format(version=version) for pkg in config["packages"]]

config = json.dumps(config, indent=4)

main  = """from zenaura.client.app import Route, App
from zenaura.client.page import Page
from zenaura.client.component import Component
from zenaura.ui import div, h1, h2, img

class ZenauraStarter(Component):
    def render(self):
        return div(
            div(
                img(src="./public/logo.png", width=255, height=255, alt="starterLogo"),
                h1("The Python Framework For"),
                h2("Building Modern Web User Interface"),
            ),
            class_="zenaura"
        )
    
starter = ZenauraStarter()

# App and routing
app = App()
home_page = Page([starter])

app.add_route(Route(
    title="Developer-Focused | Zenaura",
    path="/",
    page=home_page
))

app.run()
"""

index_html = """<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="./public/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="title" content="zenaura" />
    <meta http-equiv="refresh"  />
    <meta
      name="description"
      content="this app is made with zenaura"
    />
    <script type="module" src="https://pyscript.net/releases/2024.1.1/core.js"></script>
 
	<script type="py" src="./public/main.py" config="./public/config.json"></script>

    <link  rel="stylesheet" href="./public/main.css">

    <title>zenaura</title>
    
  </head>
  <body>
    <div id="root">
    </div>
  
  </body>

</html>

"""

main_css = """.zenaura{
  text-align: center;
}"""


build_file = '''
from zenaura.server import ZenauraServer
from public.main import app

ZenauraServer.hydrate_app(app, scripts=[
        """
        <script>
            const ws = new WebSocket("ws://localhost:5000/refresh");
            ws.onmessage = () => {
            console.log("Reloading...");
            location.reload();
            };
        </script>
        """
])

'''

index_file = '''import logging
from flask import render_template, Flask
from zenaura.server import DevServer

app = Flask(__name__, static_folder="public", template_folder="public")

DEVSERVER = DevServer(app, port=5000, debug=True)

@DEVSERVER.app.route("/")
def root():
    try:
        return render_template("index.html")
    except Exception as e:
        logging.info(f"Error rendering template: {e}")
        return "An error occurred.", 500

if __name__ == "__main__":
    DEVSERVER.run()
'''