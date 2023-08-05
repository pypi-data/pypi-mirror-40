from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
  name='json_serializer',
  version='1.0.0',
  description='The library for serialize/deserialize into format JSON.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://gitlab.com/Chvarkov/json_serializer',
  author='Alexey Chvarkov',
  author_email='chvarkov.alexey@gmail.com',
  license='MIT',
  packages=['json_serializer'],
  zip_safe=False,
  setup_requires=['pytest-runner'],
  tests_require=['pytest', 'pytest-cov']
)
