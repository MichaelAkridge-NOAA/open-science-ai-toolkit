#!/bin/bash
# Welcome
echo "===================================================================================="
echo " _   _   ___      _        _               _     ___          ____  _   _  ___ "
echo "| \ | | / _ \    / \      / \             / \   |_ _|        / ___|| | | ||_ _|"
echo "|  \| || | | |  / _ \    / _ \   _____   / _ \   | |  _____ | |  _ | | | | | | "
echo "| |\  || |_| | / ___ \  / ___ \ |_____| / ___ \  | | |_____|| |_| || |_| | | | "
echo "|_| \_| \___/ /_/   \_\/_/   \_\       /_/   \_\|___|        \____| \___/ |___|"
echo "===================================================================================="
echo "Welcome to the NOAA AI GUI Setup Script!"
echo "This script will set up your Conda environment and optionally install CUDA dependencies."
echo "===================================================================================="
echo ""

# Step 0: Check for required system dependencies
echo "STEP 0: Checking for required system dependencies..."
echo "===================================================================================="

OS=$(uname)
echo "Detected OS: $OS"
if [ "$OS" == "Linux" ]; then
    echo "Installing Linux dependencies..."
    sudo apt-get update
    sudo apt-get install -y libxcb-xinerama0 libxcb1 libx11-xcb1 libxcb-glx0 libxcb-keysyms1
elif [ "$OS" == "Darwin" ]; then
    echo "Installing macOS dependencies..."
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install Homebrew first: https://brew.sh/"
        exit 1
    fi
    brew update
    brew install xcb qt
elif [[ "$OS" == CYGWIN* || "$OS" == MINGW* || "$OS" == MSYS* ]]; then
    echo "Detected Windows."
else
    echo "Unknown platform."
    exit 1
fi

# Step 1: Create the Conda environment
echo ""
# Step 1: Create the Conda environment
echo "STEP 1: Creating Conda environment..."
echo "===================================================================================="
conda create --name noaa-ai-gui python=3.12 -y

# Step 2: Initialize Conda in the script
echo ""
echo "STEP 2: Initializing Conda..."
echo "===================================================================================="
# uncomment if needed: source ~/miniconda3/etc/profile.d/conda.sh
conda activate noaa-ai-gui

# Step 3: Install necessary packages
echo ""
echo "STEP 3: Installing necessary packages..."
echo "===================================================================================="
pip install git+https://github.com/MichaelAkridge-NOAA/open-science-ai-toolkit.git

# Optional Step: Install CUDA dependencies
echo ""
echo "===================================================================================="
read -p "STEP 4: Do you wish to install CUDA dependencies (y/n)? " answer
case ${answer:0:1} in
    y|Y )
    echo ""
    echo "Installing CUDA Toolkit and PyTorch with CUDA support..."
    conda install nvidia::cuda-toolkit -y 
    echo "===================================================================================="
    echo "CUDA dependencies installed successfully."
    ;;
    * )
    echo "Skipping CUDA installation."
    ;;
esac

# Final Message
echo ""
echo "===================================================================================="
echo "Setup Complete! The Conda environment 'noaa-ai-gui' is ready to use."
echo "To activate the environment, run: conda activate noaa-ai-gui"
echo "To launch the app, use: noaa-ai-gui"
echo "===================================================================================="
echo "If you need more CUDA for GPU support, ensure your NVIDIA drivers are installed and compatible."
echo "For more info, visit:"
echo "  - CUDA Toolkit: https://anaconda.org/nvidia/cuda-toolkit"
echo "  - PyTorch: https://pytorch.org/get-started/locally/"
echo "    example:"
echo "    conda install nvidia/label/cuda-12.4.0::cuda-nvcc -y"
echo "    conda install nvidia/label/cuda-12.4.0::cuda-toolkit -y"
 echo "   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124 --upgrade"
echo "===================================================================================="
