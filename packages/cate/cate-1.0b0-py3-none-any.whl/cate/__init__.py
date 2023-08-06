# -*- coding: utf-8 -*-

"""
CATE: Chaotic Attractor TEmplate


Chaotic attractors are solutions of deterministic processes, of which the
topology can be described by templates.  We consider templates of chaotic
attractors bounded by a genus-1 torus described by a linking matrix.

This package provides modules to:
    - validate a linking matrix by checking continuity and determinism
      constraints.
    - draw a template of a valid linking matrix.  The representation of the
      template is compact, as the height of the template is minimized.  The
      representation is saved as a Scalable Vector Graphics (SVG) file.

This package also provides a CLI.
"""

__version__ = '1.0b0'
