import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cms_forms",
    version="0.0.1",
    author="Sim1234",
    author_email="szymon.zmilczak@gmail.com",
    description="Set of Django CMS plugins for creating forms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sim1234/cms_forms",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
