"""
This module has the intention to contain the marker interfaces for grouping the implementations in Service Locator

@author: Alexander Escalona Fernández
"""


class Repository:
    def __str__(self):
        return 'Repository'


class Controller:
    def __str__(self):
        return 'Controller'


class Service:
    def __str__(self):
        return 'Service'