import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cvesearch",
    version="1.2",
    author="Sujit Ghosal",
    author_email="thesujit@gmail.com",
    description="Search references, exploit modules and pocs for any CVE ID",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords="cve cveid cvesearch cvelinks cvepoc cveurl vulnerability exploits references poc search",
    url="https://pypi.org/project/cvesearch/",
    entry_points={
          'console_scripts': [
              'cvesearch = cvesearch.cvesearch:main'
          ]
      },
    python_requires='>=3',
    install_requires=[
        'termcolor',
        'requests',
        'ujson'
    ],
    dependency_links=[
        'https://pypi.org/project/ujson/',
        'https://pypi.org/project/termcolor/',
        'https://pypi.org/project/requests/'
    ],
    zip_safe=False
)
