import setuptools
import setuptools as s

with open("README.md", "r") as fh:
    long_description = fh.read()

long_description = long_description.replace('evry', 'every')
setuptools.setup(
    name="os_sys",
    version="0.1.7",
    author="Matthijs labots",
    
    author_email="libs.python@gmail.com",
    description="a big plus lib for more functions to use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://python-libs-com.webnode.nl/",
    python_requires='>=3',
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Source': 'https://github.com/Matthijs990/os_sys',
        'Downloads': 'https://python-libs-com.webnode.nl/downloads/',
        'become a member': 'https://python-libs-com.webnode.nl/user-registration/',
        'download all files': 'https://github.com/Matthijs990/os_sys.git',
        'want to help': 'https://github.com/Matthijs990/os_sys/tree/master/do%20you%20want%20to%20help'
    },
)
