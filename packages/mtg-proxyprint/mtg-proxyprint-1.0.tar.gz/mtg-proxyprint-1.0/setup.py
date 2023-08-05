from distutils.core import setup

setup(
    name='mtg-proxyprint',
    version='1.0',
    packages=['proxyprint',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Simple command line tool to create MTG deck proxies',
    long_description=open('README.txt').read(),
    url='https://gitlab.com/snapcaster/proxyprinter',
    author='Michael Sobczak',
    author_email='michaelsobczak54@gmail.com',
    entry_points={
        'console_scripts': [
            'proxyprint=proxyprint.print_proxy:main'
        ]
    },
)
