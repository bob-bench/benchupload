try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Collect xUnit xml files and upload them to bob-bench.org',
    'author': 'Holger Hans Peter Freyther',
    'url': 'http://www.bob-bench.org',
    'download_url': 'http://www.bob-bench.org',
    'author_email': 'help@bob-bench.org',
    'version': '7',
    'install_requires': [
        'jsonschema==2.6.0',
        'requests',
    ],
    'license': 'AGPLv3+',
    'packages': ['benchupload'],
    'scripts': [],
    'entry_points': {'console_scripts': [
                        'benchupload=benchupload.__main__:main',
                        'metricupload=metricupload.__main__:main']},
    'name': 'benchupload'
}

setup(**config)
