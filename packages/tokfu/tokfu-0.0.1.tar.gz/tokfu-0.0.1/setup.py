from distutils.core import setup

setup(
  name = 'tokfu',
  packages = ['tokfu'],
  version = '0.0.1',
  description = 'Tokfu',
  long_description = '',
  author = '',
  license = '',
  package_data={'tokfu': ['data/perluniprops/*.txt', 'data/nonbreaking_prefixes/nonbreaking_prefix.*']},
  url = 'https://github.com/alvations/tofu',
  keywords = [],
  classifiers = [],
  install_requires = ['six']
)
