# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 08:14:54 2018

@author: yoelr
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 15:26:49 2018

@author: yoelr
"""

from pint import UnitRegistry
from pint.util import to_units_container
import os

__all__ = ['ureg', 'Quantity', 'Q_']

# Set pint Unit Registry
ureg = UnitRegistry()
ureg.default_format = '~P'
dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
ureg.load_definitions(dir_path + 'my_units_defs.txt')
Quantity = Q_ = ureg.Quantity

# Remove latex formating
def _new_format(self):
    return self.__format__('')

Quantity._repr_latex_ = Q_._repr_html_ = Q_.__str__ = Q_.__repr__ = _new_format

# Add function to check dimensions
def check(self, dimensions):
    return self.dimensionality is ureg._get_dimensionality(to_units_container(dimensions))

Quantity.check = check
