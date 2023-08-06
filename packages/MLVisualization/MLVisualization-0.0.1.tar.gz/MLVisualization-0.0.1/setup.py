import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'scikit-learn',
    'bokeh',
    'pandas',
]

setuptools.setup(
    name="MLVisualization",
    version="0.0.1",
    author="Armin Mesic",
    author_email="armin.mesic@aisec.fraunhofer.de",
    description="Basic Visualizations for Machine Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    url="https://git-int.aisec.fraunhofer.de/kao/visulization",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)