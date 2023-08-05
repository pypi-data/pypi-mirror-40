from setuptools import setup

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

setup(
    name='mtg-proxyprint',
    version='1.0.6',
    packages=['proxyprint',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Simple command line tool to create MTG deck proxies',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/snapcaster/proxyprinter',
    author='Michael Sobczak',
    author_email='michaelsobczak54@gmail.com',
    entry_points={
        'console_scripts': [
            'proxyprint=proxyprint.print_proxy:main'
        ]
    },
    install_requires=parse_requirements('requirements.txt'),
    include_package_data=True
)
