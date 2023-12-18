#!/usr/bin/env bash
if [ \! -d venv ]; then
    python -m venv venv
    . venv/bin/activate
    pip install sslyze
    sslyze --early_data localhost
else
    . venv/bin/activate
    sslyze --early_data localhost
fi