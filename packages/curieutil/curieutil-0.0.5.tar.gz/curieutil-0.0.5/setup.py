from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='curieutil',
    version='0.0.5',
    description='Python Library to translate CURIEs to IRIs and vice versa. Python version based on the Java Implementation: https://github.com/prefixcommons/curie-util and the JavaScript Implementation: https://github.com/geneontology/curie-util-es5',
    py_modules=["curieutil"],
    packages=['src'],
    url="https://github.com/geneontology/curie-util-py",
    author="Laurent-Philippe Albou",
    author_email="laurent.albou@lbl.gov",
    keywords=["CURIE", "URI", "IRI", "RDF", "OWL"],
    install_requires=[
        'bidict',
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],

    long_description=long_description,
    long_description_content_type="text/markdown"
)


