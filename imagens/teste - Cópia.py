
from tkinter import *
root=Tk()
b=Button(root)
photo=PhotoImage(file="fill.gif")
b.config(image=photo)
b.grid(row = 0, column = 0)
root.mainloop()
