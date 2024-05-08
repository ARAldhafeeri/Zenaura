from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='zenui',
    version='1.0.1',
    description="ZenUI is python framework that brings python zen into the UI world. Build scalable, stateful component-based, interactive SPA with nothing but TailwindCSS and pure Python, no HTML, no CSS, no JS. ",
    author="Ahmed Rakan",
    author_email="ar.aldhafeeri11@gmail.com",
    packages=['zenui'],
    install_requires=[
        # Add any dependencies here
    ],
    test_suite='tests',
    long_description=long_description,
    long_description_content_type="text/markdown",
)