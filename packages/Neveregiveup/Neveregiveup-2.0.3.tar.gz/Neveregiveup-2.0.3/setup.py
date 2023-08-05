from distutils.core import setup
with open('README.rst') as file:
    readme=file.read()
setup(
    name='Neveregiveup',
    version='2.0.3',
    packages=['wargame'],
    url='http://localhost:8090/simple',
    license='LICENSE.txt',
    description='test pkg private',
    long_description=readme,
    author='huyahao',
    author_email="1509232028@qq.com"
)