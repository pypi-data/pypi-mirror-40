from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='mopidyartfetch',
    version='0.1',
    description='Fetch album art for various mopidy uri types',
    url='http://github.com/sharktamer/mopidy-art-fetch',
    author='Shane Donohoe',
    author_email='donohoe.shane@gmail.com',
    license='GPL',
    packages=['mopidyartfetch'],
    install_requires=['feedparser'],
    long_description=readme(),
    include_package_data=True
)
