#!/usr/bin/env python

from setuptools import setup

long_description = "placeholder"

VERSION = "1.0.0"

setup(name='buildbot-gitpull',
      version=VERSION,
      description='buildbot plugin for pulling repos (and subtrees).',
      author='Quentin POIRIER',
      author_email='quentin.poirier@opus-solutions.eu',
      url='https://github.com/placeholder',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['buildbot_gitpull'],
      requires=[
          "buildbot (>=2.0.0)"
      ],
      entry_points={
          "buildbot.steps": [
              "GitPull = buildbot_gitpull.pull:GitPull"
          ],
      },
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Plugins",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: MacOS",
          "Operating System :: POSIX :: Linux",
          "Topic :: Software Development :: Build Tools",
      ]
      )
