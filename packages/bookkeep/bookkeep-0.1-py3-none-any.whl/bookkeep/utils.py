# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 08:12:55 2018

@author: yoelr
"""
from colorama import Fore, Style

def dim(string):
    """Return string with gray ansicolor coding."""
    return Fore.WHITE + Style.NORMAL + string + Style.RESET_ALL
