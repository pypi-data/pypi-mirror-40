from setuptools import setup, find_packages

with open("README.md") as f:
   long_description = f.read()

setup(
   name="inflame",
   version="0.4.0",
   license='MIT',
   description="Deep learning applied to text classification, in PyTorch",
   long_description=long_description,
   long_description_content_type="text/markdown",
   author="John Jung",
   author_email="tojohnjung@gmail.com",
   url="https://github.com/zjohn77/inflame",
   packages=find_packages(),
   classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: POSIX :: Linux",
   ],
   keywords='deep learning',
   install_requires=[
      'scipy>=1.1',
      'numpy>=1.15',
      'torch>=0.4',
      'spacy>=2.0',
      'scikit_learn>=0.20',
      'PyYAML>=3',
   ],
   dependency_links=['https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.0.0/en_core_web_sm-2.0.0.tar.gz']
)