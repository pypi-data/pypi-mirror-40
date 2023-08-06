# coding: utf-8
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='mqtt-sentinel',
      version='0.8.0',
      description='Integration between MQTT and custom notification services.',
      url='https://github.com/caiovictormc/mqtt-sentinel',
      author='caiovictormc',
      author_email='caiovictormc@gmail.com',
      license='MIT',
      packages=['sentinel'],
      install_requires=[
        'paho-mqtt==1.4.0',
        'PyInquirer==1.0.3',
        'prompt_toolkit==1.0.14',
        'click==7.0',
        'colorama==0.4.1',
        'requests==2.21.0'
      ],
      long_description=long_description,
      long_description_content_type="text/markdown",
      include_package_data=True,
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Networking :: Monitoring'
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      entry_points={
        'console_scripts': ['msentinel=sentinel.cli:cli']
      },
      zip_safe=False)
