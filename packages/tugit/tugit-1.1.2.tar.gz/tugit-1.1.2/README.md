# TugIt

**TugIt** is a Python library for installing packages directly from a git repository. 

# How to Install

To install TugIt just use: 

```bash
pip install tugit
```

# How to install a Python package hosted as a Git repo

To use TugIt to install Python packages directly from a git repository use the Installer class:

```python
from tugit import Installer
installer = Installer()
installer.tug(package='tugit', url='https://github.com/idin/tugit.git') 
# optional arguments: 
#   ignore_if_installed (default: True)
#   echo (default: 1)
```

# How to get a list of installed packages

```python
print(installer.installed_packages)
```
