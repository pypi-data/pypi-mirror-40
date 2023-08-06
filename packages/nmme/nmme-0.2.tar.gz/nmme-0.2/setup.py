from setuptools import setup

setup(name='nmme',
      version='0.2',
      description='NMME pip install script',
      url='https://nemoest.com',
      author='Nemo Est',
      author_email='nemo_est@outlook.com',
      license='MIT',
      packages=['nmme'],
      install_requires=[
      'requests',
      ],
      zip_safe=False)
