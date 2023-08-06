# -*- coding: utf-8 -*-

"""
Template export primitives.
"""

class Exporter:
    _available_exporters = {}

    def __init_subclass__(cls, *, alias=None, **kwargs):
        assert alias not in cls._available_exporters, f'Shadowing existing alias: \'{alias}\''
        super.__init_subclass__(**kwargs)
        if alias is not None:
            cls._available_exporters[alias] = cls

    @classmethod
    def factory(cls, alias):
        try:
            return cls._available_exporters[alias]
        except KeyError:
            raise KeyError(f'Unknown Backend alias: \'{alias}\'') from None

    def write(self, template, *, output, color=True, complete_flow=False, scale=1.0):
        raise NotImplementedError


from ._svg import SVGExporter  # import required for the factory to work
