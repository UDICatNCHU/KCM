from distutils.core import setup

setup(
    name = 'KCM',
    packages = ['KCM'],
    package_data={'KCM':['*.*', 'WikiRaw/*', 'WikiRaw/preprocess_lib/*', 'build/*', 'install/*', 'langConfig/*', 'test/*']},
    version = '1.5',
    description = 'A API which will return Course of specific Dept. and also Course which you can enroll at that time.',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/UDICatNCHU/KCM',
    download_url = 'https://github.com/UDICatNCHU/KCM/archive/v1.5.tar.gz',
    keywords = ['nlp', 'keyword', 'correlation'],
    classifiers = [],
    install_requires=[
        'djangoApiDec',
        'jieba',
        'nltk==3.2.1',
        'numpy==1.11.2',
        'pathlib==1.0.1',
        'pyprind==2.9.9',
        'pymongo',
        'udicOpendata'
    ],
    zip_safe=True
)
