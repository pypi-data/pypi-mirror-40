import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="telefly",
    version="0.1.0",
    author="Zeitpunk",
    author_email="ztpnk@mailbox.org",
    description="Create telegram bots in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://chaos.expert/ztpnk/telefly",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
