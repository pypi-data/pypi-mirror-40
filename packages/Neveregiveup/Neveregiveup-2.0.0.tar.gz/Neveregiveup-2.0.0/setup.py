from distutils.core import setup
with open('README.rst') as file:
    readme=file.read()
setup(
    name='Neveregiveup',
    version='2.0.0',
    packages=['wargame'],
    url='https://testpypi.python.org/pypi/some_unique_name/',
    license='LICENSE.txt',
    description='my fantasy game',
    long_description=readme,
    author='huyahao',
    author_email="1509232028@qq.com"
)