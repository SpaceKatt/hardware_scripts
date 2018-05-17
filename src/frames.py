class Frame():
  def __init__(self, frame_number=0):
    self.reference_bit = True
    self.dirty_bit = False
    self.frame_number = frame_number

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
    string_repr = "[" + str(self.getFrameNum()) + ", " \
                + str(int(self.getRefBit())) + "]"
    return string_repr

class Clock():
  def __init__(self, frames, debug=False):
    self.pointer = 0
    self.frame_list = []
    self.debug = debug
    for x in range(frames):
      self.frame_list.append(Frame())
    if self.debug:
      self.print_frames()

  def print_frames(self):
    for i in range(len(self.frame_list)):
      frame = self.frame_list[i]
      print("{} ".format(frame), end="")

  def do_thing(self, page_string):
    for char in page_string:
      frame_num = int(char)
      if self.hasFrame(frame_num):
        if self.debug:
          print(3 * '-' + " Found frame in table: " + str(frame_num))
      else:
        self.replaceFrame(frame_num)
      if self.debug:
        self.print_frames()
    if self.debug:
      print(3 * '_' + ' FINISHED!!!')
    return self.frame_list

  def hasFrame(self, frame_num):
    for frame in self.frame_list:
      if frame.getFrameNum() == frame_num:
        return True
    return False

  def replaceFrame(self, frame_num):
    while self.frame_list[self.pointer].getRefBit():
      self.frame_list[self.pointer].clearRefBit()
      self.pointer = (self.pointer + 1) % len(self.frame_list)
    self.frame_list[self.pointer] = Frame(frame_num)
    if self.debug:
      print(3 * '-' + " Replace index " + str(self.pointer) \
            + " with frame " + str(frame_num))
    self.pointer = (self.pointer + 1) % len(self.frame_list)




if __name__ == '__main__':
  INST = Clock(3, True)

  PAGE_STRING = '68691418328914'
  INST.do_thing(PAGE_STRING)

  INST = Clock(3)
  print(INST.do_thing(PAGE_STRING))
