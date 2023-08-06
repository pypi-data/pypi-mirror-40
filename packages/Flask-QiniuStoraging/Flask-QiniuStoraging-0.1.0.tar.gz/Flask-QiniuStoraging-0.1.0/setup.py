# coding: utf-8
from setuptools import setup

setup(
    name='Flask-QiniuStoraging',
    version='0.1.0',
    url='https://github.com/stravel611/flask_qiniustoraging',
    license='MIT',
    author='Yilin Liu',
    author_email='liuyilin611@qq.com',
    description='Qiniu object storage for flask',
    long_description='See https://github.com/stravel611/flask_qiniustoraging',
    platforms='any',
    py_modules=['flask_qiniustoraging'],
    zip_safe=False,
    test_suite='tests',
    include_package_data=True,
    install_requires=[
        'Flask',
        'qiniu'
    ],
    keywords='flask extension qiniu',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
