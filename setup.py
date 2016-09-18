from setuptools import setup, find_packages

setup(name='kala',
      version='0.1',
      description="kala client",
      long_description="""\
Kala scheduler api client
""",
      classifiers=[],
      keywords='kala',
      author='gmajere@gmail.com',
      author_email='gmajere@gmail.com',
      url='',
      license='Apache2',
      scripts=[],
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['requests'],
      )
