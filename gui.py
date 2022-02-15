import tkinter as tk
from PIL import ImageTk, Image
import os


class PPPApp(object):
    """
    home screen of the Property Professionals Plus Application
    """

    def __init__(self):

        # generate window object and specify size
        self.window = tk.Tk()
        self.window.geometry("1000x700+50+50")
        self.window.title("Main Menu")

        # generate button
        self.find_home_butt = tk.Button(self.window,
                                        text=' Find Home ',
                                        command=lambda: [self.window.withdraw(), self.open_home_search()])
        self.find_home_butt.place(x=50, y=50)

        self.window.mainloop()

    def open_home_search(self):
        """
        close current screen and open the home search screen
        """
        home_search = tk.Toplevel(self.window)
        home_search.geometry("1000x700+50+50")
        home_search.title("Home Search")

        return_home_butt = tk.Button(home_search,
                                     text=' Return Home ',
                                     command=lambda: [self.window.deiconify(), home_search.destroy()])
        return_home_butt.place(x=60, y=60)


if __name__ == "__main__":
    PPPApp()
