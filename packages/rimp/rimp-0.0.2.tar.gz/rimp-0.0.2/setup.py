from setuptools import setup

try:
    with open('README.md') as f:
        long_desc = f.read()
except FileNotFoundError:
    long_desc = "See pypi project for information"

try:
    with open('requirements.txt') as f:
        requires = f.read().splitlines()
except FileNotFoundError:
    requires = ['requests', 'beautifulsoup4']

setup(
    name="rimp",
    version="0.0.2",
    url="https://github.com/Zwork101/rimp",
    description="A hacky project that lets you import repls from https://repl.it into your project",
    long_description=long_desc,
    author="Nathan Zilora",
    author_email="zwork101@gmail.com",
    requires=requires,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Archiving :: Packaging'
    ]
)
