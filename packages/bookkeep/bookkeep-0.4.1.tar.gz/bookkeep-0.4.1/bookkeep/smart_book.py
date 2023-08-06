# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 08:27:01 2018

@author: yoelr
"""
from .utils import dim
from .unit_registry import Quantity
from .unit_manager import UnitManager
from numpy import asarray, ndarray
from pandas import DataFrame
from warnings import warn


class SmartBook(dict):
    """Create a dictionary that represents values with units of measure and alerts when setting an item out of bounds. It assumes bounds are inclusive unless items in *inclusive* state otherwise.
    
    **Parameters**
    
        **units:** [UnitManager or dict] Dictionary of units of measure.
        
        **bounds:** [dict] Dictionary of bounds.
        
        ***args:** Key-value pairs to initialize.

        **inclusive:** [dict] Dictionary of (lblim, ublim) boolean pairs where [-]:
            * lblim is True if lower bound limit is included, and False otherwise.
            * ublim is True if upper bound limit is included, and False otherwise.
        
        **source:** Should be one of the following [-]:
            * [str] Short description of the SmartBook object.
            * Object which the SmartBook object belongs to.
            * None
        
        ****kwargs:** Key-value pairs to initialize.
    
    **Class Attribute**
    
        **Quantity:** `pint Quantity <https://pint.readthedocs.io/en/latest/>`__ class for compatibility.
    
    **Examples**
    
    SmartBook objects provide an easy way to keep track of units of measure and enforce bounds.
    
        Create a SmartBook object with *units*, *bounds*, a *source* description, and *arguments* to initialize the dictionary:
         
            >>> sb = SmartBook(units={'T': 'K', 'Duty': 'kJ/hr'},
            ...                bounds={'T': (0, 1000)},
            ...                source='Operating conditions',
            ...                T=350)
            >>> sb
            {'T': 350 (K)}
        
        The *units* attribute becomes a :doc:`UnitManager` object with a reference to all dictionaries (*clients*) it controls. These include the SmartBook and its bounds.
    
            >>> sb.units
            UnitManager: {'T': 'degC', 'Duty': 'kJ/hr'}
            >>> sb.units.clients
            [{'T': 350 (K)}, {'T': (0, 1000)}]
        
        Change units:
         
            >>> sb.units['T'] = 'degC'
            >>> sb
            {'T': 76.85 (degC)}
            >>> sb.bounds
            {'T': array([ -273.15, 726.85])}
        
        Add items:
            
            >>> sb['P'] = 101325
            >>> sb
            {'T': 76.85 (degC),
             'P': 101325}
            
        Add units:
            
            >>> sb.units['P'] = 'Pa'
            >>> sb
            {'T': 76.85 (degC),
             'P': 101325 (Pa)}
             
        A RuntimeWarning is issued when a value is set out of bounds:
            
            >>> sb['T'] = -300
            __main__:1: RuntimeWarning: @Operating conditions: T (-300 degC) is out of bounds.
            T should be within -273.15 to 726.85 degC.
        
    Nested SmartBook objects are easy to read, and can be made using the same units and bounds. A representative pandas DataFrame object can be created from the SmartBook object.
    
        Create new SmartBook objects:
        
            >>> sb1 = SmartBook(sb.units, sb.bounds,
            ...                 T=25, P=500)
            >>> sb2 = SmartBook(sb.units, sb.bounds,
            ...                 T=50, Duty=50)
            >>> sb1
            {'T': 25 (degC),
             'P': 500 (Pa)}
            >>> sb2
            {'T': 50 (degC),
             'Duty': 50 (kJ/hr)})
            
        Create a nested SmartBook object:
            
            >>> nsb = SmartBook(units=sb.units, sb1=sb1, sb2=sb2)
            {'sb1':
                {'T': 25 (degC),
                 'P': 500 (Pa)},
             'sb2':
                {'T': 50 (degC),
                 'Duty': 50 (kg/hr)}}
        
        Create DataFrame object:
            
            >>>  nsb.table()
                    Units Value
            sb1:               
              T      degC    25
              P        Pa   500
            sb2:               
              T      degC    50
              Duty  kJ/hr    50
    
    SmartBook objects assume bounds are inclusive, but may be set otherwise through the *inclusive* argument.
    
        Create SmarBook object excluding bound limits, with value at lower bound limit:
            
            >>> SmartBook(sb.units, sb.bounds, T=-273.15, inclusive={'T': (False, False)})
            __main__:1: RuntimeWarning: @Operating conditions: T (-273.15 degC) is out of bounds.
            T should be within -273.15 to 726.85 degC.
    
    `pint Quantity <https://pint.readthedocs.io/en/latest/>`__ objects are also compatible, so long as the corresponding Quantity class is set as the Quantity attribute.
    
        Set a Quantity object:
            
            >>> Q_ = SmartBook.Quantity
            >>> sb1.bounds['T'] = Q_((0, 1000), 'K')
            >>> sb1['T'] = Q_(100, 'K')
            >>> sb1
            {'T': -173.15 degC,
             'P': 500 (Pa)}
        
        Setting a Quantity object out of bounds will issue a warning:
            
            >>> sb1['T'] = Q_(-1, 'K')
             __main__:1: RuntimeWarning: T (-274.15 degC) is out of bounds.
             T should be within -273.15 to 726.85 degC.
        
        Trying to set a Quantity object with wrong dimensions will raise an error:
            
            >>> Q_ = SmartBook.Quantity    
            >>> sb1['T'] = Q_(100, 'meter')
            DimensionalityError: Cannot convert from 'meter' ([length]) to 'degC' ([temperature])
    
    .. Note:: Numpy arrays are also compatible with bounds checking. Give it a shot!
    
    """
    __slots__ = ('_source' ,'_units', '_bounds', 'inclusive')
    
    Quantity = Quantity
    
    def __init__(self, units={}, bounds={}, *args,
                 inclusive={}, source=None, **kwargs):
        # Make sure units is a UnitManager and add clients
        if isinstance(units, UnitManager):
            clients = units.clients
            clients.append(self)
        else:
            units = UnitManager([self], **units)
            clients = units.clients                
        if bounds not in clients:
            clients.append(bounds)
        
        # Set all attributes and items
        self._units = units
        self._bounds = bounds
        self._source = source
        self.inclusive = inclusive #: Dictionary of boolean pairs dictating whether or not to include lower and upper bounds.
        super().__init__(*args, **kwargs)
        
        # Make sure bounds are arrays for boundscheck
        for key, value in bounds.items():
            bounds[key] = asarray(bounds[key])
        
        # Check values
        for key, value in self.items():
            self.unitscheck(key, value)
            self.boundscheck(key, value)
    
    def __setitem__(self, key, value):
        self.unitscheck(key, value)
        self.boundscheck(key, value)
        dict.__setitem__(self, key, value)
    
    def unitscheck(self, key, value):
        """Adjust Quantity objects to correct units and return True."""
        if isinstance(value, self.Quantity):
            units = self._units.get(key, '')
            value.ito(units)
        return True
    
    def boundscheck(self, key, value, units=None, bounds=None):
        """Return True if within bounds. If value is out of bounds, return False and issue RuntimeWarning."""
        if bounds is None: bounds = self._bounds.get(key)
        if bounds is not None:
            # Include bound limits if inclusive values True
            lb, ub = bounds
            inclusive = self.inclusive.get(key)
            if inclusive:
                lb_include, ub_include = inclusive
                lbcheck = lb.__le__ if lb_include else lb.__lt__
                ubcheck = ub.__ge__ if ub_include else ub.__lt__
            else:
                lbcheck = lb.__le__
                ubcheck = ub.__ge__
                
            # Handle exception when value or bounds is a Quantity object but the other is not
            try:
                within_bounds = lbcheck(value).all() and ubcheck(value).all()
            except ValueError as VE:
                Q_ = self.Quantity
                units = units or self._units.get(key, '')
                value_is_Q = isinstance(value, Q_)
                bounds_is_Q = isinstance(bounds, Q_)
                if value_is_Q and not bounds_is_Q:           
                    # Use magnitude of value
                    value.ito(units)
                    value = value.magnitude
                    is_Q = 'value'
                    not_Q = 'bounds'                        
                elif bounds_is_Q and not value_is_Q:
                    # Use magnitude of bounds
                    bounds.ito(units)
                    bounds = bounds.magnitude
                    is_Q = 'bounds'
                    not_Q = 'value'                        
                elif (not bounds_is_Q) and (not value_is_Q):
                    # Bounds should be an array, try again
                    if not isinstance(bounds, ndarray):
                        self._bounds[key] = bounds = asarray(bounds)
                        return self.boundscheck(key, value, units, bounds)
                else:
                    raise VE
                # Warn to prevent bad usage of SmartBook
                name = "'" + key + "'" if isinstance(key, str) else key
                msg = f"For key, {name}, {is_Q} is a Quantity object, while {not_Q} is not."
                warn(self._warning(msg, RuntimeWarning), stacklevel=3)
                
                # Try again with matching value and bound types
                return self.boundscheck(key, value, units, bounds)
            
            # Warn when value is out of bounds
            if not within_bounds:
                # Make sure correct units are used
                units = units or self._units.get(key, '')
                if units:
                    Q_ = self.Quantity
                    if isinstance(value, Q_):
                        value.ito(units)
                        value = value.magnitude
                    else:
                        units = ' ' + units
                
                # Handle format errors
                try:
                    msg = f"{key} ({value:.4g}{units}) is out of bounds. {key} should be within {lb:.4g} to {ub:.4g}{units}."
                except:
                    msg = f"{key} ({value}{units}) is out of bounds. {key} should be within {lb} to {ub}{units}."
                
                warn(self._warning(msg, RuntimeWarning), stacklevel=3)
                
            return within_bounds
    
    @classmethod
    def enforce_boundscheck(cls, val):
        """If *val* is True, issue RuntimeWarning whenever an item is set out of bounds. If *val* is False, ignore bounds."""
        if val:
            cls.boundscheck = cls._boundscheck
        else:
            cls.boundscheck = cls._boundsignore

    @classmethod
    def enforce_unitscheck(cls, val):
        """If *val* is True, adjust Quantity objects to correct units. If *val* is False, ignore units."""
        if val:
            cls.unitscheck = cls._unitscheck
        else:
            cls.unitscheck = cls._unitsignore
     
    _boundscheck = boundscheck
    _unitscheck = unitscheck
    def _boundsignore(*args, **kwargs): pass
    def _unitsignore(*args, **kwargs): pass    

    @property
    def units(self):
        """Dictionary of units of measure."""
        return self._units
    
    @units.setter
    def units(self, units):
        bounds = self._bounds
        old_clients = self.units.clients
        
        # Remove self and bounds from clients
        old_clients.remove(self)
        if bounds: old_clients.remove(bounds)
        
        # Add self and bounds as clients
        if isinstance(units, UnitManager):
            new_clients = units.clients
            if self not in new_clients: new_clients.append(self)
            if bounds not in new_clients: new_clients.append(bounds)
        else:
            units = UnitManager([self, bounds], **units)
            
        self._units = units
    
    @property
    def bounds(self):
        """Dictionary of bounds."""
        return self._bounds
    
    @bounds.setter
    def bounds(self, bounds):
        for key, value in bounds.items():
            bounds[key] = asarray(bounds[key])
        clients = self.units.clients
        clients.remove(self._bounds)
        if bounds not in clients: clients.append(bounds)    
        self._bounds = bounds
    
    @property
    def source(self):
        """Object or string denoting what the SmartBook object pertains to."""
        return self._source
        
    def nested_keys(self):
        """Return all keys of self and nested SmartBook objects."""
        for key, val in self.items():
            if isinstance(val, SmartBook) and not val is self:
                for key in val.nested_keys():
                    yield key
            else:    
                yield key
    
    def nested_values(self):
        """Return all values of self and nested SmartBook objects."""
        for key, val in self.items():
            if isinstance(val, SmartBook) and not val is self:
                for val in val.nested_values():
                    yield val
            else:    
                yield val
    
    def nested_items(self):
        """Return all key-value pairs of self and nested SmartBook objects."""
        for key, val in self.items():
            if isinstance(val, SmartBook) and not val is self:
                for item in val.nested_items():
                    yield item
            else:    
                yield key, val
    
    def table(self, with_units=True):
        """Return a representative DataFrame object."""
        Q_ = self.Quantity
        udict = self._units
        obj = self._source
        if obj:
            Value = str(obj)
            Title = type(obj).__name__  if not isinstance(obj, str) else ''
        else:
            Value = 'Value'
            Title = ''
        if with_units:
            columns = ('Units', Value)
            
            def add_values(key, val, udict):
                units = udict.get(key, '')
                if units and isinstance(val, Q_):
                    val.ito(units)
                    val = val.magnitude
                data.append((units, val))
            
            def add_recursion(key, val):
                data.append(('[...]', ''))
            
            def add_nothing():
                data.append(('', ''))
        else:
            columns = (Value,)
            
            def add_values(key, val, udict):
                units = udict.get(key, '')
                if units and isinstance(val, Q_):
                    val.ito(units)
                    val = val.magnitude
                data.append(val)
            
            def add_recursion(key, val):
                data.append('[...]')
            
            def add_nothing():
                data.append('')
        
        previous_dicts = [self]
        data = [] # units, values
        index = []
        
        def add_row(key, val, N_recursive, udict):
            new_key = N_recursive*'  ' + key
            if isinstance(val, dict):
                if val in previous_dicts:
                    add_recursion(key, val)
                elif val:
                    index.append(new_key + ':')
                    add_block(key, val, N_recursive)
            else:
                index.append(new_key)
                add_values(key, val, udict)
        
        def add_block(key, current_dict, N_recursive):
            previous_dicts.append(current_dict)
            N_recursive += 1
            add_nothing()
            if current_dict:
                udict = current_dict.units
                for key, val in current_dict.items():
                    add_row(key, val, N_recursive, udict)    
            N_recursive -= 1
            del previous_dicts[-1]
                
        for key, val in self.items():
            add_row(key, val, 0, udict)
        
        df = DataFrame(data, index, columns)
        df.columns.name = Title
        return df
    
    def _warning(self, msg, category=Warning):
        """Return a Warning object with source description."""
        obj = self._source
        
        name = str(obj)
        if len(name) > 20:
            name = name[:20] + '...'
        
        if isinstance(obj, str):
            msg = f'@{obj}: ' + msg
        elif obj:
            msg = f'@{type(obj).__name__} {str(obj)}: ' + msg
        
        return category(msg)
    
    def show(self, depth=1):
        """Print representation with specified *depth*.
        
        **Parameters**
        
            **depth:** [int] Number of nested dictionaries represented.
        
        """
        print(self._info([], 0, depth))
    
    def __repr__(self):
        return self._info()
    
    def _info(self, previous_dicts=[], N_recursive=0, depth=1):
        if depth < 0:
            raise ValueError(f'depth must be 0 or higher, not {depth}.')
        add_line = self._info_item
        udict = self._units
        out = ''
        
        # N_recursive: Number of SmartBook recursions
        N_spaces = 4*(N_recursive)
        if N_recursive == 0:
            new_line = ''
        elif N_recursive < depth+1:
            new_line = '\n' + N_spaces*' '
        else:
            return f'<{type(self).__name__}>,\n '
        N_recursive += 1
        
        if self:
            # Log self to prevent infinite recursion later
            previous_dicts.append(self)
            
            # Add lines of key/value pairs
            out += new_line + '{'
            for key, value in self.items():
                units = udict.get(key, '')
                out += add_line(key, value, units, previous_dicts, N_recursive, depth)
            out = out[:-(4*N_recursive - 1)] + '},\n '
            
            # Log out self
            del previous_dicts[-1]
        else:
            out += new_line + '{},\n '
        
        if N_recursive == 1:
            return out[:-4] + '}'
        else:
            return out
    
    def _info_item(self, key, value, units, previous_dicts, N_recursive, depth):
        """Represent key/value pair."""
        Q_ = self.Quantity
        out = f"'{key}': "
        
        if isinstance(value, dict):
            if value in previous_dicts:
                # Prevent infinite recursion
                out += "{...},\n "
            elif value and isinstance(value, SmartBook):
                # Pretty representation of inner smart book
                out += value._info(previous_dicts, N_recursive, depth)
            else:
                # Normal representation of dictionaries
                out += repr(value) + ',\n '
        else:
            if units:
                if isinstance(value, Q_):
                    value.ito(units)
                    value = value.magnitude
                    units = ' ' + units
                else:
                    units = dim(' (' + units + ')')
            
            # Values may not have g-format, so handle exception
            try:
                out += f"{value:.3g}{units},\n "
            except:
                out += f"{value}{units},\n "
        
        # Include spaces for next line
        out += 4*(N_recursive - 1)*' '
        return out