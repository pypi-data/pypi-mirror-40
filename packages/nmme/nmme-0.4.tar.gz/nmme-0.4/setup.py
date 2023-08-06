from setuptools import setup

def readme():
    with open('README.rst') as f:
        return(f.read())


setup(name='nmme',
      version='0.4',
      description='NMME pip install script',
      long_description=readme(),
      url='https://nemoest.com',
      author='Nemo Est',
      author_email='nemo_est@outlook.com',
      license='MIT',
      packages=['nmme'],
      install_requires=[
      'requests',
      ],
      zip_safe=False)
