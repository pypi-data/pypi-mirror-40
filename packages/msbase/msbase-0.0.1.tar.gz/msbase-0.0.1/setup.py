import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="msbase",
    version="0.0.1",
    author="Zhen Zhang",
    author_email="hi@monad.systems",
    description="Monad-Systems Base Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monad-systems/base.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
