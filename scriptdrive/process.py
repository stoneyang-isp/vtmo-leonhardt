from multiprocessing import Process
import multiprocessing
import time


class Processor(Process):
  def __init__(self, from_, to):
    Process.__init__(self)

    self.from_ = from_
    self.to = to

  def run(self):
    while True:
      if self.from_._closed:
        self.to.close()
        break
      content = self.from_.get()
      print content
      time.sleep(2)
      self.to.put(content + "_finished")
      self.from_.task_done()
    return


if __name__ == "__main__":

  processors = []
  tos = []
  froms = []

  for i in range(1):
    to = multiprocessing.JoinableQueue()
    from_ = multiprocessing.JoinableQueue()
    tos.append(to)
    froms.append(from_)
    processor = Processor(from_, to)
    processors.append(processor)
    processor.start()

  for from_ in froms:
    from_.put("aerg")

  for to in tos:
    to.get()

  for from_ in froms:
    from_.join()
    from_.close()

  for processor in processors:
    processor.terminate()



