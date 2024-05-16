from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='zenaura',
    version='0.9.33',
    description="Zenaura, light weight, super fast python full-stack development framework, in which every line of code emit the aura of python zen, build interactive SPA with pure Python, create secure and scalable endpoints.",
    author="Ahmed Rakan",
    author_email="ar.aldhafeeri11@gmail.com",
    packages=['zenaura'],
    install_requires=[
        # Add any dependencies here
    ],
    test_suite='tests',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
