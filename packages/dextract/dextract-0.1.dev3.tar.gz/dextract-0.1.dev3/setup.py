import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='dextract',
                 version='0.1.dev3',
                 description='Layered extractor of data',
                 url='http://github.com/csehdz/dextract',
                 author='cseHdz',
                 author_email='carlos.hdz@me.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 classifiers=["Programming Language :: Python :: 3",
                 "Operating System :: OS Independent"])
