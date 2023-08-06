from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='sphcpy',
      version='0.0.5',
      description='Wrappers and tools for reading and plotting p.XX data from SPHC',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Visualization',
      ],
      keywords='plot SPH VTK',
      scripts=['bin/p2VTK'],
      url='https://github.com/viper2642/sphcpy',
      author='David Pfefferle',
      author_email='david.pfefferle@uwa.edu.au',
      license='GPL-3.0',
      packages=['sphcpy'],
      install_requires=[
          'numpy',
          'pyevtk'
      ],
      include_package_data=True,
      zip_safe=False)

