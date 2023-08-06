import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gscapl",
    version="0.0.0.5",
    author="Luke Waninger",
    author_email="luke.waninger@gmail.com",
    description="A package for geospatial context analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lukeWaninger/GSCAP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'googlemaps==3.0.2',
        'numpy==1.15.2',
        'pandas==0.23.4',
        'requests==2.19.1',
        'scikit-learn==0.19.2',
        'scipy==1.1.0',
        'SQLAlchemy==1.2.12',
        'urllib3==1.23',
        'synapseclient>=1.9.0'
    ],
    python_requires='>=3.6'
)
