from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='curieutil',
    version='0.0.1',
    description='say hello',
    py_modules=["curieutil"],
    package_dir={'': 'src'},
    url="https://github.com/geneontology/curie-util-py",
    author="Laurent-Philippe Albou",
    author_email="laurent.albou@lbl.gov",

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],

    long_description=long_description,
    long_description_content_type="text/markdown"
)


