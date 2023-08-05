import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='dextract',
                 version='0.1.dev1',
                 description='Layered extractor of data',
                 url='http://github.com/csehdz/dextract',
                 author='cseHdz',
                 author_email='carlos.hdz@me.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 install_requires=['os','copy','xlrd','pandas','numpy',
                 'pyexcel','pyexcel_xls','pyexcel_xlsx','statistics',
                 'collections','multiprocessing','gc','csv'],
                 zip_safe=False,
                 classifiers=["Programming Language :: Python :: 3",
                 "Operating System :: OS Independent"])
