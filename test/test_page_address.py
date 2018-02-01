'''aaa'''
from ..page_address_calc import AddressParser as ap

def test_page_0():
    '''a'''
    addy = ap(4, 4, 0)
    address = addy.get_start_end(0)
    assert address[0] == '0x00'
    assert address[1] == '0x0F'
