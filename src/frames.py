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

This script generates the evolution of a page table, given separate victim
  selection algorithms (FIFO, Second Chance, Enhanced Second Chance).
'''


class Frame():
    '''
    Represents a physical frame in memory. A frame has a number associated
    with it, which corresponds to the location on the physical disk. These
    frames are place into a page table, so logical page numbers can be mapped
    to these physical frames.

    A reference bit is set to signal that a frame was recently referenced, and
      cleared once it hasn't been referenced recently

    A dirty bit is set when
    '''
    def __init__(self, frame_number=-1, short_string=False):
        if frame_number == -1:
            self.reference_bit = False
        else:
            self.reference_bit = True
        self.dirty_bit = False
        self.frame_number = frame_number
        self.short_string = short_string

    def get_frame_num(self):
        '''Get the physical frame number'''
        return self.frame_number

    def get_ref_bit(self):
        '''Read reference bit'''
        return self.reference_bit

    def get_dirty_git(self):
        '''Read dirty bit'''
        return self.dirty_bit

    def clear_dirty_bit(self):
        '''Indicates that page has been written back to disk.'''
        self.dirty_bit = False

    def set_dirty_bit(self):
        '''
        Page has been modified and nees to be written back to disk.
        '''
        self.dirty_bit = True

    def clear_ref_bit(self):
        '''
        Page has been set as a replacement candidate.
        '''
        self.reference_bit = False

    def set_ref_bit(self):
        '''
        Page has been recently referenced.
        '''
        self.reference_bit = True

    def __repr__(self):
        if self.get_frame_num() == -1:
            number = '--'
        else:
            number = self.get_frame_num()
        if self.short_string:
            string_repr = "[{0:0>2}]".format(number)
        else:
            string_repr = "[{0:0>2}, {1}, {2}]"
            string_repr = string_repr.format(number, int(self.get_ref_bit()),
                                             int(self.get_dirty_git()))
        return string_repr


class PageTable():
    def __init__(self, frames, terse_output=False):
        self.formatted_table = ''
        self.terse_output = terse_output
        self.pointer = 0
        self.frame_list = []
        self.number_of_pages = frames
        self.page_array = []
        for _ in range(self.number_of_pages):
            self.frame_list.append(Frame(short_string=terse_output))

    def print_frames(self):
        print("{} ".format(self.get_table_string(), end=""))

    def get_table_string(self):
        frame_table = ''
        if self.number_of_pages < 1:
            frame_table = 'No table!!!'
            return
        for i in range(len(self.frame_list)):
            frame_table += "{} ".format(self.frame_list[i])
        return frame_table[:-1]

    def evolve_formatted_table(self, message):
        self.formatted_table += "{} --- {}\n".format(self.get_table_string(),
                                                     message)

    def get_whole_table(self):
        return self.formatted_table

    def parse_page_string(self, page_string):
        self.page_array = page_string.split(',')
        for element in self.page_array:
            try:
                int(element)
            except ValueError:
                raise ValueError('Frame numbers can only be integers... '
                                 + ' Try again, you idiot n___n')
            if int(element) > 99 or int(element) < 0:
                raise ValueError('Frames must be between 0 and 99, inclusive')

    def second_chance(self, page_string):
        self.parse_page_string(page_string)
        self.evolve_formatted_table('Cold start cache')
        for char in self.page_array:
            frame_num = int(char)
            if self.has_frame(frame_num):
                mess = "Found frame in table: {}".format(frame_num)
                self.evolve_formatted_table(mess)
            else:
                self.replace_frame_second_chance(frame_num)
        self.evolve_formatted_table(' FINISHED!!!')
        return self.get_whole_table()

    def has_frame(self, frame_num):
        for frame in self.frame_list:
            if frame.get_frame_num() == frame_num:
                return True
        return False

    def replace_frame_second_chance(self, frame_num):
        while self.frame_list[self.pointer].get_ref_bit():
            self.frame_list[self.pointer].clear_ref_bit()
            self.pointer = (self.pointer + 1) % len(self.frame_list)
        self.frame_list[self.pointer] = Frame(frame_num,
                                              short_string=self.terse_output)
        message = "Replace index {} with frame {}".format(self.pointer,
                                                          frame_num)
        self.evolve_formatted_table(message)
        self.pointer = (self.pointer + 1) % len(self.frame_list)


if __name__ == '__main__':
    INST = PageTable(3, True)

    PAGE_STRING = '6,8,6,2,1,4,1,8,3,2,8,9,1,4'
    INST.second_chance(PAGE_STRING)

    INST = PageTable(3)
    print(INST.second_chance(PAGE_STRING))

    INST = PageTable(3, terse_output=True)
    print(INST.second_chance(PAGE_STRING))

    INST = PageTable(3, terse_output=True)
    PAGE_STRING = '3,5,7,3,3,6,7,3,5,4,6,7,5'
    print(INST.second_chance(PAGE_STRING))
