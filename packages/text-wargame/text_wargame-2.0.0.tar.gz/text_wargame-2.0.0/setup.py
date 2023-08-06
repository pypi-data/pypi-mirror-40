from distutils.core import setup
import setuptools
with open('README') as file:
    readme = file.read()

# NOTE: change the 'name' field below with some unique package name.
# then update the url field accordingly.

setup(
    name='text_wargame',
    version='2.0.0',
    packages=['wargame'],
    url='https://testpypi.python.org/pypi/text_wargame/',
    license='LICENSE.txt',
    description='It is a test pkg ignore. I just want to test whether I am able to prepare it',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Mohd Shadab Khan',
    author_email='khanshadab96@yahoo.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
