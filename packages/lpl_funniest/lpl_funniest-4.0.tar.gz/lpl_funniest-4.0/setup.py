from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='lpl_funniest',
      version='4.0',
      description='The funniest joke in the world',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='http://github.com/xxxxx',
      author='Peilun',
      author_email='xxxxx@example.com',
      license='MIT',
      #packages=['lpl_funniest'],
      packages=find_packages(),
      install_requires=[
          'markdown',
      ],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      entry_points = {
        'console_scripts': ['funniest-joke=lpl_funniest.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
