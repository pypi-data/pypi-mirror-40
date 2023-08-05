Development Setup
===

Environment
---
Usual magic:

    python3 -m venv venv
    pip install -U pip
    pip install -r requirements.txt


Publish
---
Package:

    python3 setup.py sdist bdist_wheel

Sign:

    gpg --detach-sign -a dist/*gz
    gpg --detach-sign -a dist/*whl
    
Upload:

    twine upload