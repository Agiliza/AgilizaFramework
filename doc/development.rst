=================================
 Agiliza Core development manual
=================================
-------------
 Style Guide
-------------

:Authors:
    Vicente Ruiz Rodríguez

:Version: 0.1 of 2012/03


Chapter 1 Component Design
==========================

Component directory name = Component name

For example: Resource -> resources, Template -> templates

Directory structure:
::
    component/
        \ -- __init__.py
        \ -- base.py
        \ -- interface.py

``__init__.py`` must import, at least, its base and interface if they
are present.

``interface.py`` contains the interface of the component, if it's
required. Furthermore, this interface can use a Metaclass. It will
included in this file.

``base.py`` contains a useful implementation of the component (not
always makes sense, it's depend of component).


Section 1.1 Component Metaclass
-------------------------------

Included on `component/interface.py` file.


Section 1.2 Component Interface
-------------------------------

Included on `component/interface.py` file.


Section 1.3 Component Base
--------------------------

Included on `component/base.py` file.
