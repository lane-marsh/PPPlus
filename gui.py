import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dataCrunch import ObjectifyCSV


class PPPApp(object):
    """
    home screen of the Property Professionals Plus Application
    """

    def __init__(self):

        # generate window object and specify size
        self.window = tk.Tk()
        self.window.geometry("1000x700+50+50")
        self.window.title("Main Menu")

        # generate features to add to main menu
        self.make_home()

        # axis values for plot of house prices over time
        self.x_axis = []
        self.x_ticks = []
        self.y_axis = [i ** 2 for i in range(101)]

        self.listings = ObjectifyCSV('data/listings.csv')

        # start the application
        self.window.mainloop()

    def make_home(self):
        """
        makes elements on the home screen
        """

        # generate main label for home screen
        main_title = tk.Label(self.window,
                              text='Property Professionals +',
                              font=('Arial', 36),
                              wraplength=800)
        main_title.place(x=50, y=50)

        # message to the user that is displayed on home screen
        # describes application of the application!
        with open('applicationGoal.txt', 'r') as f:
            desc_message = str(f.readlines())

        # trim brackets and quotes
        desc_message = desc_message[2:-2]

        # generate description of application
        desc_label = tk.Label(self.window,
                              text=desc_message,
                              font=('Arial', 12),
                              wraplength=600)
        desc_label.place(x=150, y=200)

        # generate home search button
        find_home_butt = tk.Button(self.window,
                                   width=50,
                                   height=2,
                                   text=' Find Home ',
                                   command=lambda: [self.window.withdraw(),
                                                    self.open_home_search()])
        find_home_butt.place(x=50, y=150)

        # generate home search button
        find_agent_butt = tk.Button(self.window,
                                   width=50,
                                   height=2,
                                   text=' Find Agent ',
                                   command=lambda: [self.window.withdraw(),
                                                    self.open_agent_search()])
        find_agent_butt.place(x=450, y=150)

    def open_home_search(self):
        """
        close current screen and open the home search screen
        """
        home_search = tk.Toplevel(self.window)
        home_search.geometry("1000x700+50+50")
        home_search.title("Home Search")

        self.make_home_search(home_search)

    def open_agent_search(self):
        """
        close current screen and open the home search screen
        """
        agent_search = tk.Toplevel(self.window)
        agent_search.geometry("1000x700+50+50")
        agent_search.title("Agent Search")

        self.make_agent_search(agent_search)

    def make_home_search(self, window):
        """
        generate features on the home search page
        """

        # generate main label for home search screen
        main_title = tk.Label(window,
                              text='Search Homes',
                              font=('Arial', 36),
                              wraplength=800)
        main_title.place(x=50, y=50)

        # generate plot
        price_plot = self.plot(window)
        price_plot.place(x=400, y=150)

        # plot title
        plot_title = tk.Label(window,
                              text='House Prices Over Time',
                              font=('Arial', 16),
                              bg='white')
        plot_title.place(x=555, y=150)

        # generate return home button
        return_home_butt = tk.Button(window,
                                     text=' Return Home ',
                                     command=lambda: [self.window.deiconify(),
                                                      window.destroy()])
        return_home_butt.place(x=870, y=620)

        table_frame = ScrollyTable(window,
                                   width=350,
                                   height=500,
                                   loc_x=30,
                                   loc_y=150)

        for x in range(30):
            table_frame.add_row([x, "x", "y"])

    def make_agent_search(self, window):
        """
        generate features on the agent search page
        """

        main_title = tk.Label(window,
                              text='Search Agents',
                              font=('Arial', 36),
                              wraplength=800)
        main_title.place(x=50, y=50)

        # generate return home button
        return_home_butt = tk.Button(window,
                                     text=' Return Home ',
                                     command=lambda: [self.window.deiconify(),
                                                      window.destroy()])
        return_home_butt.place(x=870, y=620)

    def plot(self, window):
        # the figure that will contain the plot
        fig = Figure(figsize=(8, 4),
                     dpi=70)

        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.plot(self.y_axis)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()

        return canvas.get_tk_widget()

        # placing the canvas on the Tkinter window
        # canvas.get_tk_widget().place(x=400, y=125)

    def change_plot(self, city):
        """
        search data and alter text criteria
        """


class ScrollyTable(object):
    """
    Table object in tkInter
    Generates columns
    """
    def __init__(self, root, width=300, height=500, loc_x=0, loc_y=0):

        self.main_frame = tk.Frame(root, width=width, height=height+10, bg='white', padx=5, pady=5)
        self.main_frame.place(x=loc_x, y=loc_y)
        self.main_frame.pack_propagate(False)

        self.col_1 = tk.Frame(self.main_frame, width=width/3, height=height, bg='white', padx=1, pady=1)
        self.col_1.pack(side=tk.LEFT)
        self.col_2 = tk.Frame(self.main_frame, width=width/3, height=height, bg='white', padx=1, pady=1)
        self.col_2.pack(side=tk.LEFT)
        self.col_3 = tk.Frame(self.main_frame, width=width/3, height=height, bg='white', padx=1, pady=1)
        self.col_3.pack(side=tk.LEFT)

    def add_row(self, row):
        """
        add item to the table
        """
        obj1 = tk.Label(self.col_1, text=row[0])
        obj1.pack()

        obj2 = tk.Label(self.col_2, text=row[1])
        obj2.pack()

        obj3 = tk.Label(self.col_3, text=row[2])
        obj3.pack()


if __name__ == "__main__":
    PPPApp()
