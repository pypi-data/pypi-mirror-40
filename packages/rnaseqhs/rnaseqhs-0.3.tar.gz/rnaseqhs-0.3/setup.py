from setuptools import setup, find_packages
PACKAGE = "rnaseqhs"
NAME = "rnaseqhs"
DESCRIPTION = "Tool for analysis of RNA-seq data."
AUTHOR = 'Zhi Zhang'
AUTHOR_EMAIL = 'zzjerryzhang@gmail.com'
USERNAME = 'eglaab'
PASSWORD = 'webfish3'
URL = 'https://upload.pypi.org/legacy/', # use the URL to the github repo
download_url = 'https://git-r3lab.uni.lu/zhi.zhang/rnaseqhs/raw/master/rnaseqhs/dist/rnaseqhs-0.2.tar.gz' 
VERSION = __import__(PACKAGE).__version__


def readme():
    with open('README.rst') as f:
        return f.read()
    
setup(name=NAME,
#      packages=['rnaseq'],
      version=VERSION,
      description=DESCRIPTION,
      long_description=readme(),
      classifiers=[
              'Development Status :: 3 - Alpha',
	           'License :: OSI Approved :: MIT License',
	           'Programming Language :: Python :: 3.6',
                'Topic :: Scientific/Engineering :: Bio-Informatics',
	           ],
      keywords='rnaseq main',
      url=URL,
      download_url =download_url ,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      test_suite='nose.collector',
      tests_require=['nose==1.3.7'],
      #scripts=['bin/rnaseq'],
      entry_points = {
             'console_scripts': ['rnaseqhs=rnaseqhs.command_line:main'],
               },
      license='MIT',
      packages=find_packages(exclude=['tests']),
      #install_requires=['markdown', ],
      #dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0']
      include_package_data=True,
      zip_safe=False)

