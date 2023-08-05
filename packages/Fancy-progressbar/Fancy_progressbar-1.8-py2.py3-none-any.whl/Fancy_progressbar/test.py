import Fancy_progressbar as bar
import time
import threading

b = bar.Progress_bar(taskname='dead')
bars = [bar.Progress_bar(taskname=str(i)) for i in range (5)]

f2 =  bar.Progress_bar_family(list=[bar.Progress_bar(taskname=str(i)) for i in range (15,20)], taskname='yay3')

f = bar.Progress_bar_family(list=[*bars, f2], taskname='yay')

f1 = bar.Progress_bar_family(list=[b, f], taskname='yay2')


# threading.Thread(target=rm, args=(bars, )).start()
h = bar.Progress_bar_handler(f1)
h.start()