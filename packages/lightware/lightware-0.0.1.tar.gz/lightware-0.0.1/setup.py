import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lightware",
    version="0.0.1",
    author="Andrew Dorokhin",
    author_email="andrew@dorokhin.moscow",
    description="Python library to provide a  communication link with LightWare Eth switches.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dorokhin/lightware-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 1 - Planning",
        "Topic :: Home Automation"
    ],
)
