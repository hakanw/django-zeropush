# encoding: utf-8
from setuptools import setup, find_packages
setup(
    name='django-zeropush',
    version='0.2.1',
    author=u'Håkan Waara',
    author_email='hwaara@gmail.com',
    packages=find_packages(),
    url='https://github.com/hakanw/django-zeropush',
    license='BSD licence, see LICENCE.txt',
    description='ZeroPush iOS push notifications support for django',
    #long_description=open('README.txt').read(),
    install_requires=['requests'],
    zip_safe=False,
)
