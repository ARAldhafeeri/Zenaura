# Zenaura CLI Guide

The Zenaura CLI tool simplifies the process of creating, building, and running Zenaura projects. This guide will walk you through the basic commands and functionalities provided by the Zenaura CLI.

## Installation

Zenaura cli comes out of the box with zenaura framework:
```
pip install zenaura
```


## CLI Commands

The Zenaura CLI provides three main commands: `init`, `build`, and `run`.

### init

The `init` command sets up a new Zenaura project with the necessary structure and files.

```sh
zenaura init
```

This command creates a `public` directory with initial files and folders, including:

- `components.py`
- `presentational.py`
- `main.py`
- `routes.py`
- `config.json`
- `index.html`
- `main.css`
- `__init__.py`

It also creates two additional files in the project root:

- `build.py`
- `index.py`

### build

The `build` command runs the `build.py` script to prepare your project for deployment.

```sh
zenaura build
```

### run

The `run` command starts the development server using the `index.py` script.

```sh
zenaura run
```

## Example Workflow

Here is an example of a typical workflow using the Zenaura CLI:

1. **Initialize a new project**:
    ```sh
    zenaura init
    ```

2. **Build the project**:
    ```sh
    zenaura build
    ```

3. **Run the project**:
    ```sh
    zenaura run
    ```

## Notes

- **Hot-reloading**: The hot-reloading feature is currently under development. To ensure your changes are reflected in the browser, use the `build` command before running the project.
- **Python Versions**: Ensure you are using a compatible Python version with Zenaura and the required packages.

By following this guide, you can efficiently manage your Zenaura projects using the CLI tool. Enjoy building dynamic and interactive UIs with Zenaura!