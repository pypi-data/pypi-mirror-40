import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

cur_classifiers = [
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

setuptools.setup(
    name="pystag",
    version="0.0.1",
    author='Abin Simon',
    author_email='abinsimon10@gmail.com',
    description="Tag local music using spotify api",
    url="https://github.com/meain/stag",
    long_description=long_description,
    packages=setuptools.find_packages(),
    keywords=['spotify', 'music', 'tagging'],
    classifiers=cur_classifiers)
