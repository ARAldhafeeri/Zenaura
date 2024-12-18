# Zenaura

> [!WARNING]
> This library is under development, it's going to change a lot from now on; breaking changes may occur. Please keep an eye on release notes.

> [!NOTE]
> Contribution is open , awesome features in the backlog so if you are intrested my email is linked to this profile.

<img title="a title" alt="Alt text" src="./assets/logo.png" width="300" height="300" />

Zenaura is a Python library built on top Pydide, PyScript, designed to empower Python developers to create light-weight, performant, stateful, component-based Single Page Applications (SPAs). By leveraging a virtual DOM implementation, Zenaura optimizes the performance, reactivity, responsiveness, and interactivity of web applications. This allows developers to build high-performance, dynamic web applications using familiar Python concepts and syntax.

# Documentation

<a href="https://araldhafeeri.github.io/Zenaura/" target="_blank"> Zenaura documentation and API reference</a>

note: hot-reloading is still under-development, it works, however working with cli, zenaura build after every change is better.

# Installing zenaura

### prerequisits:

- Python 3.11 or above.
- pip
- devolopment server requirements:
  - flask==2.3.3
  - watchdog==4.0.1
  - flask-sock==0.7.0

```bash
pip install zenaura flask==2.3.3 watchdog==4.0.1 flask-sock==0.7.0
```

This command will install zenaura library, client and server, CLI.

# Creating your first zenaura app

In this example we will go over creating your first zenaura application, go over basic concepts as well.

Once you installed the library, the library, it comes with simple CLI tool.

#### CLI Commands:

    - init: Will create simple zenaura application
    - build : Will build the application
    - run : Will run the development server

First let's initials a basic zenaura application:

```bash
zenaura init
```

This command will auto generate basic zenaura application with the needed files auto generated for you, so you can get up to speed with the library.

### Auto generated files from init command:

- build.py : used for building zenaura application.
- index.py : simple zenaura server.
- public/components.py: single zenaura component.
- public/presentational.py: few zenaura presentational components created using builder interface.
- public/main.py : main file where we import components, create pages and configure the client router.
- public/routes.py : where your client side routes lives.
- public/main.css : the main css file.
- public/config.json: pyscript pydide configuration.

### Building zenaura

```bash
zenaura build
```

This command will build index.html.

### Running zenaura

```bash
zenaura run
```

This command will run the development server. Now open browser tab and go to localhost:5000.
