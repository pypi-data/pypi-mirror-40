from setuptools import setup, find_packages

setup(name='Rsql',
      version='0.5',
      description='Rsql',
      long_description='This package will allow you to create clean SQL queries in your python app like FLask... Instant speed and simple api. For now it works only with mysql',
      classifiers=[ 
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
      ],
      keywords='sql, clear SQL, flask SQL, sql like PDO',
      namespace_packages=['Rsql'],  
      author='Raf',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'PyMySQL==0.9.3',
      ],
      include_package_data=True,
      zip_safe=False)