from setuptools import setup

setup(
    name='teach_SR',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_login',
        'flask_sqlalchemy',
        'wtforms'
    ],
)