import geopy.distance as calculator
import json
from Tkinter import *
from PIL import ImageTk, Image

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt


# "constants"
F = 10**-7 #F - CHANGE THE NUMBER TO TERM OF "lat" and "lon"
t_cords = (-35.3632296, 149.1652651) #target cords


def calc_dis(cords1,cords2):
    return calculator.vincenty(cords1, cords2).m

def point_to_cords(point):
    return (point["lat"]*F,point["lon"]*F)

def create_point(t_cords,p):
    return (p["deltaTime"],calc_dis(t_cords,point_to_cords(p)))

def plot_graph():
    with open("landingData.json") as json_file:
        data = json.load(json_file)
        data = [(create_point(t_cords,p)) for p in data]
        time = [time[0] for time in data]
        location = [location[1] for location in data]
        plt.title("Deviation form target over time") 
        plt.xlabel('Time')
        plt.ylabel('Deviation')
        plt.plot(time,location, 'go--', linewidth=0.5, markersize=3.4)
        plt.show()




class Application(Frame):
    def createButton(self):
        self.plot = Button(self)
        self.plot["text"] = "Plot",
        self.plot["command"] = plot_graph
        self.plot.pack({"side": "bottom"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.master.minsize(600, 280)
        self.master.maxsize(600, 280)
        self.master.title("Civdrone  - deviation app")
        self.createButton()

root = Tk()
app = Application(master=root)
img = ImageTk.PhotoImage(Image.open("civdrone.png"))
panel = Label(app, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")

app.mainloop()
root.destroy()