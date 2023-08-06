from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.1.14'
description = '{}: 总算测试可以用了！'.format(version)

setup(
    name='cloversearch',
    version=version,
    packages=setuptools.find_packages(),
    install_requires=[
        'jieba>=0.39',
        'django',
    ],
    url='https://github.com/Deali-Axy',
    # license='GPLv3',
    author='DealiAxy',
    author_email='dealiaxy@gmail.com',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],

)
