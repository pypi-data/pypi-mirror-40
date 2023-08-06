from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='twikenizer',
      version='1.0',
      description='Tokenizer for Twitter comments (tweets)',
      url='https://github.com/Guilherme-Routar/Twikenizer',
      author='Guilherme Routar',
      author_email='groutar@gmail.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['twikenizer'],
      zip_safe=False,
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ])