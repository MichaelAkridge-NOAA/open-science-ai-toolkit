from setuptools import setup, find_packages

setup(
    name="open-science-ai-toolkit",
    version="0.2.0",
    author="Michael Akridge",
    author_email="michael.akridge@example.com",
    description="A toolkit for AI dataset preparation, filtering, and annotation validation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MichaelAkridge-NOAA/open-science-ai-toolkit",
    packages=find_packages(),  
    install_requires=[],       
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
