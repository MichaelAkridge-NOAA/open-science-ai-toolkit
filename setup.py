from setuptools import setup, find_packages

setup(
    name="open-science-ai-toolkit",
    version="0.9.1",
    author="Michael Akridge",
    author_email="michael.akridge@noaa.gov",
    description="A comprehensive toolkit for AI-driven analysis and dataset management at NOAA. It includes functions for dataset preparation, image filtering, annotation validation, and model training.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MichaelAkridge-NOAA/open-science-ai-toolkit",
    packages=find_packages(),
    install_requires=['ultralytics'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    python_requires=">=3.7",
    keywords="AI, NOAA, datasets, image processing, YOLO, machine learning, data preparation, annotation",
    project_urls={
        "Bug Reports": "https://github.com/MichaelAkridge-NOAA/open-science-ai-toolkit/issues",
        "Source": "https://github.com/MichaelAkridge-NOAA/open-science-ai-toolkit",
    },
)
