# -*- coding: utf-8 -*-

"""NeuroMMSig Knowledge."""

import os

from bel_repository import BELRepository

__all__ = ['repository', 'main']

HERE = os.path.dirname(__file__)
VERSION = '0.0.1'

repository = BELRepository(HERE)
main = repository.build_cli()
