#!/usr/bin/env bash
pytest $@ -W ignore::DeprecationWarning
