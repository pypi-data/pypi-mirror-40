from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cloversearch',
    version='0.0.13',
    packages=setuptools.find_packages(),
    install_requires=[
        'jieba>=0.39',
        'django',
    ],
    url='https://github.com/Deali-Axy',
    # license='GPLv3',
    author='DealiAxy',
    author_email='dealiaxy@gmail.com',
    description='CloverSearch for Django',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],

)
