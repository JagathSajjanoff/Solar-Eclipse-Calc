from curses import window
import ephem
from datetime import datetime, timedelta
from PIL import *
from PIL import Image,ImageTk
import tkinter as tk

class Application(tk.Frame):    
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.name = "Solar Eclipse" 
        self.age = None
        self.results = []

    def create_widgets(self):
        self.label1 = tk.Label(self, text="Enter Start Year:", fg="black", font=("Robotica", 14))
        self.label1.pack(side="left")
        self.entry1 = tk.Entry(self)
        self.entry1.pack(side="left")
        self.label2 = tk.Label(self, text="Enter End Year:", fg="black", font=("Robotica", 14))
        self.label2.pack(side="left")
        self.entry2 = tk.Entry(self)
        self.entry2.pack(side="left")
        self.button = tk.Button(self, text="Submit", fg="red", command=self.submit)
        self.button.pack(side="left")
        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

    def submit(self):
        if self.name is None or self.age is None:
            self.name = self.entry1.get()
            self.age = self.entry2.get()
            print("Received The Info")
            self.compute_eclipse_times()
            self.button.config(state="disabled")
        else:
            print("Calculation Done, The Result Is Displayed.")

    def compute_eclipse_times(self):
        curtime = datetime(int(self.name), 1, 1, 0, 0, 0)
        endtime = datetime(int(self.age), 12, 31, 23, 59, 59)
        moon = ephem.Moon()
        sun = ephem.Sun()
        observer = ephem.Observer()
        observer.elevation = -6371000
        observer.pressure = 0

        self.results.clear()  # Clear the previous results
        self.result_label.config(text="Calculating... Please wait.")

        def calculate_eclipses():
            nonlocal curtime
            if curtime <= endtime:
                observer.date = curtime.strftime('%Y/%m/%d %H:%M:%S')
                moon.compute(observer)
                sun.compute(observer)
                sep = abs((float(ephem.separation(moon, sun)) / 0.01745329252))
                if sep < 1.59754941:  # Adjust this threshold as needed
                    print(curtime.strftime('%Y/%m/%d %H:%M:%S'))
                    date_str = curtime.strftime('%Y/%m/%d')
                    print(date_str)
                    if not (date_str in '\n'.join(self.results)):
                        result_str = curtime.strftime('%Y/%m/%d %H:%M:%S') + " " + str(sep)
                        self.results.append(result_str)
                curtime += timedelta(minutes=60)
                self.master.after(1, calculate_eclipses)
            else:
                self.button.config(state="normal")
                self.result_label.config(text="Calculation completed.")
                self.result_label.config(text='\n'.join( self.results), font=("Helvetica", 14))  # Display all results in the label
        calculate_eclipses()



root = tk.Tk()

root.config(cursor="shuttle")
root.geometry("1200x500")
imgB3=Image.open("m.png")
resize_img=imgB3.resize((1270,710))
img_B3=ImageTk.PhotoImage(resize_img)
ImgLabel=tk.Label(root,image=img_B3)
ImgLabel.img3=img_B3
ImgLabel.place(x=0, y=0)
app = Application(master=root)
app.mainloop()
