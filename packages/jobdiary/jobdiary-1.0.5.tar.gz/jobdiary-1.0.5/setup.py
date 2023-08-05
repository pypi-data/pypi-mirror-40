import re

from setuptools import setup, find_packages


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='jobdiary',
      version=get_version('jobdiary/__init__.py'),
      description='A funny and easy to use job diary',
      long_description=readme(),
      license='MIT',
      author='Federico Barresi',
      author_email='fede.barresi@gmail.com',
      url='https://github.com/fbarresi/JobDiary',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      install_requires=[
        'setuptools',
        'tinydb',
        'huepy'],
      entry_points={
        'console_scripts': [
            'jd = jobdiary.__main__:main',
        ],
        },
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Terminals',
        'Topic :: Text Processing',
        'Topic :: Utilities'
        ]
      )
