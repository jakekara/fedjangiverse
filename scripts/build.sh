#!/usr/bin/env sh

python -m build --sdist fedj_webfinger && \
python -m twine upload fedj_webfinger/dist/*
