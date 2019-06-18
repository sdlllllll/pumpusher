from tkinter import *
from tkinter import ttk # also import the themed tkinter for good looking widgets (not obligatory)
 
      
class Widget:
   def __init__(self):
      self.speeddictionary={}
      self.timedictionary={}
      self.intervaldictionary={}
      window = Tk()
      window.title("The amazing pump")
      window.resizable(0,0) # prohibit resizing the window
      
      text =ttk.Label(window, text = "How many rounds do you need:")
      text.grid(row=0, column=0, sticky=W)
      
      self.entry_id=StringVar() # create an id for your entry, this helps getting the text
      entry = ttk.Entry(window, textvariable=self.entry_id, justify=RIGHT)
      entry.grid(row=0, column=1, sticky=E)
      
      button = ttk.Button(window, text='Next', command=self.clicked)
      button.grid(row=2, column=1, sticky=E)
      window.bind("<Return>", self.clicked) # handle the enter key event of your keyboard
      button.bind("<Button-1>", self.clicked) # bind the action of the left button of your mouse to the button assuming your primary click button is the left one.
      
      window.mainloop() # call the mainloop function so the window won't fade after the first execution
 
 
   def clicked(self): #open a new window for next steps
      self.rounds = int(self.entry_id.get())
      button1=self.new_winF()
      button1.pack()
         
   def sclicked(self,thespeed=0): #wheneven click a save for s, save the step and its value of entry in the dictionary created
      thespeed = self.entry_s.get()
      self.speeddictionary[self.news]=thespeed
      print(self.speeddictionary)
      
   def tclicked(self,thetime=0):
      thetime = self.entry_t.get()
      self.timedictionary[self.newt]=thetime
      print(self.timedictionary)
      
   def iclicked(self,theinterval=0):
      theinterval = self.entry_i.get()
      self.intervaldictionary[self.newi]=theinterval
      print(self.intervaldictionary)
      
   def new_winF(self):# new window definition, based on what we got from the original window
      newwin = Toplevel()
    
      for i in (0,self.rounds): ####looks weird:I want to generate a new s/t/i for each loop of entries
        self.news=str("s"+str(i))
        self.newt=str("t"+str(i))
        self.newi=str("i"+str(i))
        
        self.news = ttk.Label(newwin, text='Speed:')
        self.news.grid(row=0+i*6, column=0, sticky=W)
        self.entry_s = StringVar()
        newsentry=ttk.Entry(newwin,textvariable=self.entry_s, justify=RIGHT)
        newsentry.grid(row=0+i*6, column=1, sticky=E)
        button = ttk.Button(newwin, text='Save', command=self.sclicked)
        button.grid(row=1+i*6, column=1, sticky=E)
        button.bind("<Button-1>", self.sclicked) 
        
        self.newt = ttk.Label(newwin, text='Time:')
        self.newt.grid(row=2+i*6, column=0, sticky=W)
        self.entry_t = StringVar()
        newtentry=ttk.Entry(newwin,textvariable=self.entry_t, justify=RIGHT)
        newtentry.grid(row=2+i*6, column=1, sticky=E)
        button = ttk.Button(newwin, text='Save', command=self.tclicked)
        button.grid(row=3+i*6, column=1, sticky=E)
        button.bind("<Button-1>", self.tclicked) 
        
        self.newi = ttk.Label(newwin, text='Interval:')
        self.newi.grid(row=4+i*6, column=0, sticky=W)
        self.entry_i = StringVar()
        newientry=ttk.Entry(newwin,textvariable=self.entry_i, justify=RIGHT)
        newientry.grid(row=4+i*6, column=1, sticky=E)
        button = ttk.Button(newwin, text='Save', command=self.iclicked)
        button.grid(row=5+i*6, column=1, sticky=E)
        button.bind("<Button-1>", self.iclicked) 


 
Widget()





