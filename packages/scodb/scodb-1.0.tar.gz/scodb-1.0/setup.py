from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='scodb',
      version='1.0',
      description='Conector escrito em python para API do SCODB.',
      long_description=readme(),
      keywords='Demolay, SCODB',
      url='https://github.com/Otoru/scodb',
      author='Vitor Hugo de O. Vargas',
      author_email='vitor.hov@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requests',
          'xmltodict'
      ],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Plugins',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Portuguese (Brazilian)',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.7',
          'Topic :: Utilities'
      ],
      zip_safe=False)