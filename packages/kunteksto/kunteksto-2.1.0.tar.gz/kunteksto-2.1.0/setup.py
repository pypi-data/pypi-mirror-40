from setuptools import setup

import configparser

config = configparser.ConfigParser()
config.read('kunteksto.conf')
VERSION = config['SYSTEM']['version']

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kunteksto',
    version=VERSION,
    description='The tool to translate your CSV data files into RDF, XML and JSON with full semantics and syntactic validation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Timothy W. Cook',
    author_email='tim@datainsights.tech',
    url='https://datainsights.tech/',
    download_url='https://github.com/DataInsightsInc/Kunteksto/archive/' + VERSION + '.tar.gz',
    keywords=['context rdf xml machine learning data-centric semantic interoperability semantics'],
    tests_require=['pytest', ],
    setup_requires=['pytest-runner', ],
    python_requires='>=3.7',
    packages=['kunteksto'],
    package_dir={'kunteksto': 'kunteksto'},
    package_data={'docs': ['docs/*'], 'kunteksto': ['.flaskenv', 'kunteksto.sh', 'kunteksto.bat']},
    data_files=[('example_data', ['example_data/Demo.csv', 'example_data/Demo2.csv', 'example_data/Demo3.csv', 'example_data/Demo_info.pdf']),
                ('s3model', ['s3model/s3model_3_1_0.xsl', 's3model/s3model_3_1_0.xsd', 's3model/s3model_3_1_0.rdf', 's3model/s3model.owl', 's3model/dm-description.xsl']),
                ('catalogs', ['catalogs/Kunteksto_catalog.xml']),
                ('', ['kunteksto.conf', 'README.md', 'LICENSE.txt']),
                ('utils', ['utils/datastats.py', 'utils/db_setup.py'])],
    install_requires=[
        'agraph-python',
        'basexclient',
        'click',
        'requests',
        'lxml',
        'shortuuid',
        'sphinx',
        'sphinx-rtd-theme',
        'ujson',
        'xmltodict',
        'cuid',
        'flask',
        'flask-admin',
        'flask-sqlalchemy',
        'flask-babelex',
        'sqlalchemy-utils',
        'python-dotenv'
      ],
    entry_points='''
            [console_scripts]
            kunteksto=kunteksto.kunteksto:main
        ''',
    classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Customer Service',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Education',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Financial and Insurance Industry',
                   'Intended Audience :: Healthcare Industry',
                   'Intended Audience :: Information Technology',
                   'Intended Audience :: Legal Industry',
                   'Intended Audience :: Manufacturing',
                   'Intended Audience :: Other Audience',
                   'Intended Audience :: Religion',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: System Administrators',
                   'Intended Audience :: Telecommunications Industry',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python :: 3 :: Only',
                   'Topic :: Scientific/Engineering :: Information Analysis',
                 ],

)
