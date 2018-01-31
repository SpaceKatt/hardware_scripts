        # TODO: complete documentation
        # TODO: add to discord bot
class AddressParser:
    '''
    '''
    # The number of page bits
    page_bits = 0
    # The number of offfset bits
    offs_bits = 0
    # The number of byte-selector bits
    byte_bits = 0
    # The number of bits in our address
    total_bits = 0
    # The length of the hex address
    hex_length = 0

    def __init__(self, page, offset, byte_sel):
        '''Initializes the data members of our object'''
        self.page_bits = page
        self.offs_bits = offset
        self.byte_bits = byte_sel
        self.total_bits = page + offset + byte_sel
        self.hex_length = self.get_hex_length()

    def to_hex(self, bin_num):
        '''
        '''
        value = hex(int(bin_num, 2))[2:].upper()
        value = '0x' + value.zfill(self.hex_length)
        return value

    def get_hex_length(self):
        length = 1
        while length * 4 < self.total_bits:
            length += 1
        return length

    def get_page(self, page_num):
        '''
        '''
        page_bin = "{0:b}".format(page_num)
        return page_bin

    def get_ending(self, is_start):
        '''
        '''
        remaining_bits = self.offs_bits + self.byte_bits
        if is_start:
            return '0' * remaining_bits
        else:
            return '1' * remaining_bits

    def get_address(self, page_num, is_start):
        '''
        '''
        page = self.get_page(page_num)
        offset_byte_sel = self.get_ending(is_start)

        address = page + offset_byte_sel
        return self.to_hex(address).zfill(self.hex_length)

    def is_valid_page(self, page_num):
        return (page_num < 2 ** self.page_bits and page_num >= 0)

    def get_start_end(self, page_num):
        '''
        Retruns the starting and ending address of a page.
        '''
        if not self.is_valid_page(page_num):
            return "Invalid page number"
        result = "Chip summary:\n"
        result += "Page bits: {}, Offset bits: {}, Byte-select bits: {}\n"
        result = result.format(self.page_bits, self.offs_bits, self.byte_bits)
        result += "Addresses for page number {}:\n".format(page_num)
        result += "Start: " + self.get_address(page_num, True) + '\n' 
        result += "End:   " + self.get_address(page_num, False)
        return result

if __name__ == '__main__':
    addre = AddressParser(4, 13, 0)
    print('-------------------------------------------------')
    print(addre.get_start_end(0))
    print('-------------------------------------------------')
    print(addre.get_start_end(1))
    print('-------------------------------------------------')
    print(addre.get_start_end(7))
    print('-------------------------------------------------')
    print(addre.get_start_end(15))
    print('-------------------------------------------------')

    addre = AddressParser(11, 17, 2)
    print('-------------------------------------------------')
    print(addre.get_start_end(0))
    print('-------------------------------------------------')
    print(addre.get_start_end(17))
    print('-------------------------------------------------')
    print(addre.get_start_end(381))
    print('-------------------------------------------------')
    print(addre.get_start_end(1024))
    print('-------------------------------------------------')
    print(addre.get_start_end(1094))
    print('-------------------------------------------------')
    addre = AddressParser(13, 17, 0)
    print('-------------------------------------------------')
    print(addre.get_start_end(0))
    print('-------------------------------------------------')
    print(addre.get_start_end(17))
    print('-------------------------------------------------')
    print(addre.get_start_end(381))
    print('-------------------------------------------------')
    print(addre.get_start_end(1024))
    print('-------------------------------------------------')
    print(addre.get_start_end(1094))
    print('-------------------------------------------------')
