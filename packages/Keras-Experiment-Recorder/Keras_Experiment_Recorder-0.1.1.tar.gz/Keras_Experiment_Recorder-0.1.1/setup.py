import os
import pathlib
from setuptools import setup
from setuptools import find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='Keras_Experiment_Recorder',

      version='0.1.1',
      description='A keras extension (callback) to record details of a training task',
      long_description=README,
      long_description_content_type="text/markdown",
      author='Kapil Sachdeva',
      author_email='notanemail@gmail.com',
      url='https://github.com/ksachdeva/keras-experiment-recorder.git',
      license='Apache-2.0',
      install_requires=[],
      extras_require={
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      packages=['keras_experiment_recorder'])
