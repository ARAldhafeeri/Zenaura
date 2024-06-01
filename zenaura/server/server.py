import io
import logging
import subprocess
import time
from threading import Thread, Event
import asyncio
import contextlib
from zenaura.client.page import Page 
from zenaura.client.hydrator import HydratorCompilerAdapter
from zenaura.client.app import App 
from flask import Flask
from flask_sock import Sock
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO)
compiler_adapter = HydratorCompilerAdapter()

# create pyscript pydido template 
def template(content, meta_description=None, title=None, icon=None, pydide="https://pyscript.net/releases/2024.1.1/core.js", scripts=None):
  """
    This function generates the HTML structure of a Zenaura page.

    Args:
        content (str): The main content of the page, typically generated by compiling Zenaura components.
        meta_description (str, optional): A brief description of the page, used by search engines. Defaults to None.
        title (str, optional): The title of the page, displayed in the browser tab. Defaults to None.
        icon (str, optional): The URL of the favicon, a small icon associated with the page. Defaults to None.
        pydide (str, optional): The URL of the PyScript library, used for running Python code in the browser. Defaults to "https://pyscript.net/releases/2024.1.1/core.js".
        scripts (list, optional): An optional list of additional JavaScript scripts, CSS links to include in the page. Defaults to None.

    Returns:
        str: The complete HTML code as a string.
  """
  if scripts:
    s = io.StringIO()
    for script in scripts:
        s.write(script)
        s.write("\n")
    scripts = s.getvalue()
      
  return f"""

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="{icon}" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="title" content="{title}" />
    <meta http-equiv="refresh"  />
    <meta
      name="description"
      content="{meta_description}"
    />
    <script type="module" src="{pydide}"></script>
    {scripts if scripts else ""}
 
	<script type="py" src="./public/main.py" config="./public/config.json"></script>

    <link  rel="stylesheet" href="./public/main.css">

    <title>{title}</title>
    
  </head>
  <body>
    <div id="root">
        {content}
    </div>
  
  </body>

</html>
"""
class ZenauraServer:
    """
    A class for server-side rendering of Zenaura applications.

    This class provides methods for:

    * Hydrating Zenaura pages for server-side rendering.
    * Hydrating Zenaura apps for server-side rendering.
    * Generating the HTML structure of a Zenaura page.
    """

    @staticmethod
    def hydrate_page(page: Page, title="zenaura", meta_description="this app created with zenaura", icon="./public/favicon.ico", pydide="https://pyscript.net/releases/2024.1.1/core.js") -> str:
        """
        Hydrates a Zenaura page for server-side rendering.

        This method compiles the page's components using the HydratorCompilerAdapter and generates the HTML structure of the page.

        Args:
            page (Page): The Zenaura page to be hydrated.
            title (str, optional): The title of the page. Defaults to "zenaura".
            meta_description (str, optional): The meta description of the page. Defaults to "this app created with zenaura".
            icon (str, optional): The URL of the favicon. Defaults to "./public/favicon.ico".
            pydide (str, optional): The URL of the PyScript library. Defaults to "https://pyscript.net/releases/2024.1.1/core.js".

        Returns:
            str: The HTML structure of the hydrated page.
        """

        return template(compiler_adapter.hyd_comp_compile_page(page), meta_description, title, icon, pydide)

    @staticmethod
    def hydrate_app(app: App, title="zenaura", meta_description="this app created with zenaura", icon="./public/favicon.ico", pydide="https://pyscript.net/releases/2024.1.1/core.js", scripts=None) -> None:
        """
        Hydrates a Zenaura app for server-side rendering.

        This method renders all pages in the app, sets the page with path "/" to visible, and the rest to hidden. It then compiles the index.html file for server-side rendering.

        Args:
            app (App): The Zenaura app to be hydrated.
            title (str, optional): The title of the page. Defaults to "zenaura".
            meta_description (str, optional): The meta description of the page. Defaults to "this app created with zenaura".
            icon (str, optional): The URL of the favicon. Defaults to "./public/favicon.ico".
            pydide (str, optional): The URL of the PyScript library. Defaults to "https://pyscript.net/releases/2024.1.1/core.js".
            scripts (list, optional): An optional list of additional JavaScript scripts and CSS links to include in the page. Defaults to None.
        """

        pages = io.StringIO()

        # Render pages
        for path, route in app.routes.items():
            page, _, _, ssr = route
            if ssr:  # Ignore SSR pages
                continue
            if path == "/":  # Set / route to visible
                page_div = lambda comps: f'<div data-zenaura="{page.id}">{comps}</div>'
                pages.write(page_div(compiler_adapter.hyd_comp_compile_page(page)))
                continue
            # Pages other than / are set to hidden
            page_div = lambda comps: f'<div hidden data-zenaura="{page.id}">{comps}</div>'
            pages.write(page_div(compiler_adapter.hyd_comp_compile_page(page)))

        pages = pages.getvalue()

        # Overwrite in public dir
        with open("./public/index.html", "w") as file:
            file.write(template(pages, meta_description, title, icon, pydide, scripts))


