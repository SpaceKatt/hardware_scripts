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

Defines an page address calculator to be used to verify homework questions
in my hardware class.

Unit tests are distributed in,
    https://github.com/SpaceKatt/hardware_scripts
'''

class AddressParser(object):
    '''
    Calculates the addresses for the beginning and end of pages given
    a specific memory chip. Chips are defined by the number of page, offset,
    and byte-selector bits in its address space. Pages that cannot
    exist within the chip will not have valid addresses, thus this
    parser will not generate them (rather return an error message).

    To get the start and end addresses for page number 7 of a chip
    with 3 paging bits, 4 offset bits, and 5 byte-selector bits, we
    would do the following:
    >>> addy = AddressParser(3, 4, 5)
    >>> print(addy.get_start_end(7))
    '''
    # The number of page bits
    page_bits = 0
    # The number of offfset bits
    offs_bits = 0
    # The number of byte-selector bits
    byte_bits = 0
    # The number of bits in our address
    total_bits = 0
    # The length of the absolute hex address for our memory chip
    hex_length = 0

    def __init__(self, page, offset, byte_sel):
        '''
        Initializes the data members of our object, obviously
        '''
        self.page_bits = page
        self.offs_bits = offset
        self.byte_bits = byte_sel
        self.total_bits = page + offset + byte_sel
        self.hex_length = self.get_hex_length()

    def to_hex(self, bin_num):
        '''
        From a binary bumber, `bin_num`, convert it into its hexadecimal
        representation (with uppercase letters). Also pads the hex number
        with zeros in order to make it into an absolute address.
        '''
        value = hex(int(bin_num, 2))[2:].upper()
        value = '0x' + value.zfill(self.hex_length)
        return value

    def get_hex_length(self):
        '''
        Calculates the total length of a hexadecimal address for a
        specific memory chip (e.g., a chip with 17 total bits will
        have a hexidecimal address that is 5 characters long).
        '''
        length = 1
        while length * 4 < self.total_bits:
            length += 1
        return length

    def get_ending(self, is_start):
        '''
        Returns the binary representation of the offset and byte-selector
        bits. Since we are only concerned with the beginning or end
        of a page's address, these bits will either all be zero or all
        be one, if it is the start or end (respectively).

        `is_start` indicates whether we are generating the start or end
        of the page's address.
        '''
        remaining_bits = self.offs_bits + self.byte_bits
        if is_start:
            # The start of page has all offset and byte-selector bits at zero
            return '0' * remaining_bits
        # Else, the end has all offset and b-s bits at one
        return '1' * remaining_bits

    def get_address(self, page_num, is_start):
        '''
        Returns the absolute address of a specific page. Whether we
        are at the start or end of the page is indicated by `is_start`.
        '''
        # Get the page number in its binary representation
        page = "{0:b}".format(page_num)
        # Get the offset and byte-selector bits
        offset_byte_sel = self.get_ending(is_start)

        address = page + offset_byte_sel
        # Return the absolute hex address
        return self.to_hex(address)

    def is_valid_page(self, page_num):
        '''
        Valid page numbers are non-negative and less than 2 to the
        power of the number of page bits we have.
        '''
        return page_num < 2 ** self.page_bits and page_num >= 0

    def get_start_end(self, page_num):
        '''
        Returns the starting and ending address of a page.
        '''
        if not self.is_valid_page(page_num):
            return "Invalid page number"
        result = []
        # Get the start address
        result.append(self.get_address(page_num, True))
        # Get the end address
        result.append(self.get_address(page_num, False))
        return result

    def get_formatted_page_results(self, page_num):
        '''
        Formats results in a pretty fashion for display.
        '''
        if not self.is_valid_page(page_num):
            return "Invalid page number"
        page_addresses = self.get_start_end(page_num)
        result = "Chip summary:\n"
        result += "Page bits: {}, Offset bits: {}, Byte-select bits: {}\n"
        result = result.format(self.page_bits,
                               self.offs_bits,
                               self.byte_bits)
        result += "Addresses for page number {}:\n".format(page_num)
        result += "Start: " + page_addresses[0] + '\n'
        result += "End:   " + page_addresses[1]
        return result

if __name__ == '__main__':
    ADDRE = AddressParser(4, 13, 0)
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(0))
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(1))
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(7))
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(15))
    print('-------------------------------------------------')

    ADDRE = AddressParser(11, 17, 2)
    print(ADDRE.get_formatted_page_results(0))
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(17))
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(381))
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(1024))
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(1094))
    print('-------------------------------------------------')

    ADDRE = AddressParser(13, 17, 0)
    print(ADDRE.get_formatted_page_results(0))
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(17))
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(381))
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(1024))
    print('-------------------------------------------------')
    print(ADDRE.get_formatted_page_results(1094))
    print('-------------------------------------------------')
