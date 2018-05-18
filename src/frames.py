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
    def __init__(self, frame_number=0, short_string=False):
        self.reference_bit = True
        self.dirty_bit = False
        self.frame_number = frame_number
        self.short_string = short_string

    def getFrameNum(self):
        return self.frame_number

    def getRefBit(self):
        return self.reference_bit

    def getDirtyBit(self):
        return self.dirty_bit

    def clearDirtyBit(self):
        self.dirty_bit = False

    def setDirtyBit(self):
        self.dirty_bit = True

    def clearRefBit(self):
        self.reference_bit = False

    def setRefBit(self):
        self.reference_bit = True

    def __repr__(self):
        if self.short_string:
            string_repr = "[{}]".format(self.getFrameNum())
        else:
            string_repr = "[{}, {}, {}]".format(self.getFrameNum(),
                                                int(self.getRefBit()),
                                                int(self.getDirtyBit()))
        return string_repr

class Clock():
    def __init__(self, frames, debug=False, terse_output=False):
        self.formatted_table = ''
        self.terse_output = terse_output
        self.pointer = 0
        self.frame_list = []
        self.debug = debug
        self.number_of_pages = frames
        for _ in range(self.number_of_pages):
            self.frame_list.append(Frame(short_string=terse_output))
        # if self.debug:
            # self.print_frames()

    def print_frames(self):
        print("{} ".format(self.get_table_string(), end=""))

    def get_table_string(self):
        frame_table = ''
        if self.number_of_pages < 1:
            frame_table = 'No table!!!'
            return
        for i in range(len(self.frame_list)):
            frame_table += "{} ".format(self.frame_list[i])
        return frame_table

    def evolve_formatted_table(self, message):
        self.formatted_table += "{} --- {}\n".format(self.get_table_string(),
                                                   message)

    def get_whole_table(self):
        return self.formatted_table

    def do_thing(self, page_string):
        self.evolve_formatted_table('Cold start cache')
        for char in page_string:
            frame_num = int(char)
            if self.hasFrame(frame_num):
                mess = "Found frame in table: {}".format(frame_num)
                self.evolve_formatted_table(mess)
            else:
                self.replaceFrame(frame_num)
            # if self.debug:
                # self.print_frames()
        self.evolve_formatted_table(' FINISHED!!!')
        return self.get_whole_table()

    def hasFrame(self, frame_num):
        for frame in self.frame_list:
            if frame.getFrameNum() == frame_num:
                return True
        return False

    def replaceFrame(self, frame_num):
        while self.frame_list[self.pointer].getRefBit():
            self.frame_list[self.pointer].clearRefBit()
            self.pointer = (self.pointer + 1) % len(self.frame_list)
        self.frame_list[self.pointer] = Frame(frame_num, short_string=self.terse_output)
        message = "Replace index {} with frame {}".format(self.pointer,
                                                          frame_num)
        self.evolve_formatted_table(message)
        self.pointer = (self.pointer + 1) % len(self.frame_list)

if __name__ == '__main__':
    INST = Clock(3, True)

    PAGE_STRING = '68691418328914'
    INST.do_thing(PAGE_STRING)

    INST = Clock(3)
    print(INST.do_thing(PAGE_STRING))

    INST = Clock(3, terse_output=True)
    print(INST.do_thing(PAGE_STRING))
