import tkinter as tk
import FX

class OpenRGB_FXApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.SpectrumCycleBut = tk.Button(self,text='Spectrum Cycling',bg=(87,84,78),command=self.SpectrumCycleFunc())
        #self.SpectrumCycleFunc.pack(side="left")
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
    
    def SpectrumCycleFunc(self):
        FX.CustomSpectrumCycle()

root = tk.Tk()
app = OpenRGB_FXApp(master=root)
app.mainloop()