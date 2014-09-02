from setuptools import setup

setup(
    name='j2cli',
    version = '0.1',
    description='json + jinja2 template == file',
    url='https://github.com/tommyvn/j2cli',
    author='Tom van Neerijnen',
    author_email='tom@tomvn.com',
    packages=['j2ccli'],
    install_requires=['jinja2'],
    keywords='cli jinja2 template',
    license='Apache',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            'j2cli=j2cli:main',
        ],
    },
)
