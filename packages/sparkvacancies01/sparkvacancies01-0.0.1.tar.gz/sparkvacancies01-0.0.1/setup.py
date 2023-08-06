from setuptools import setup, find_packages

PACKAGE = ""
NAME = "sparkvacancies01"
DESCRIPTION = "Collecting data about vacancies"
AUTHOR = "jjavadzade@yandex.ru"
AUTHOR_EMAIL = "jjavadzade@yandex.ru"
URL = ""
VERSION = "0.0.1"

with open("README.md", "r") as fh:
    DESCRIPTION = fh.read()
 
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description= DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    include_package_data=True,
    zip_safe=False,
)