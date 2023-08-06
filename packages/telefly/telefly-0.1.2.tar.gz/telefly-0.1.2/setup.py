import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    'requests',
    'json',
    'urllib'
]

setuptools.setup(
    name="telefly",
    version="0.1.2",
    author="Zeitpunk",
    author_email="ztpnk@mailbox.org",
    description="Create Telegram bots in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://chaos.expert/ztpnk/telefly",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
