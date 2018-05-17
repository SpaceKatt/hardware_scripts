'''
------------------------------- LICENSE ---------------------------------------
hardware_scripts; Basic scripts to validate my work in my hardware class
Copyright (C) 2018, Thomas Kercheval

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-------------------------------------------------------------------------------
'''

from ..src.boolean_expr_parser import BooleanExpr as be

def result_equality(unknown, known):
    '''
    Returns true if two 2D lists are equal.
    '''
    if (len(unknown) != len(known) or len(unknown[0]) != len(known[0])):
        return False
    for i in range(len(unknown)):
        for j in range(len(unknown[0])):
            if unknown[i][j] != known[i][j]:
                return False
    return True


def test_not():
    '''Tests the boolean function NOT'''
    known = [[0, 1],
             [1, 0]]
    booly = be("!A")
    assert result_equality(booly.generate_table_values(['A']), known)

def test_or():
    '''Tests the boolean function OR'''
    pass

def test_xor():
    '''Tests the boolean function XOR'''
    pass

def test_and():
    '''Tests the boolean function AND'''
    pass
