from setuptools import setup
version = "0.0.11"
setup(name='planblick.autorun',
      version=version,
      description='A simple class that can be placed in a services root folder and will be picked up and executed during deployment',
      url='https://www.planblick.com',
      author='Florian Kröber @ Planblick',
      author_email='fk@planblick.com',
      license='MIT',
      packages=['planblick.autorun'],
      install_requires=[
          'requests',
          'json',
      ],
      zip_safe=False)
