import os
from io import open
from setuptools import setup, find_packages


# Load package info, without importing the package
basedir = os.path.dirname(os.path.abspath(__file__))
package_info_path = os.path.join(basedir, "hybrid", "package_info.py")
package_info = {}
try:
    with open(package_info_path, encoding='utf-8') as f:
        exec(f.read(), package_info)
except SyntaxError:
    execfile(package_info_path, package_info)


# Package requirements, minimal pinning
install_requires = ['six>=1.10', 'numpy', 'networkx', 'click>5', 'plucky>=0.4.3',
                    'dimod>=0.7.7,!=0.7.10', 'minorminer>=0.1.7', 'dwave-networkx>=0.6.6',
                    'dwave-system>=0.5.5', 'dwave-neal>=0.4.1', 'dwave-tabu>=0.1.3']

# Package extras requirements
extras_require = {
    'test': ['coverage'],

    # python2 backports
    ':python_version == "2.7"': ['futures']
}

setup(
    name=package_info['__packagename__'],
    version=package_info['__version__'],
    author=package_info['__author__'],
    author_email=package_info['__authoremail__'],
    description=package_info['__description__'],
    long_description=open('README.rst', encoding='utf-8').read(),
    url=package_info['__url__'],
    license=package_info['__license__'],
    packages=find_packages(),
    install_requires=install_requires,
    extras_require=extras_require,
)
