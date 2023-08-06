from setuptools import setup, find_packages

setup(name='simpleais',
      version=0.60,
      description='a simple ais parser',
      url='https://github.com/wpietri/simpleais',
      author='William Pietri',
      author_email='william-simpleais-0_6@scissor.com',
      license='Apache 2.0',
      packages=find_packages(),
      install_requires=['bitstring', 'testfixtures', 'Click', 'numpy', 'beautifulsoup4'],
      entry_points={
          'console_scripts': [
              'aiscat = simpleais.tools:cat',
              'aisgrep = simpleais.tools:grep',
              'aist = simpleais.tools:as_text',
              'aisburst = simpleais.tools:burst',
              'aisinfo = simpleais.tools:info',
              'aisdump = simpleais.tools:dump',
          ],
      },
      )
