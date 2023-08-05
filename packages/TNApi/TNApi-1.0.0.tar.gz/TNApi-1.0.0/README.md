# TNApi
Textnow API, written in Python

## Installation
1. Install from pip:
```bash
pip3 install TNApi
```

2. Install from sources:
```bash
git clone https://github.com/katant/TNApi.git
cd TNApi
python3 setup.py install
```

## Usage
Example code to login:
```python
from TNApi import TNApi

api = TNApi("email@example.com", "12345679")
api.login()
```

