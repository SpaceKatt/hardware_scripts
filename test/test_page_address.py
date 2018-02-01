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

from ..src.page_address_calc import AddressParser as ap

def test_page_0():
    '''a'''
    addy = ap(4, 4, 0)
    address = addy.get_start_end(0)
    assert address[0] == '0x00'
    assert address[1] == '0x0F'

def test_page_1():
    '''ITS NOT EMPTY'''
    assert True
