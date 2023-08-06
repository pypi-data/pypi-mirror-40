from setuptools import setup

setup(name='dreamnet',
      version='0.1',
      description='An adventure game of sorts powered by ConceptNet',
      url='http://github.com/EHilly/dreamnet',
      author='Emmet Hilly',
      author_email='emmet.hilly@gmail.com',
      license='MIT',
      packages=['dreamnet'],
      install_requires=[
      	'pattern',
      ],
      zip_safe=False)