# def test1():
#     for val in test2():
#         print(val)
#
# def test2():
#     for i in range(5):
#         yield i
#
# test1()

# mylst = [[1,2], [3,4], [5,6]]
# # print(mylst[1])
#
# for line in mylst:
#     if line == mylst[0]:
#         print('yes')
#     else:
#         print('no')

# from geographiclib.geodesic import Geodesic
#
# lat1 = 43.6532
# lon1 = -79.3832
# lat2 = 49.8951
# lon2 = -97.1384
#
#
# res = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)
# print(res['azi1'])


# mylist = [(round(x * 0.1, 1), x) for x in range(0, 50)]
# for val in mylist:
#     print(val)

# x = [[1,2,3], [4,5,6], [7,8,9]]
# for item in x:
#     y = ','.join(str(val) for val in item)
#     print(y)

# a = b = c = 1
# d = []
# d.append([a,b,c])
# # print(d)
# for item in d:
#     x = ','.join(str(i) for i in item)
#     print(x)

# from os import listdir
# import os
# optInDir = r'C:\Projects\dataCompression\data\clean_tracks'
#
#
# for filename in listdir(optInDir):
#     if filename.endswith('.csv'):
#         # print(filename)
#         fpath = os.path.join(optInDir, filename)
#         with open(fpath, newline='') as f:
#             for line in f:
#                 print(line)

# def frange(start, stop=None, step=None):
#     # flt_range = []
#     #Use float number in range() function
#     # if stop and step argument is null set start=0.0 and step = 1.0
#     if stop == None:
#         stop = start + 0.0
#         start = 0.0
#     if step == None:
#         step = 1.0
#     while True:
#         if step > 0 and start >= stop:
#             break
#         elif step < 0 and start <= stop:
#             break
#         yield start
#         start = start + step
#         # yield ("%g" % start) # return float number
#     # return flt_range
#
#
# width = (370.-204.)/30
# for i in frange(204., 370., width):
#      print(i, i+width)

# import matplotlib.pyplot as plt
# import numpy as np
#
#
# def f(t):
#     'A damped exponential'
#     s1 = np.cos(2 * np.pi * t)
#     e1 = np.exp(-t)
#     return s1 * e1
#
#
# t1 = np.arange(0.0, 5.0, .2)
#
# l = plt.plot(t1, f(t1), 'ro')
# plt.setp(l, markersize=30)
# plt.setp(l, markerfacecolor='C0')
#
# plt.show()

# def tester(dict1):
#     # for key in dict1:
#     #     print(key, dict1[key].get())
#
#     if dict1['Length'].get() == 1:
#         print('You got length = 1')
#     if dict1['Length'].get() == 0:
#         print('You got length = 0')
#     if dict1['gpsFolder'].get():
#         print('You selected:', dict1['gpsFolder'].get())
#     else:
#         print('Hello')

from tkinter import *
root = Tk()

def fetch():
    print('var1', var1.get())
    print('var2', var2.get())
    print('var3', var3.get())

var1 = IntVar()
Checkbutton(root, text='Val1', variable=var1).pack()

var2 = IntVar()
Checkbutton(root, text='Val2', variable=var2).pack()

var3 = IntVar()
Checkbutton(root, text='Val3', variable=var3).pack()


Button(root, text='Fetch', command=fetch).pack()


root.mainloop()