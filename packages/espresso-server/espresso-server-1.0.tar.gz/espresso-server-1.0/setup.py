import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='espresso-server',
    version='1.0',
    description="Espresso Server for MicroPython development boards",
    # description_file="README.rst",

    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',

    #url = 'http://www.pinguino.cc/',
    url='http://yeisoncardona.com/',
    download_url='http://bitbucket.org/espressoide',

    packages=find_packages(),
    install_requires=[
        # 'numpy',
        # 'sympy',
        # 'structure',
        # 'scipy',
        # 'matplotlib',
        # 'pybrain',
        'tornado==4.5.3',
        # 'shell',
        # 'pandas',
        # 'pillow',
        # 'sklearn',
        # 'mpld3',
        # 'jinja2',
    ],

    scripts=[
        "cmd/espresso",
    ],

    zip_safe=False,

    include_package_data=True,
    license='BSD License',

    classifiers=[
        'Environment :: Web Environment',
    ],
)
