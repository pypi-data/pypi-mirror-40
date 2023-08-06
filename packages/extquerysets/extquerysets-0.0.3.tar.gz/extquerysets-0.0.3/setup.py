import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="extquerysets",
    version="0.0.3",
    author="Ramil Aglyautdinov",
    author_email="aglyautdinov@gmail.com",
    description="Extended QuerySets for Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rami_dk/extquerysets",
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=[
        'Django>=1.8.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)