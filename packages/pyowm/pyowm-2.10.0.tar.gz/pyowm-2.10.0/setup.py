#!/usr/bin/env python

from setuptools import setup
from pyowm import constants

setup(
    name='pyowm',
    version=constants.PYOWM_VERSION,
    description='A Python wrapper around OpenWeatherMap web APIs',
    author='Claudio Sparpaglione (@csparpa)',
    author_email='csparpa@gmail.com',
    url='http://github.com/csparpa/pyowm',
    packages=['pyowm',
              'pyowm.abstractions',
              'pyowm.agroapi10',
              'pyowm.alertapi30',
              'pyowm.caches',
              'pyowm.commons',
              'pyowm.exceptions',
              'pyowm.pollutionapi30', 'pyowm.pollutionapi30.xsd',
              'pyowm.uvindexapi30', 'pyowm.uvindexapi30.xsd',
              'pyowm.tiles',
              'pyowm.utils',
              'pyowm.weatherapi25', 'pyowm.weatherapi25.cityids', 'pyowm.weatherapi25.parsers', 'pyowm.weatherapi25.xsd',
              'pyowm.stationsapi30', 'pyowm.stationsapi30.parsers', 'pyowm.stationsapi30.xsd'],
    long_description="""PyOWM is a client Python wrapper library for OpenWeatherMap web APIs. It allows quick and easy 
    consumption of OWM data from Python applications via a simple object model and in a human-friendly fashion.""",
    include_package_data=True,
    install_requires=[
        'requests>=2.20.0,<3',
        'geojson>=2.3.0,<3'
    ],
    python_requires='>=3.4',
    classifiers=[
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.4",
      "Programming Language :: Python :: 3.5",
      "Programming Language :: Python :: 3.6",
      "Programming Language :: Python :: 3.7",
      "Natural Language :: English",
      "Operating System :: OS Independent",
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "Topic :: Software Development :: Libraries"],
    package_data={
        '': ['*.gz', '*.xsd', '*.md', '*.txt', '*.json']
    },
    keywords='openweathermap web api client weather forecast uv alerting owm pollution meteostation agro agriculture',
    license='MIT'
)
