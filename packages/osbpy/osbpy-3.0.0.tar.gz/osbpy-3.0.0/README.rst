
osbpy
=====

osbpy is a simple library for creating storyboards for the game osu!. It can help you automate the process of creating a high number of storyboard objects, but even to make very advanced effects.

What can it do?
===============

It supports all functions of storyboarding that osu! does, including triggers and loops. The only exception are the storyboard hitsounds, because it has no use for people who create storyboards.

Additionally, you can generate an audio spectrum data from an audio file and use that with your objects to create a visual spectrum very easily.

Am I allowed to change the library?
===================================

Of course. The library is using MIT license. As long as you follow its simple conditions, I don't mind you using or distributing this library in any way.

If you want to modify other libraries that this library is using, please follow their license. This license only applies to files that are included on this repository.

Requirements
============

This library requires:


* Python (3.6+), I will always update osbpy to the newest version.
* numpy 1.10.4+ + MKL
* matplotlib 1.5.1+
* scipy 0.17.0+
  All these libraries can be easily installed with pip except for numpy+mkl. You will need to get it from an external source, such as https://www.lfd.uci.edu/~gohlke/pythonlibs/ or you can use the Intel Distribution for Python* which includes all of the required libraries.

Installation
============

.. code-block::

   pip install osbpy
