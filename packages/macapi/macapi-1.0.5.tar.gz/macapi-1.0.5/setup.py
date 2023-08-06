#!bin/python

"""Setup tool for macapi."""

from setuptools import setup

# import versions.py for versions display
with open('macapi/version.py') as f:
    exec(f.read())

# import readme.rst long_description file content to be displayed
with open('README.rst') as f:
    long_description = f.read()

packages = ['macapi',
            'macapi.alerts',
            'macapi.ipwhitelist',
            'macapi.cluster'
            ]

setup(name='macapi',
      entry_points={
          'console_scripts': [
              'alerts=macapi.alerts.alerts:main',
              'ipwhitelist=macapi.ipwhitelist.ipwhitelist:main',
              'cluster=macapi.cluster.cluster:main'
          ],
      },
      #scripts=['bin/alerts'],
      version=__version__,
      long_description=long_description,
      url='https://github.com/dmcna005/macapi',
      author='Dwayne McNab',
      author_email='dmcnab@imperiadata.com',
      description=("scripts written to interact with mongodb cloud api"),
      license='Apache 2.0',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database :: Database Engines/Servers',
        'Intended Audience :: Developers'
      ],
      packages=packages,
      install_requires=['requests'],
      zip_safe=False)
