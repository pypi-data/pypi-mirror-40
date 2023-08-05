from setuptools import setup


__version__ = '0.0.0'


setup(
    name='squabble',
    version=__version__,
    description='An extensible linter for SQL',
    author='Erik Price',
    url='https://github.com/erik/squabble',
    packages=['squabble'],
    entry_points={
        'console_scripts': [
            'squabble = squabble.__main__:main',
        ],
    },
    license='GPLv3+',
    install_requires=[
        'pglast==1.1',
        'docopt==0.6.2',
        'colorama==0.4.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: SQL'
    ]
)
