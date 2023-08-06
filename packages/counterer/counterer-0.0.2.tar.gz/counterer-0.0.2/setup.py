import setuptools

with open("README.md", "r") as fh:  # description to be used in pypi project page
    long_description = fh.read()

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

install_requires = []  # any requirements your package has

setuptools.setup(
    name="counterer",
    version="0.0.2",
    author="Abin Simon",
    author_email="abinsimon10@gmail.com",
    description="Simple counter",
    url="https://github.com/meain/counterer",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["counterer"],
    install_requires=install_requires,
    keywords=["counter", "python"],
    classifiers=classifiers,
    entry_points={"console_scripts": ["counter = counterer.counterer:main"]},
)
