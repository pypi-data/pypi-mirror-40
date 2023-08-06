__author__ = 'Abdulrahman Semrie<hsamireh@gmail.com>'

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mozi-cli",
    version="1.4.1",
    author="Abdulrahman Semrie",
    author_email="hsamireh@gmail.com",
    descirption="A cli tool that will prepare a json file which can be used to call the MOSES SNET Service",
    py_modules=["mozi_cli"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Habush/mozi-service-cli",
    packages=setuptools.find_packages(),
    entry_points="""
        [console_scripts]
        mozi-cli=mozi_service_cli.mozi_cli:cli
    """
)