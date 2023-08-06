import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nms",
    version="0.1.6",
    author="Tom Hoag",
    author_email="tomhoag@gmail.com",
    description="A Non Maximal Suppression Python Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.com/tomhoag/nms",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'numpy',
    ],
    keywords=['non maximal suppression', 'non maximum suppression', 'opencv', 'image processing'],

)
