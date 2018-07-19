from setuptools import setup, find_packages

setup(name='nlpru',
      version='0.1.2',
      description='simple Russian Natural language Processing library for python',
      long_description=open('README.md').read(),
      classifiers=[
        'Development Status :: WIP',
        'License :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Natural Language Processing :: English',
      ],
      url='https://www.rudatalab.com',
      author='@SergeGoussev',
      author_email='rudatalab_info@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['experiments.*','*.experiments*','*experiments*']),
      install_requires=[
              'pysqlc',
              'pymorphy2',
              'nltk',
              'emoji',
              'sklearn'],
      zip_safe=False)