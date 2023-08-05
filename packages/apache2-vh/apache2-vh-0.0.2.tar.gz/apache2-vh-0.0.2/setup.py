from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='apache2-vh',
    version='0.0.2',
    description='Make your virtual host for apache2 automatically in ubuntu',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MNGemignani/apache2_virtual_host_creator',
    author='Mateus Gemignani',
    author_email='gemignaniholland@gmail.com',
    keywords='virtual-host apache2 magento2',
    packages=['vh'],
    install_requires=['argparse'],
    scripts=['bin/vh']
)
