# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
    name='ege_theme',
    description='EGE Theme',
    long_description='EGE Theme',
    license='MIT',
    author='Luiz Antonio Freitas de Assis',
    author_email='luizvpc@gmail.com',
    packages=['ege_theme', 'ege_theme/migrations', 'ege_theme/static', 'ege_theme/templates', 'ege_theme/templatetags'],
    include_package_data=True,
    version='0.5.1',
    download_url='https://github.com/CoticEaDIFRN/ege_theme/releases/tag/0.5.1',
    url='https://github.com/CoticEaDIFRN/ege_theme',
    keywords=['EGE', 'JWT', 'Django', 'Auth', 'SSO', 'client', ],
    # install_requires=['PyJWT==1.7.1', 'requests==2.21.0', 'django>=2.0,<3.0'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)

