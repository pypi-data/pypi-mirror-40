import setuptools
import sys
sys.path.append('/home/dyz/.local/lib/python3.5/site-packages/')
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="novamind",
    version="0.0.2",
    author="Nova Mind",
    author_email="duanyzhi@outlook.com",
    description="Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duanyzhi/novamind",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
