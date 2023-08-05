import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discord_config",
    version="0.0.1",
    author="Casimir Nowak",
    author_email="nowakcasimir@outlook.com",
    description="Easy config module for Discord bots",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/nowakcasimir/discord-config",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       'appdirs'
    ]
)
