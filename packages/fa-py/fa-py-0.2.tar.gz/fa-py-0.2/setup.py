from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

def requirements():
    with open('requirements.txt') as r:
        reqs = r.read()
    reqs = reqs.split("\n")
    return reqs[:-1]

setup(name='fa-py',
      version='0.2',
      description='A Python package to for performing Factor analysis on any given data.',
      long_description=readme(),
      url='https://github.com/ck090/FactorApy',
      author='Chandra Kanth N',
      author_email='canfindck@gmail.com',
      license='MIT',
      packages=['fa_py'],
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
      ],
      install_requires=requirements(),
      zip_safe=False)