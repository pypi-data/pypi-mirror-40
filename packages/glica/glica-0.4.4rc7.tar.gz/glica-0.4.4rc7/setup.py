import setuptools

# Note that the version is populated via a CI/CD script and is invalid until populated.

setuptools.setup(
    name="glica",
    version="0.4.4-rc7",
    author="Tian Hao Wang",
    scripts=[
        "glica/extractors.py",
    ],
    author_email="dev@paced.me",
    description="GitLab Instant Changelog Assurance (GLICA) for ensuring up-to-date CHANGELOG.md files!",
    long_description="Please refer to the repository's README.md file for the longer description.",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/halfbakedstudio/tools/glica",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Version Control :: Git",
        "Operating System :: OS Independent",
    ],
)
