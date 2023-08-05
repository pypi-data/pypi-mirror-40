import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plotserver_api",
    version="0.0.4",
    author="Aleksandr Artemenkov",
    author_email="alartum@gmail.com",
    description="Python API for PlotServer.",
    license = 'MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alartum/plotserver-api",
    packages=setuptools.find_packages(),
    install_requires=[
          'requests',
          'cryptography',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)