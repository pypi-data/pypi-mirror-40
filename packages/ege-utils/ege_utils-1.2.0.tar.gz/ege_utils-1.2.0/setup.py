# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
    name='ege_utils',
    packages=['ege_utils', ],
    version='1.2.0',
    download_url='https://github.com/CoticEaDIFRN/ege_utils/releases/tag/1.2.0',
    description='Utils classes for EGE project',
    long_description='Utils classes for EGE project',
    author='Kelson da Costa Medeiros',
    author_email='kelsoncm@ifrn.edu.br',
    url='https://github.com/CoticEaDIFRN/ege_utils',
    keywords=['EGE', 'JWT', 'Django', 'Auth', 'SSO', 'client', ],
    install_requires=['PyJWT==1.7.1', 'requests==2.21.0', 'django>=2.0,<3.0'],
    classifiers=[]
)

