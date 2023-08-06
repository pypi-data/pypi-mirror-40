# -*- coding: utf-8 -*-

import itertools as _itertools

import svgwrite as _svgwrite

from . import core as _core
from . import export as _export


COLORSET = (
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b",
    "#e377c2", "#7f7f7f",
)


# primitives configuration
STRAND_WIDTH = 40
BOUNDARY_WIDTH = 2
STRAND_GAP = 100  # distance between the left boundary of two neighbor strands
STRETCHING_HEIGHT = 60  # should be > (STRAND_WIDTH - STRAND_GAP) / 2
TORSION_HEIGHT = 40
CROSSING_HEIGHT = 120
LAYERING_HEIGHT = 120
FLOW_GAP = 50


# derived/internal lengths
_MASK_WIDTH = 3 * BOUNDARY_WIDTH
_AA_OVERLAP = 1  # height of layers' overlap to avoid antialiasing artifact
_AA_TORSION_H = TORSION_HEIGHT - _AA_OVERLAP
_AA_CROSSING_H = CROSSING_HEIGHT - _AA_OVERLAP


# boundary curves
_TORSION_LCURVE = \
        f'v {_AA_OVERLAP}' \
        f'c 0 {_AA_TORSION_H / 2} {STRAND_WIDTH} {_AA_TORSION_H / 2} {STRAND_WIDTH} {_AA_TORSION_H}' \
        f'v {_AA_OVERLAP}'
_TORSION_RCURVE = \
        f'v {-_AA_OVERLAP}' \
        f'c 0 {-_AA_TORSION_H / 2} {STRAND_WIDTH} {-_AA_TORSION_H / 2} {STRAND_WIDTH} {-_AA_TORSION_H}' \
        f'v {-_AA_OVERLAP}'
_LSHIFT_CURVE = \
        f'v {_AA_OVERLAP}' \
        f'c 0 {_AA_CROSSING_H / 2} {-STRAND_GAP} {_AA_CROSSING_H / 2} {-STRAND_GAP} {_AA_CROSSING_H}' \
        f'v {_AA_OVERLAP}'
_LSHIFT_REVCURVE = \
        f'v {-_AA_OVERLAP}' \
        f'c 0 {-_AA_CROSSING_H / 2} {STRAND_GAP} {-_AA_CROSSING_H / 2} {STRAND_GAP} {-_AA_CROSSING_H}' \
        f'v {-_AA_OVERLAP}'
_RSHIFT_CURVE = \
        f'v {_AA_OVERLAP}' \
        f'c 0 {_AA_CROSSING_H / 2} {STRAND_GAP} {_AA_CROSSING_H / 2} {STRAND_GAP} {_AA_CROSSING_H}' \
        f'v {_AA_OVERLAP}'
_RSHIFT_REVCURVE = \
        f'v {-_AA_OVERLAP}' \
        f'c 0 {-_AA_CROSSING_H / 2} {-STRAND_GAP} {-_AA_CROSSING_H / 2} {-STRAND_GAP} {-_AA_CROSSING_H}' \
        f'v {-_AA_OVERLAP}'
_LAYERING_CURVE_TEMPLATE = \
        f'c 0 {LAYERING_HEIGHT / 2} {{shift}} {LAYERING_HEIGHT / 2} {{shift}} {LAYERING_HEIGHT}'
_LAYERING_REVCURVE_TEMPLATE = \
        f'c 0 {-LAYERING_HEIGHT / 2} {{shift}} {-LAYERING_HEIGHT / 2} {{shift}} {-LAYERING_HEIGHT}'
_ARC_TEMPLATE = \
        'a 1 1 0 1 0 {width} 0'