class PausingObserver(Observer):
    def dispatch_events(self, *args, **kwargs):
        if not getattr(self, '_is_paused', False):
            super(PausingObserver, self).dispatch_events(*args, **kwargs)

    def pause(self):
        self._is_paused = True

    def resume(self):
        time.sleep(self.timeout)  # allow interim events to be queued
        self.event_queue.queue.clear()
        self._is_paused = False

    @contextlib.contextmanager
    def ignore_events(self):
        self.pause()
        yield
        self.resume()

class DevServer:
    """
    A class for running a development server for Zenaura applications.

    This class provides methods for:

    * Starting a Flask server with WebSocket support.
    * Sending refresh signals to connected clients when changes are detected.
    * Hydrating the application and notifying clients when changes are made.
    * Running a file system observer to detect changes in the application files.
    """

    def __init__(self, app, debug=True, port=5000):
        """
        Initializes the DevServer class.

        Args:
            debug (bool, optional): Whether to run the server in debug mode. Defaults to True.
            port (int, optional): The port on which to run the server. Defaults to 5000.
        """

        self.debug = debug
        self.port = port
        self.app = app
        self.sock = Sock()
        self.ws_client_list = []
        self.shutdown_event = Event()
        self.observer = PausingObserver()
        self.sock.init_app(self.app)
        self.loop = asyncio.new_event_loop()

        self.setup_websocket()

    def setup_websocket(self):
        """
        Sets up the WebSocket route for sending refresh signals to clients.
        """

        @self.sock.route("/refresh")
        def refresh(ws):
            """
            WebSocket handler for sending refresh signals to clients.

            Args:
                ws (WebSocket): The WebSocket connection.
            """

            self.ws_client_list.append(ws)
            while not self.shutdown_event.is_set():
                try:
                    ws.receive()
                    ws.sleep(1)
                    ws.send("refresh")
                except Exception as e:
                    print(f"Error in WebSocket connection: {e}")
                    break

    def send_refresh_signal(self):
        """
        Sends a refresh signal to all connected clients.
        """

        logging.info("Sending refresh signal...")
        clients = self.ws_client_list.copy()
        for client in clients:
            try:
                client.send("refresh")
            except Exception as e:
                print(f"Error sending refresh: {e}")
                self.ws_client_list.remove(client)

    def get_change_handler(self):
        """
        Returns a ChangeHandler class that handles file system events.

        Returns:
            ChangeHandler: A class that handles file system events.
        """

        DEVSERVER = self

        class ChangeHandler(FileSystemEventHandler):
            """
            A class that handles file system events.

            This class is used to detect changes in the application files and trigger a refresh of the browser.
            """

            def __init__(self, server):
                """
                Initializes the ChangeHandler class.

                Args:
                    server (DevServer): The DevServer instance.
                """

                super().__init__()
                self.server = server

            def on_any_event(self, event):
                """
                Handles file system events.

                Args:
                    event (FileSystemEvent): The file system event.
                """

                try:
                    logging.info(f"File {event.src_path} has changed.")
                    logging.info("Changes are live...")
                    DEVSERVER.hydrate_and_notify()
                    logging.info("Reloading browser...")
                    DEVSERVER.send_refresh_signal()
                    logging.info("Browser reloaded.")
                except Exception as e:
                    logging.info(f"Error in ChangeHandler: {e}")

        return ChangeHandler

    def start_server(self):
        """
        Starts the Flask server.
        """

        try:
            self.app.run(debug=self.debug, port=self.port, use_reloader=False)
        except Exception as e:
            logging.info(f"Error starting server: {e}")

    def hydrate_and_notify(self):
        """
        Hydrates the application and notifies clients of changes.
        """

        try:
            self.observer.pause()
            logging.info("Hydrating...")
            logging.info("Pausing the observer...")
            process = subprocess.Popen("python build.py", shell=True)
            process.communicate()
            logging.info("Hydrated done...")

        finally:
            logging.info("Running the observer...")
            self.observer.resume()

    def run(self):
        """
        Runs the development server.

        This method starts the Flask server, file system observer, and WebSocket server.
        """

        path = 'public'
        ChangeHandler = self.get_change_handler()
        event_handler = ChangeHandler(self)
        self.observer.schedule(event_handler, path, recursive=True)
        self.observer.start()

        server_thread = Thread(target=self.start_server, daemon=True)
        server_thread.start()

        try:
            while not self.shutdown_event.is_set():
                time.sleep(0.1)  # Shorter sleep interval
        except KeyboardInterrupt:
            logging.info("KeyboardInterrupt received, stopping...")
        finally:
            # Faster Shutdown of Observer
            self.observer.event_queue.queue.clear()
            self.observer.stop()  
            self.observer.join()  