import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'filemanip',
    version = '0.0.0',
    author = 'Dane Morgan',
    author_email = 'danemorgan91@gmail.com',
    description = 'a simple module to manipulate files, find and remove/replace flags, etc...',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/deadlift1226/filemanip',
    install_requires = [], #3rd party pip packages
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)


