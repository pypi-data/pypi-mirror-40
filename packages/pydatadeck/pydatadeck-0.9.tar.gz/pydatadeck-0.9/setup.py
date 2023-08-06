from setuptools import setup

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(name='pydatadeck',
      version='0.9',
      description='Python SDK for Datadeck',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.7'
      ],
      keywords='datadeck',
      url='https://www.datadeck.com',
      author='Datadeck Dev',
      author_email='datadeck_dev@ptmind.com',
      license='MIT',
      packages=['pydatadeck'],
      install_requires=[
          'flask',
          'pyyaml'
      ],
      include_package_data=True,
      zip_safe=False)
