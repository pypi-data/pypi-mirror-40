import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="termux_texter",
    version="0.0.6",
    author="Robert Wendt",
    author_email="",
    description="Easily send text messages using Flask and termux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'flask',
        'pause'
    ],
    entry_points={'console_scripts': [
        'termux-texter=termuxtexter.main:main']
    }
)
