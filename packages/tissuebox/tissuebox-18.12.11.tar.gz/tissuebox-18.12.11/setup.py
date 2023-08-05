from distutils.core import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='tissuebox',
    version='18.12.11',
    description='Tissuebox :: Pythonic payload validator',
    author='nehem',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author_email='nehemiah.jacob@gmail.com',
    url='https://github.com/nehemiahjacob/tissuebox.git',
    packages=['tissuebox'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
