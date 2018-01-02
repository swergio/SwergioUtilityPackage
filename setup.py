from setuptools import setup
from setuptools import find_packages
setup(name='SwergioUtility',
      version='0.1',
      description='Description for package',
      url='http://',
      author='Ishmagurca',
      #author_email='me@example.com',
      license='MIT',
      packages=find_packages(),
      package_data={
          'Settings': ['DEFAULT_settings.json'],
      },
      install_requires=[
          'socketIO-client',
      ],
      zip_safe=False)