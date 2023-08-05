from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='boundio',
    version='0.0.2',
    author='A1Liu',
    author_email='albertymliu@gmail.com',
    description='A toolkit for IO-bound applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/a1liu/boundio',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'aiofiles', 'websockets', 'aiohttp', 'cchardet', 'aiodns'
        ]
)
