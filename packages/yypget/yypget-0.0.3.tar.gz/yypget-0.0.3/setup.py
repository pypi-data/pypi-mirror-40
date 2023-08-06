import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "yypget",
    version = "0.0.3",
    author = "ysouyno",
    author_email = "ysouyno@163.com",
    description = "Download videos, documents, etc. from the website",
    license = "MIT",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ysouyno/yypget",

    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages = setuptools.find_packages('src'),
    package_dir = {'': 'src'},

    entry_points = {
        'console_scripts': 'yypget = yypget.__main__:main'
    }
)
