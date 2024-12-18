import argparse
import os
import shutil
init_content = {


    "components.py": """from zenaura.client.component import Component
from public.presentational import * 


class ZenauraStarter(Component):
    def render(self):
        return Div("zenaura", [
           Div("", [
            Image("./public/logo.png", "zenaura", "255", "255", "starterLogo"),
            Header1("The Python Library For"),
            Header1("Building Modern Web User Interface")
           ])
        ])
""",


    "presentational.py": """from zenaura.client.tags.builder import Builder

def Div(class_name, children):
    div = Builder('div').with_attribute('class', class_name).build()
    div.children = children
    return div

def Image(src, alt, width, height, classname=""):
    return Builder("img").with_attributes(
        src=src,
        alt=alt,
        width=width,
        height=height,
    ).with_attribute("class", classname).build()

def Header1(text):
    return Builder('h1').with_text(text).build()
""",


    "main.py": """from zenaura.client.app import Route, App
from zenaura.client.page import Page
from public.routes import ClientRoutes
from public.components import ZenauraStarter

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

""", 


    "routes.py": """from enum import Enum

class ClientRoutes(Enum):
    home="/"
""", 

    "config.json": """{
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
      "zenaura==0.9.94"
    ],
    "fetch": [
      {
        "files": [
          "./public/routes.py",
          "./public/components.py",
          "./public/presentational.py",
          "./public/data.py",
          "./public/constants.py"
        ]
      }
    ],
    "plugins": [],
    "pyscript": {
      "version": "2022.12.1.dev",
      "time": "2024-04-29T20:57:07.199Z"
    }
  }
""", 

    "index.html": """<html lang="en">
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

""",

    "main.css": """.zenaura{
  text-align: center;
}

""", 
    "__init__.py": "" 

}

build_file_init = '''
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

index_file_init = '''import logging
from flask import render_template, Flask
from public.routes import ClientRoutes
from zenaura.server import DevServer

app = Flask(__name__, static_folder="public", template_folder="public")

DEVSERVER = DevServer(app, port=5000, debug=True)

@DEVSERVER.app.route(ClientRoutes.home.value)
def root():
    try:
        return render_template("index.html")
    except Exception as e:
        logging.info(f"Error rendering template: {e}")
        return "An error occurred.", 500

if __name__ == "__main__":
    DEVSERVER.run()
'''
def init_project():
    """Creates the initial Zenaura project structure."""
    # Create public directory and files
    public_dir = os.path.join(os.getcwd(), "public")
    script_dir = os.path.dirname(__file__)
    os.makedirs(public_dir, exist_ok=True)
    files = ["__init__.py", "components.py", "main.py", "main.css", "index.html", "presentational.py", "routes.py", "config.json"]
    static = ["favicon.ico", "logo.png"]
    for file in files:
        with open(os.path.join(public_dir, file), "w") as f:
            f.write(init_content[file])

    for file in static:
        logo_path = os.path.join(script_dir, file)
        destination_path = os.path.join(public_dir, file) 

        # 3. Copy the file
        try:
            shutil.copy(logo_path, destination_path)
            print("Logo copied to current directory:", destination_path)
        except FileNotFoundError:
            print("Logo file not found.")
        except PermissionError:
            print("Insufficient permissions to copy the logo.")  


    # Create build.py and index.py files

    build_file = os.path.join(os.getcwd(), "build.py")
    index_file = os.path.join(os.getcwd(), "index.py")
    with open(build_file, "w") as f:
        f.write(build_file_init)
    with open(index_file, "w") as f:
        f.write(index_file_init)

    print("Zenaura project initialized successfully!")

def build_project():
    """Runs the build.py script."""
    os.system("python build.py")  # Adjust if build.py is elsewhere

def run_project():
    """Runs the index.py script."""
    os.system("python index.py")  # Adjust if index.py is elsewhere

def main():
    parser = argparse.ArgumentParser(description="Zenaura CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Create a new project")
    build_parser = subparsers.add_parser("build", help="Build the project")
    run_parser = subparsers.add_parser("run", help="Run the project")

    args = parser.parse_args()

    if args.command == "init":
        init_project()
    elif args.command == "build":
        build_project()
    elif args.command == "run":
        run_project()
    else:
        parser.print_help()