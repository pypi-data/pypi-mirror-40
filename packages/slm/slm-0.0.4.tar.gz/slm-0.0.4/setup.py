from setuptools import setup

version = '0.0.4'

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='slm',
    packages=[],
    scripts=['slm'],
    version=version,
    license='MIT',
    description='Seshat library manager.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='hardboiled65',
    author_email='hardboiled65@gmail.com',
    url='https://github.com/hardboiled65/slm',
    download_url='https://github.com/hardboiled65/slm/archive/v{}.tar.gz'.format(version),
    keywords=['c', 'c++'],
    install_requires=[
        'pyyaml',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
