import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyDHC",
    version="1.3.2",
    author="Sidney Kuyateh",
    author_email="sidneyjohn23@icloud.com",
    description="Communication to Devolo Home Control hub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/autinerd/python-devoloDHC",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
)