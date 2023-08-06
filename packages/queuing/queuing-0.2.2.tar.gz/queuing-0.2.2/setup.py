from setuptools import setup
import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name='queuing',
      version='0.2.2',
      description='Multithreating producent-consumer solution',
      long_description=README,
      long_description_content_type="text/markdown",
      url='https://github.com/vojtek/queuing',
      author='Wojciech Kolodziej',
      author_email='vojtekkol@o2.pl',
      license='MIT',
      packages=['queuing'],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ])
