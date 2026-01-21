# Installation

This guide covers how to install EthosCrawl on your system.

## Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **Git** (for development installation)

## Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
# Basic installation
pip install ethoscrawl

# With AI features
pip install ethoscrawl[ai]

# With Scrapling integration
pip install ethoscrawl[scrapling]

# With all optional features
pip install ethoscrawl[all]
```

### Method 2: Install from GitHub

```bash
# Install latest development version
pip install git+https://github.com/YOUR_USERNAME/ethoscrawl.git

# Or clone and install
git clone https://github.com/YOUR_USERNAME/ethoscrawl.git
cd ethoscrawl
pip install -e .
```

### Method 3: Development Installation

For contributing to EthosCrawl or modifying the source code:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ethoscrawl.git
cd ethoscrawl

# Install in development mode with all dependencies
pip install -e .[dev]

# Verify installation
python -c "import ethoscrawl; print(ethoscrawl.__version__)"
```

## Optional Dependencies

EthosCrawl has several optional dependencies for extended functionality:

### AI Features
```bash
pip install ethoscrawl[ai]
```
Includes:
- `openai` - For AI-powered content analysis
- `transformers` - For local AI models
- `torch` - PyTorch for machine learning

### Scrapling Integration
```bash
pip install ethoscrawl[scrapling]
```
Includes integration with Scrapling for advanced scraping capabilities.

### Development Tools
```bash
pip install ethoscrawl[dev]
```
Includes:
- `pytest` - Testing framework
- `flake8` - Code linting
- `mypy` - Type checking
- `black` - Code formatting
- `isort` - Import sorting

### All Features
```bash
pip install ethoscrawl[all]
```
Installs all optional dependencies.

## Platform-Specific Instructions

### macOS
```bash
# Using Homebrew
brew install python
pip install ethoscrawl

# Or using pyenv
pyenv install 3.10
pyenv global 3.10
pip install ethoscrawl
```

### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install EthosCrawl
pip install ethoscrawl
```

### Windows
```bash
# Using PowerShell
python -m pip install --upgrade pip
pip install ethoscrawl

# Or using Windows Terminal
# Create virtual environment
python -m venv venv
venv\Scripts\activate
pip install ethoscrawl
```

## Virtual Environments (Recommended)

Using virtual environments is recommended to avoid conflicts with system packages:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install EthosCrawl
pip install ethoscrawl
```

## Docker Installation

You can also use EthosCrawl with Docker:

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install EthosCrawl
RUN pip install ethoscrawl

# Copy your scripts
COPY . .

# Run your script
CMD ["python", "your_script.py"]
```

Or use the pre-built image (when available):

```bash
docker pull yourusername/ethoscrawl:latest
```

## Verification

After installation, verify that EthosCrawl is working correctly:

```bash
# Check version
ethoscrawl --version

# Test CLI
ethoscrawl --help

# Test Python import
python -c "from ethoscrawl import EthosCrawler; print('Import successful')"
```

## Troubleshooting Installation

### Common Issues

1. **Permission Errors**
   ```bash
   # Use --user flag
   pip install --user ethoscrawl
   
   # Or use virtual environment
   python -m venv venv
   source venv/bin/activate
   pip install ethoscrawl
   ```

2. **Missing Dependencies**
   ```bash
   # On Ubuntu/Debian
   sudo apt install python3-dev build-essential
   
   # On macOS
   xcode-select --install
   ```

3. **Outdated pip**
   ```bash
   pip install --upgrade pip
   ```

4. **Network Issues**
   ```bash
   # Use mirror
   pip install ethoscrawl -i https://pypi.tuna.tsinghua.edu.cn/simple
   
   # Or increase timeout
   pip install --default-timeout=100 ethoscrawl
   ```

### Getting Help

If you encounter issues during installation:

1. Check the [FAQ](../docs/faq.md)
2. Search [existing issues](https://github.com/YOUR_USERNAME/ethoscrawl/issues)
3. Create a [new issue](https://github.com/YOUR_USERNAME/ethoscrawl/issues/new) with:
   - Your operating system
   - Python version (`python --version`)
   - pip version (`pip --version`)
   - Full error message

## Next Steps

Once installed, check out the [Quick Start Guide](quickstart.md) to begin using EthosCrawl.