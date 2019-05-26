import setuptools

with open('README.md','r') as f:
    long_description = f.read()
setuptools.setup(
    name = 'lazyplotly',
    version = '0.1',
    author = 'chuboy',
    description = '',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/billju/lazyplotly',
    #packages = setuptools.find_packages(),
    scripts = ['lazyplotly']
)
#python setup.py sdist bdist_wheel
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#twine upload dist/*