# -*- coding: utf-8 -*-
"""Top-level package for SteganoGAN."""

__author__ = """MIT Data To AI Lab"""
__email__ = 'dailabmit@gmail.com'
__version__ = '0.1.0'

from steganogan import cli
from steganogan.models import SteganoGAN

__all__ = ('SteganoGAN', 'cli')
