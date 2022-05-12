from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
    long_description_content_type = "text/x-rst"
except(IOError, ImportError):
    long_description = open('README.md').read()
    long_description_content_type = 'text/markdown'

setup(
    name='pyDAC',
    version='0.0.1',
    description='pyDAC (python Directly Addressable Codes) offers a variable-length encoding scheme for (unsigned) integers with random access to any element of the encoded sequence.',
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url='https://github.com/rmrschub/pyDAC',
    author='René Schubotz',
    author_email='rene.schubotz@dfki.de',
    license='CC BY-NC-SA 4.0',
    packages=['pyDAC'],
    install_requires=['typing',
                      'numpy',
                      'bitarray',
                      'more_itertools',
                      'succinct',
                      'tqdm',
                      'tensorflow',
                      'tensorflow_probability'],

    classifiers=[ ],
)