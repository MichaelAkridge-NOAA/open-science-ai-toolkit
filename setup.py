from setuptools import setup, find_packages

setup(
    name="open-science-ai-toolkit",
    version="0.5.1",
    author="Michael Akridge",
    author_email="michael.akridge@noaa.gov",
    description="A toolkit for AI-driven analysis, including a GUI and a Python library.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MichaelAkridge-NOAA/open-science-ai-toolkit",
    packages=find_packages(),
    install_requires=[
        'PyQt5', 
        'ultralytics',
        'pyqtdarktheme'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'noaa-ai-gui=noaa_ai_gui.main:main',  # Launch the GUI
        ],
    },
    keywords="AI, NOAA, datasets, GUI, toolkit, machine learning",
    project_urls={
        "Bug Reports": "https://github.com/MichaelAkridge-NOAA/open-science-ai-toolkit/issues",
        "Source": "https://github.com/MichaelAkridge-NOAA/open-science-ai-toolkit",
    },
)
