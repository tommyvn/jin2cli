from setuptools import setup

setup(
    name='jin2cli',
    version = '0.1',
    description='json + jinja2 template == file',
    url='https://github.com/tommyvn/jin2cli',
    author='Tom van Neerijnen',
    author_email='tom@tomvn.com',
    packages=['jin2cli'],
    install_requires=['jinja2'],
    keywords='cli jinja2 template',
    license='Apache',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        'console_scripts': [
            'jin2cli=jin2cli:main',
        ],
    },
)
