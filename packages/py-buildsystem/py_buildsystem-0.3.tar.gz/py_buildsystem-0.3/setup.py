from setuptools import setup, find_packages

setup(name='py_buildsystem',
      version='0.3',
      description='pythin based build system.',
      url='https://github.com/ProrokWielki/py_buildsystem',
      author='Paweł Warzecha',
      author_email='pawel.warzecha@yahoo.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'pyyaml',
          'setuptools-git'
          ],
      zip_safe=False)