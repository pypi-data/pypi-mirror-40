import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

long_description = long_description.replace('evry', 'every')
setuptools.setup(
    name="os_sys",
    version="0.0.8",
    author="Matthijs labots",
    
    author_email="libs.python@gmail.com",
    description="a big plus lib for more functions to use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://python-libs-com.webnode.nl/",
    python_requires='>=3',
    include_package_data=True,
    packages=setuptools.find_packages(),
    package_data={'data_files': ['data/*.data']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
