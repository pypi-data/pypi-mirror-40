from setuptools import setup, find_packages
 
setup(name='opticalmarkmedi',
      version='0.1',
      url='https://gitlab.com/trunghd828/optical_mark',
      license='None',
      author='Tiamo',
      author_email='trunghd828@gmail.com',
      description='Optical mark for Meditech',
      packages=find_packages(),
      long_description=open('README.md').read(),
      zip_safe=False)