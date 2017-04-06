from setuptools import setup

setup(
    name = 'markslide',
    version = '0.1',
    author = 'verysure',
    license = 'MIT',
    install_requires = [
        'markdown',
        'pdfkit',
        'pyScss',
        'watchdog',
    ],
    packages = ['markslide'],
    package_dir = {'markslide': 'src'},
    package_data = {
        'markslide': ['../styles/*.*'],
    },
    scripts = ['bin/markslide'],
)
