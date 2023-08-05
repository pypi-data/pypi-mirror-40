from distutils.core import setup, Extension

module1 = Extension('cnormalizer',
                    sources=['normalizer.cpp'])

setup(name='balad-cnormalizer', version='1.0', description='Normalizer in C++',
      ext_modules=[module1])
