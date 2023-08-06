from setuptools import setup

setup(name='savemodel',
      version='0.3',
      description='To save models to HDFS',
      url='http://github.com',
      author='Yogesh Somawar',
      author_email='yogesh.somawar@qio.io',
      license='MIT',
      packages=['savemodel'],
      install_requires=[
	'clipper_admin',
	'pyspark',
	'tensorflow',
	'keras',
	'h2o',
        'cloudpickle==0.5.3'
      ],
      zip_safe=False)
