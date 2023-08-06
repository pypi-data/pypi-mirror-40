import re
from os.path import join, dirname
from setuptools import setup, find_packages

package_name = 'microhttp_auth'

# Reading package's version
with open(join(dirname(__file__), package_name, '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(
        v_file.read()
    ).group(1)

setup(
    name=package_name,
    version=package_version,
    author='Mahdi Ghanea.g',
    description='Role based JWT stateless/ful authentication '
                'module for microhttp',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    install_requires=[
        'microhttp',
        'user-agents',
        'ujson',
        'redis',
        'pyjwt'
    ],
    license='MIT License',
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