class _SVGDrawer:
    def __init__(self):
        self.dwg = _svgwrite.Drawing()
        self.depth = 0
        self._sprites = self._create_sprites()

    def _create_straight_sprite(self, height):
        sprite = self.dwg.g(class_='strand')
        sprite.add(
            self.dwg.rect(
                insert=(0, -_AA_OVERLAP),
                size=(STRAND_WIDTH, height + _AA_OVERLAP),
                class_='interior'
            )
        )
        sprite.add(
            self.dwg.line(
                start=(0, -_AA_OVERLAP),
                end=(0, height),
                class_='boundary'
            )
        )
        sprite.add(
            self.dwg.line(
                start=(STRAND_WIDTH, -_AA_OVERLAP),
                end=(STRAND_WIDTH, height),
                class_='boundary'
            )
        )
        self.dwg.defs.add(sprite)
        return sprite

    def _create_pos_torsion_sprite(self):
        mask = self.dwg.mask()  # emulate the overlap of the boundaries with a mask
        sprite = self.dwg.g(class_='strand')
        mask.add(
            self.dwg.path(
                (f'M 0 {-_AA_OVERLAP}', _TORSION_LCURVE, ),
                stroke='black',
                stroke_width=_MASK_WIDTH,
            )
        )
        mask.add(
            self.dwg.path(
                (f'M 0 {TORSION_HEIGHT}', _TORSION_RCURVE, ),
                stroke='white',
                stroke_width=BOUNDARY_WIDTH,
            )
        )
        sprite.add(
            self.dwg.path(
                (f'M 0 {-_AA_OVERLAP}', _TORSION_LCURVE, f'h {-STRAND_WIDTH}', _TORSION_RCURVE, 'Z', ),
                class_='interior',
            )
        )
        sprite.add(
            self.dwg.path(
                (f'M 0 {-_AA_OVERLAP}', _TORSION_LCURVE, ),
                class_='boundary',
            )
        )
        sprite.add(
            self.dwg.path(
                (f'M 0 {TORSION_HEIGHT}', _TORSION_RCURVE, ),
                mask=mask.get_funciri(),
                class_='boundary',
            )
        )
        self.dwg.defs.add(mask)
        self.dwg.defs.add(sprite)
        return sprite

    def _create_neg_torsion_sprite(self):
        mask = self.dwg.mask()  # emulate the overlap of the boundaries with a mask
        sprite = self.dwg.g(class_='strand')
        mask.add(
            self.dwg.path(
                (f'M 0 {TORSION_HEIGHT}', _TORSION_RCURVE, ),
                stroke='black',
                stroke_width=_MASK_WIDTH,
            )
        )
        mask.add(
            self.dwg.path(
                (f'M 0 {-_AA_OVERLAP}', _TORSION_LCURVE, ),
                stroke='white',
                stroke_width=BOUNDARY_WIDTH,
            )
        )
        sprite.add(
            self.dwg.path(
                (f'M 0 {-_AA_OVERLAP}', _TORSION_LCURVE, f'h {-STRAND_WIDTH}', _TORSION_RCURVE, 'Z', ),
                class_='interior',
            )
        )
        sprite.add(
            self.dwg.path(
                (f'M 0 {-_AA_OVERLAP}', _TORSION_LCURVE, ),
                mask=mask.get_funciri(),
                class_='boundary',
            )
        )
        sprite.add(
            self.dwg.path(
                (f'M 0 {TORSION_HEIGHT}', _TORSION_RCURVE, ),
                class_='boundary',
            )
        )
        self.dwg.defs.add(mask)
        self.dwg.defs.add(sprite)
        return sprite

    def _create_left_shift_sprite(self):
        sprite = self.dwg.g(class_='strand')
        sprite.add(
            self.dwg.path(
                (f'M 0 {-_AA_OVERLAP}', _LSHIFT_CURVE, f'h {STRAND_WIDTH}', _LSHIFT_REVCURVE, 'Z', ),
                class_='interior',
            )
        )
        sprite.add(
            self.dwg.path(
                (f'M 0 {-_AA_OVERLAP}', _LSHIFT_CURVE, ),
                class_='boundary'
            )
        )
        sprite.add(
            self.dwg.path(
                (f'M {STRAND_WIDTH} {-_AA_OVERLAP}', _LSHIFT_CURVE, ),
                class_='boundary'
            )
        )
        self.dwg.defs.add(sprite)
        return sprite

    def _create_right_shift_sprite(self):
        sprite = self.dwg.g(class_='strand')
        sprite.add(
            self.dwg.path(
                (f'M 0 {-_AA_OVERLAP}', _RSHIFT_CURVE, f'h {STRAND_WIDTH}', _RSHIFT_REVCURVE, 'Z', ),
                class_='interior',
            )
        )
        sprite.add(
            self.dwg.path(
                (f'M 0 {-_AA_OVERLAP}', _RSHIFT_CURVE, ),
                class_='boundary'
            )
        )
        sprite.add(
            self.dwg.path(
                (f'M {STRAND_WIDTH} {-_AA_OVERLAP}', _RSHIFT_CURVE, ),
                class_='boundary'
            )
        )
        self.dwg.defs.add(sprite)
        return sprite

    def _create_sprites(self):
        sprites = {
            'no-torsion': self._create_straight_sprite(height=TORSION_HEIGHT),
            'no-shift': self._create_straight_sprite(height=CROSSING_HEIGHT),
            'pos-torsion': self._create_pos_torsion_sprite(),
            'neg-torsion': self._create_neg_torsion_sprite(),
            'left-shift': self._create_left_shift_sprite(),
            'right-shift': self._create_right_shift_sprite(),
        }
        return sprites

    def _use_sprite(self, sprite, strand, position):
        shape = self.dwg.use(
            self._sprites[sprite],
            insert=(position * STRAND_GAP, self.depth),
            class_=f'strand-{strand}',
        )
        return shape

    def set_style(self, palette):
        """
        Set the style of the drawn SVG elements.

        :param palette:
            Assign each strand a color from the iterable palette.  The colors
            are bound to the strands in a round robin fashion.  If palette is
            empty, no colors are bound.
        """
        self.dwg['fill'] = 'white'  # white strands by default
        common_styling = [
            f'.boundary {{fill: none; stroke: black; stroke-width: {BOUNDARY_WIDTH};}}',
        ]
        per_strand_styling = [
            f'.strand-{i} {{fill: {color};}}'
            for i, color in enumerate(palette)
        ]
        style = ' '.join(common_styling + per_strand_styling)
        self.dwg.defs.add(self.dwg.style(style))

    def draw_stretching(self, size):
        """Draw the initial stretching of a template with size strands."""
        shape = self.dwg.g(class_='boundary')
        # draw left border
        shape.add(
            self.dwg.line(
                start=(0, 0),
                end=(0, STRETCHING_HEIGHT),
            )
        )
        # draw right border
        shape.add(
            self.dwg.line(
                start=(STRAND_GAP * (size - 1) + STRAND_WIDTH, 0),
                end=(STRAND_GAP * (size - 1) + STRAND_WIDTH, STRETCHING_HEIGHT),
            )
        )
        # draw stretching of each strand
        for position in range(size - 1):
            shape.add(
                self.dwg.path(
                    (
                        f'M {STRAND_GAP * (position + 1)} {STRETCHING_HEIGHT}',
                        f'v {-_AA_OVERLAP}',
                        _ARC_TEMPLATE.format(width=STRAND_WIDTH - STRAND_GAP),
                        f'v {_AA_OVERLAP}',
                    ),
                )
            )
        self.dwg.add(shape)

    def draw_torsion(self, strand, position, torque):
        """Draw a single torsion for a given strand."""
        if torque == 0:
            sprite = 'no-torsion'
        elif torque > 0:
            sprite = 'pos-torsion'
        else:  # torque < 0
            sprite = 'neg-torsion'

        shape = self._use_sprite(sprite, strand, position)
        self.dwg.add(shape)

    def draw_no_crossing(self, strand, position):
        """Draw a straight transition the height of a crossing."""
        shape = self._use_sprite('no-shift', strand, position)
        self.dwg.add(shape)

    def draw_crossing(self, left, right, orientation):
        """Draw the crossing of two strands."""
        lstrand, lpos = left
        rstrand, rpos = right
        if lpos > rpos:
            # ensure lstrand, lpos point to the leftmost strand
            lstrand, rstrand = rstrand, lstrand
            lpos, rpos = rpos, lpos

        shape = self.dwg.g()
        lshift = self._use_sprite('left-shift', rstrand, rpos)
        rshift = self._use_sprite('right-shift', lstrand, lpos)
        if orientation:
            # a positive crossing shows the right strand (left shift) above
            shape.add(rshift)
            shape.add(lshift)
        else:
            # a negative crossing shows the left strand (right shift) above
            shape.add(lshift)
            shape.add(rshift)
        self.dwg.add(shape)

    def draw_layer(self, strand, position, size):
        """Draw the layering step for a given strand."""
        lshift = position * STRAND_GAP
        rshift = (size - 1 - position) * STRAND_GAP
        shape = self.dwg.g(class_=f'strand strand-{strand}')
        shape.add(
            self.dwg.path(
                (
                    f'M {lshift} {self.depth - _AA_OVERLAP}',
                    f'v {_AA_OVERLAP}',
                    _LAYERING_CURVE_TEMPLATE.format(shift=-lshift),
                    f'h {(size - 1) * STRAND_GAP + STRAND_WIDTH}',
                    _LAYERING_REVCURVE_TEMPLATE.format(shift=-rshift),
                    f'v {-_AA_OVERLAP}',
                    'Z',
                ),
                class_='interior',
            )
        )
        shape.add(
            self.dwg.path(
                (
                    f'M {lshift} {self.depth - _AA_OVERLAP}',
                    f'v {_AA_OVERLAP}',
                    _LAYERING_CURVE_TEMPLATE.format(shift=-lshift),
                ),
                class_='boundary',
            )
        )
        shape.add(
            self.dwg.path(
                (
                    f'M {lshift + STRAND_WIDTH} {self.depth - _AA_OVERLAP}',
                    f'v {_AA_OVERLAP}',
                    _LAYERING_CURVE_TEMPLATE.format(shift=rshift),
                ),
                class_='boundary',
            )
        )
        self.dwg.add(shape)

    def draw_flow(self, size, style='minimal'):
        """Draw the template flow."""
        if style == 'minimal':
            shape = self.dwg.g(class_='boundary', stroke_linecap='square')
            shape.add(
                self.dwg.line(
                    start=(0, 0),
                    end=(STRAND_GAP * (size - 1) + STRAND_WIDTH, 0),
                )
            )
            shape.add(
                self.dwg.line(
                    start=(0, self.depth),
                    end=(STRAND_GAP * (size - 1) + STRAND_WIDTH, self.depth),
                )
            )
        elif style == 'complete':
            shape = self.dwg.g(class_='boundary')
            shape.add(
                self.dwg.path(
                    (
                        'M 0 0',
                        _ARC_TEMPLATE.format(width=-FLOW_GAP),
                        f'v {self.depth}',
                        _ARC_TEMPLATE.format(width=FLOW_GAP),
                    ),
                )
            )
            width = STRAND_GAP * (size - 1) + STRAND_WIDTH
            shape.add(
                self.dwg.path(
                    (
                        f'M {width} 0',
                        _ARC_TEMPLATE.format(width=-FLOW_GAP - 2 * width),
                        f'v {self.depth}',
                        _ARC_TEMPLATE.format(width=FLOW_GAP + 2 * width),
                    ),
                )
            )
        else:
            raise ValueError(f'Unknown style \'{style}\'')
        self.dwg.add(shape)


