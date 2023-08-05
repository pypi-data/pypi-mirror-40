from setuptools import setup, find_packages

setup(name='mp_utils',
      version='1.0',
      license='MIT',
      author='Kevin Glasson',
      author_email='kevinglasson+mp_utils@gmail.com',
      description='machine perception utility functions',
      packages=find_packages(),
      long_description=open('README.md').read(),
      zip_safe=False,
      install_requires=[
          'numpy',
          'opencv-python',
          'matplotlib'
      ],
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ])
