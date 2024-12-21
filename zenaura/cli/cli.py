import argparse
import os
import shutil
import json
from datetime import datetime
from zenaura import version, zenaura_logger
from .files import main, config, index_html,main_css, build_file, index_file

init_content = {
    "main.py": main, 
    "config.json":config, 
    "index.html": index_html,
    "main.css": main_css,
    "__init__.py": "" 

}
def init_project():
    """Creates the initial Zenaura project structure."""
    # Create public directory and files
    zenaura_logger.info("Creating new zenaura project")
    public_dir = os.path.join(os.getcwd(), "public")
    script_dir = os.path.dirname(__file__)
    os.makedirs(public_dir, exist_ok=True)
    files = ["__init__.py", "main.py", "main.css", "index.html", "config.json"]
    static = ["favicon.ico", "logo.png"]
    for file in files:
        with open(os.path.join(public_dir, file), "w") as f:
            f.write(init_content[file])
            zenaura_logger.info(f"Created file - ${file}")

    for file in static:
        logo_path = os.path.join(script_dir, file)
        destination_path = os.path.join(public_dir, file) 

        # 3. Copy the file
        try:
            shutil.copy(logo_path, destination_path)
            zenaura_logger.info("Logo copied to current directory:", destination_path)
        except FileNotFoundError:
            zenaura_logger.info("Logo file not found.")
        except PermissionError:
            zenaura_logger.info("Insufficient permissions to copy the logo.")  


    # Create build.py and index.py files

    build_file_path = os.path.join(os.getcwd(), "build.py")
    index_file_path = os.path.join(os.getcwd(), "index.py")
    with open(build_file_path, "w") as f:
        f.write(build_file)
        zenaura_logger.info("created build.py")
        
    with open(index_file_path, "w") as f:
        zenaura_logger.info("created index.py")
        f.write(index_file)

    zenaura_logger.info("Zenaura project initialized successfully!")

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