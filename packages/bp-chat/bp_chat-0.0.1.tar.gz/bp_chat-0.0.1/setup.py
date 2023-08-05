import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bp_chat",
    version="0.0.1",
    author="CompasBP",
    author_email="compas.ru.mobile@gmail.com",
    description="BP Chat gui application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/compasrumobile/bp-chat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)