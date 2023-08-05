import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stmodels",
    #packages = ['stmodels'],
    version="0.0.0.1",
    author="Steven Zheng",
    author_email="tianwolf@msn.com",
    description="Run Outliers Detection, etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flownait/stmodels",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)