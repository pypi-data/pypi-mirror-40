import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="randtext",
    version="0.1.3",
    author="Mantaseus",
    description = 'Generate random text with a considerable amount of control ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/Mantaseus/randtext',
    license = 'MIT',

    packages=setuptools.find_packages(),
    package_dir = {'randtext': 'randtext'},
    package_data = {'randtext': ['dictionary/*']},
    include_package_data = True,

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'pathlib'
    ]
)