class SVGExporter(_export.Exporter, alias='svg'):
    def __init__(self, colorset=COLORSET):
        self.positions = None
        self.drawer = None
        self.colorset = colorset

    def _palette(self, size, color=True):
        # pylint: disable=no-else-return
        if color:
            # cycle through COLORS as long as needed
            return _itertools.islice(_itertools.cycle(self.colorset), size)
        else:
            return ()

    def _export_stretching(self, size):
        self.drawer.draw_stretching(size)
        self.drawer.depth += STRETCHING_HEIGHT

    @staticmethod
    def _decrease_torsion_torque(torque):
        # pylint: disable=no-else-return
        if torque == 0:
            return 0
        elif torque < 0:
            return torque + 1
        else:
            return torque - 1

    def _export_torsions(self, template):
        torsions = list(template.torsions)  # work on a copy
        while any(torsions):  # at least one strand remains twisted
            for strand, torque in enumerate(torsions):
                self.drawer.draw_torsion(strand, strand, torque)
                torsions[strand] = self._decrease_torsion_torque(torque)
            self.drawer.depth += TORSION_HEIGHT

    def _export_crossings(self, template):
        for crosslevel in template.crosslevels:
            uncrossed = set(range(template.size))  # track uncrossed strands
            for crossing in crosslevel:
                lstrand, rstrand = crossing
                lpos, rpos = self.positions[lstrand], self.positions[rstrand]
                self.drawer.draw_crossing(
                    left=(lstrand, lpos),
                    right=(rstrand, rpos),
                    orientation=template.crossings[lstrand, rstrand] > 0
                )
                uncrossed -= {lstrand, rstrand}
                self.positions[lstrand], self.positions[rstrand] = \
                    self.positions[rstrand], self.positions[lstrand]
            for strand in uncrossed:  # draw remaining uncrossing strands
                self.drawer.draw_no_crossing(strand, self.positions[strand])
            self.drawer.depth += CROSSING_HEIGHT

    def _export_layering(self, size):
        # paint layers from left to right (according to order, not position)
        final_order = _core.convert_order_position(self.positions)
        for position, strand in enumerate(final_order):
            self.drawer.draw_layer(strand, position, size)
        self.drawer.depth += LAYERING_HEIGHT

    def _export_flow(self, size, complete_flow=False):
        style = 'complete' if complete_flow else 'minimal'
        self.drawer.draw_flow(size, style=style)

    def _export_initialize(self, template, color=True):
        size = template.size
        self.drawer = _SVGDrawer()
        self.positions = list(range(size))
        self.drawer.set_style(self._palette(size, color=color))
        self._export_stretching(size)

    def _export_finalize(self, template, complete_flow=False):
        size = template.size
        self._export_layering(size)
        self._export_flow(size, complete_flow=complete_flow)

    def write(self, template, *, output, color=True, complete_flow=False, scale=1.0):
        self._export_initialize(template, color=color)
        self._export_torsions(template)
        self._export_crossings(template)
        self._export_finalize(template, complete_flow=complete_flow)
        self.drawer.dwg.write(output)
