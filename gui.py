import tkinter as tk
import pickle
import time
import os
from PIL import ImageTk, Image
from datetime import datetime
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

        # create object for directory of images
        self.img_dir = os.path.dirname(os.path.realpath(__file__)) + "\Images"
        self.ppp_logo = ImageTk.PhotoImage(Image.open(self.img_dir + "\PPP_Logo.jpg"))

        # generate features to add to main menu
        self.make_home()

        # holding place for plot objects on home search page
        self.listing_table = None
        self.price_plot = None

        # axis values for plot of house prices over time
        self.y_axis = []
        self.x_axis = []

        # extract and load data tables
        self.listings = ObjectifyCSV('data/listings.csv')

        # start the application
        self.window.mainloop()

    def make_home(self):
        """
        makes elements on the home screen
        """

        # generate logo
        logo_panel = tk.Label(self.window, image=self.ppp_logo)
        logo_panel.place(x=0, y=0)

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
        interest_butt = tk.Button(self.window,
                                   width=50,
                                   height=2,
                                   text=' Interest Rate Analysis ',
                                   command=lambda: [self.window.withdraw(),
                                                    self.open_interest_rates()])
        interest_butt.place(x=450, y=150)


    def open_home_search(self):
        """
        close current screen and open the home search screen
        """
        home_search = tk.Toplevel(self.window)
        home_search.geometry("1000x700+50+50")
        home_search.title("Home Search")

        self.make_home_search(home_search)

    def open_interest_rates(self):
        """
        close current screen and open the home search screen
        """
        agent_search = tk.Toplevel(self.window)
        agent_search.geometry("1000x700+50+50")
        agent_search.title("Interest Rate History")

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

        # generate return home button
        return_home_butt = tk.Button(window,
                                     text=' Return Home ',
                                     command=lambda: [self.window.deiconify(),
                                                      window.destroy()])
        return_home_butt.place(x=870, y=620)

        # city Search Label
        plot_title = tk.Label(window,
                              text='City:',
                              font=('Arial', 16))
        plot_title.place(x=30, y=120)

        # city Filter Entry
        city_filter = tk.Entry(window)
        city_filter.place(x=90, y=125)

        # generate use filter button
        filter_butt = tk.Button(window,
                                     text=' Search ',
                                     command=lambda: [self.update_listings(str(city_filter.get()), window)])
        filter_butt.place(x=180, y=120)

        self.listing_table = ScrollyTable(window,
                                          width=350,
                                          height=10000,
                                          loc_x=30,
                                          loc_y=175)

        self.update_listings('Seattle', window)

        heading = ScrollyTable(window,
                               width=350,
                               height=25,
                               loc_x=30,
                               loc_y=150)
        heading.add_row(['Address', 'Bedrooms', 'Price ($)'])

    def make_agent_search(self, window):
        """
        generate features on the agent search page
        """

        main_title = tk.Label(window,
                              text='Mortgage Interest Rates',
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
        plot1.plot(self.x_axis, self.y_axis)

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()

        return canvas.get_tk_widget()

    def update_listings(self, city, window):
        """
        search data and alter text criteria
        """

        def update_instruction(filename, status):
            """
            update the instruction file for the microservice
            inputs:
                filename:   name of file that microservice reads from
                status:     boolean argument. True if making request, False if confirming output file has been read
            """
            instr_fd = open(filename, 'wb')
            instr_dict = {'get_data': status, 'city_name': city}
            pickle.dump(instr_dict, instr_fd)
            instr_fd.close()
            return instr_dict

        def read_output(filename):
            """
            read the output from the microservice
            """
            time.sleep(1)
            instr_fd = open(filename, 'rb+')
            instr_dict = pickle.load(instr_fd)
            instr_fd.close()
            return instr_dict

        self.listing_table.clear_table()
        for listing in self.listings.get_by_field({'CITY': city},
                                                  ['ADDRESS', 'BEDS', 'PRICE']):
            self.listing_table.add_row(listing)

        update_instruction('instruction_share_microservice', True)
        plot_data = read_output('output_share_microservice')

        self.y_axis = list(map(int, plot_data['price']))
        self.x_axis = []
        for date in plot_data['date']:
            self.x_axis.append(datetime.strptime(date, '%m/%d/%Y'))

        # generate plot
        self.price_plot = self.plot(window)
        self.price_plot.place(x=400, y=150)

        # plot title
        plot_title = tk.Label(window,
                              text='House Prices Over Time',
                              font=('Arial', 16),
                              bg='white')
        plot_title.place(x=555, y=150)


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
        self.col_1.pack_propagate(False)
        self.col_2 = tk.Frame(self.main_frame, width=width/3, height=height, bg='white', padx=1, pady=1)
        self.col_2.pack(side=tk.LEFT)
        self.col_2.pack_propagate(False)
        self.col_3 = tk.Frame(self.main_frame, width=width/3, height=height, bg='white', padx=1, pady=1)
        self.col_3.pack(side=tk.LEFT)
        self.col_3.pack_propagate(False)

    def clear_table(self):
        """
        clear contents of the table
        """

        for widget in self.col_1.winfo_children():
            widget.destroy()
        for widget in self.col_2.winfo_children():
            widget.destroy()
        for widget in self.col_3.winfo_children():
            widget.destroy()

    def add_row(self, row):
        """
        add item to the table
        """

        obj1 = tk.Label(self.col_1, text=row[0], anchor='w', bg='white')
        obj1.pack()

        obj2 = tk.Label(self.col_2, text=row[1], anchor='w', bg='white')
        obj2.pack()

        obj3 = tk.Label(self.col_3, text=row[2], anchor='w', bg='white')
        obj3.pack()


if __name__ == "__main__":
    PPPApp()
