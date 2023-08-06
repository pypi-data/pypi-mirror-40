from setuptools import setup

setup(name='algo_db_controller',
      version='0.1',
      description='Controls everything db related for algo',
      author='Afzal SH @ Tarams',
      author_email='afzal.hameed@tarams.com',
      license='MIT',
      packages=['db_controller'],
      install_requires=[
          'psycopg2',
      ],
      zip_safe=False)
