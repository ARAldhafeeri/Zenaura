from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='zenaura',
    version='0.15.11',
    description="Zenaura is an experimental Python library built upon PyScript, designed to empower Python developers to create stateful, component-based Single Page Applications (SPAs). By leveraging a virtual DOM implementation, Zenaura optimizes the performance, reactivity, responsiveness, and interactivity of web applications. This allows developers to build high-performance, dynamic web applications using familiar Python concepts and syntax.",
    author="Ahmed Rakan",
    author_email="ar.aldhafeeri11@gmail.com",
    packages=[
        'zenaura', 
        'zenaura.server', 
        'zenaura.client', 
        'zenaura.client.algorithm', 
        'zenaura.client.compiler', 
        'zenaura.client.hydrator', 
        'zenaura.client.observer', 
        'zenaura.client.tags', 
        'zenaura.client.dom', 
        'zenaura.client.dom.lifecycles', 
        'zenaura.cli', 
        'zenaura.ui', 
        "zenaura.web",
        "zenaura.mocks"

        ],
    install_requires=[
        'bleach==6.1.0'
    ],
    entry_points={
        "console_scripts": [
            "zenaura = zenaura.cli:main",
        ],
    },
    test_suite='tests',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
)