import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yall",
    version="0.0.2",
    author="Denis Mingulov",
    author_email="denis@mingulov.com",
    description="Yet Another Lazy Loader for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mingulov/yall",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
)
