from setuptools import setup
import glob
import os

with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if not x.startswith("#")]

from cli import __version__, _program

setup(name=_program,
      version=__version__,
      packages=['cli'],
      description='Skeleton commandline python project with analytics and export support',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/danielecook/python-cli-skeleton',
      author='YOUR NAME',
      author_email='youremail@email.com',
      license='MIT',
      install_requires=required,
      entry_points="""
      [console_scripts]
      {program} = cli.command:main
      """.format(program = _program),
      keywords=['cli', 'analytics', 'export', 'statistics'],
      tests_require=['pytest', 'coveralls', 'six'],
      zip_safe=False)
