import setuptools
from pathlib import Path
setuptools.setup(
    name='laurentvoicerecognition',
    version=1.0,
    long_description=Path("README.md").read_text(),
    # this will exclude the 'tests' and 'data' folders
    packages=setuptools.find_packages(exclude=['tests', 'data'])

)
