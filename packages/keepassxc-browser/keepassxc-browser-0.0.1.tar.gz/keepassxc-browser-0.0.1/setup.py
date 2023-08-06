from setuptools import setup, find_packages

setup(name='keepassxc-browser',
      version='0.0.1',
      description='Access the KeepassXC Browser API from python',
      url='https://github.com/hrehfeld/python-keepassxc-browser',
      author='Hauke Rehfeld',
      author_email='pypi.org@haukerehfeld.de',
      packages=find_packages(),
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
          "Operating System :: OS Independent",
          "Topic :: Security",
          "Topic :: Software Development :: Libraries"
      ]
)

