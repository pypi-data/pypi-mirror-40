import setuptools

with open('README.md', 'r') as fp:
    long_description = fp.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
     name='morphy',
     version='0.2',
     author='Igor Ezersky',
     author_email='igor.ezersky.work@gmail.com',
     description='Smart tool for morphological analysis',
     long_description=long_description,
     long_description_content_type='text/markdown',
     url='https://github.com/igorezersky/morphy',
     packages=setuptools.find_packages(),
     install_requires=required,
     classifiers=[
         'Programming Language :: Python :: 3',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
     ],
 )
