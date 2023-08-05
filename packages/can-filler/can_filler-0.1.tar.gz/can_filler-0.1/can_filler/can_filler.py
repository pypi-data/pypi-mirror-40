#
# Serial COM Port terminal program
# 8/17/2017, Dale Gambill
# I wrote 2 modules for this program: terminal.py and serial_rx_tx.py.
#
import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext
from tkinter import *
from tkinter import filedialog
import serial_rx_tx
import _thread
import time
import webbrowser
from tkinter import messagebox

# globals
serialPort = serial_rx_tx.SerialPort()
logFile = None

root = tk.Tk() # create a Tk root window
root.title( "Moore Specialty Brewing Can Filler" )
# set up the window size and position
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width/2
window_height = screen_width/3
window_position_x = screen_width/2 - window_width/2
window_position_y = screen_height/2 - window_height/2
root.geometry('%dx%d+%d+%d' % (window_width, window_height, window_position_x, window_position_y))

# scrolled text box used to display the serial data
frame = tk.Frame(root, bg='cyan')
frame.pack(side="bottom", fill='both', expand='no')
textbox = tkscrolledtext.ScrolledText(master=frame, wrap='word', width=180, height=25) #width=characters, height=lines
textbox.pack(side='bottom', fill='y', expand=True, padx=0, pady=0)
textbox.config(font="bold")

#COM Port label
label_comport = Label(root,width=10,height=2,text="COM Port:")
label_comport.place(x=10,y=26)
label_comport.config(font="bold")

#COM Port entry box
comport_edit = Entry(root,width=10)
comport_edit.place(x=100,y=36)
comport_edit.config(font="bold")
comport_edit.insert(END,"COM4")

# serial data callback function
def OnReceiveSerialData(message):
    str_message = message.decode("utf-8")
    textbox.insert('1.0', str_message)

# Register the callback above with the serial port object
serialPort.RegisterReceiveCallback(OnReceiveSerialData)

def sdterm_main():
    root.after(200, sdterm_main)  # run the main loop once each 200 ms

#
#  commands associated with button presses
#
def OpenCommand():
    if button_openclose.cget("text") == 'Open COM Port':
        comport = comport_edit.get()
        baudrate = baudrate_edit.get()
        serialPort.Open(comport,baudrate)
        button_openclose.config(text='Close COM Port')
        textbox.insert('1.0', "COM Port Opened\r\n")
    elif button_openclose.cget("text") == 'Close COM Port':
        if button_replaylog.cget('text') == 'Stop Replay Log':
            textbox.insert('1.0',"Stop Log Replay first\r\n")
        else:
            serialPort.Close()
            button_openclose.config(text='Open COM Port')
            textbox.insert('1.0',"COM Port Closed\r\n")


def ClearDataCommand():
    textbox.delete('1.0',END)

def SendDataCommand():
    message = senddata_edit.get()
    if serialPort.IsOpen():
        message += '\r\n'
        serialPort.Send(message)
        textbox.insert('1.0',message)
    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")

def ReplayLogFile():
    try:
      if logFile != None:
        readline = logFile.readline()
        global serialPort
        serialPort.Send(readline)
    except:
      print("Exception in ReplayLogFile()")

def ReplayLogThread():
    while True:
        time.sleep(1.0)
        global logFile
        if serialPort.IsOpen():
            if logFile != None:
                ReplayLogFile()

def Lower_Head():
    
    lower = "G20 G91 Z-2"
    if serialPort.IsOpen():
        lower += '\r\n'
        serialPort.Send(lower)
        textbox.insert('1.0',lower)
    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")

def PurgeFill():
    purge = "M08"
    stop_purge = "M09"
    fill = "M4"
    stop_fill = "M5"
    if serialPort.IsOpen():
        purge += '\r\n'
        serialPort.Send(purge)
        textbox.insert('1.0',purge)
        time.sleep(5)
        stop_purge += '\r\n'
        serialPort.Send(stop_purge)
        textbox.insert('1.0',stop_purge)
        fill += '\r\n'
        serialPort.Send(fill)
        textbox.insert('1.0',fill)
    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")

def Raise_Head():
    #comport = comport_edit.get()
    #baudrate = baudrate_edit.get()
    #serialPort.Close()#After Hard Limit from full can
    #time.sleep(1)
    #serialPort.Open(comport,baudrate)#ReOpen and proceed
    #time.sleep(2)
    resume = "~"
    close = "M5"
    raise_ = "G20 G91 Z2"
    if serialPort.IsOpen():
        resume += '\r\n'
        serialPort.Send(resume)
        textbox.insert('1.0',resume)
        close += '\r\n'
        serialPort.Send(close)
        textbox.insert('1.0',close)
        raise_ += '\r\n'
        serialPort.Send(raise_)
        textbox.insert('1.0',raise_)
    else:
        textbox.insert('1.0', "Not sent - COM port is closed\r\n")

# COM Port open/close button
button_openclose = Button(root,text="Open COM Port",width=20,command=OpenCommand)
button_openclose.config(font="bold")
button_openclose.place(x=210,y=30)

#Clear Rx Data button
button_cleardata = Button(root,text="Clear Rx Data",width=20,command=ClearDataCommand)
button_cleardata.config(font="bold")
button_cleardata.place(x=210,y=72)

#Send Message button
button_senddata = Button(root,text="Manual Command",width=20,command=SendDataCommand)
button_senddata.config(font="bold")
button_senddata.place(x=620,y=30)

#Lower button
button_replaylog = Button(root,text="Lower",width=16,command=Lower_Head)
button_replaylog.config(font="bold")
button_replaylog.place(x=433,y=30)

#Purge/Fill button
button_about = Button(root,text="Purge/Fill",width=16,command=PurgeFill)
button_about.config(font="bold")
button_about.place(x=433,y=72)

#Raise Button
button_tutorials = Button(root,text="Raise",width=16,command=Raise_Head)
button_tutorials.config(font="bold")
button_tutorials.place(x=433,y=110)

#
# data entry labels and entry boxes
#

#Send Data entry box
senddata_edit = Entry(root,width=34)
senddata_edit.place(x=620,y=78)
senddata_edit.config(font="bold")
senddata_edit.insert(END,"Command")

#Baud Rate label
label_baud = Label(root,width=10,height=2,text="Baud Rate:")
label_baud.place(x=10,y=70)
label_baud.config(font="bold")

#Baud Rate entry box
baudrate_edit = Entry(root,width=10)
baudrate_edit.place(x=100,y=80)
baudrate_edit.config(font="bold")
baudrate_edit.insert(END,"115200")

#
# The main loop
#
root.after(200, sdterm_main)
root.mainloop()
#


