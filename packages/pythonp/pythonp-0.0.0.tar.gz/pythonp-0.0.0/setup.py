import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pythonp",
    version="0.0.0",
    author="Beomsoo Kim",
    author_email="bluewhale8202@gmail.com",
    description="It does what `python -c` does and a few more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bombs-kim/pythonp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pythonp = pythonp.__main__:main',
        ],
    },
)
