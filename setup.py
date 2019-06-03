import setuptools

with open('README.md','r') as f:
    long_description = f.read()
setuptools.setup(
    name = 'lazyplotly',
    version = '1.2',
    author = 'chuboy',
    description = '',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/billju/lazyplotly',
    #store project python in directory, and make an __init__.py to start
    packages = setuptools.find_packages(),
)
#pipenv shell
#pip install twine wheel
#python setup.py sdist bdist_wheel
#twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
#twine upload dist/*
