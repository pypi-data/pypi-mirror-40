import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="connectivator",
    version="0.0.4",
    author="Jonathan",
    description="Simple wrapper functions for connecting to and loading data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathan-marsan/connectivator",
    packages=setuptools.find_packages(),
    install_requires=[
          'pandas',
          'SQLAlchemy',
          'psycopg2',
          'gspread',
          'gspread-dataframe',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
