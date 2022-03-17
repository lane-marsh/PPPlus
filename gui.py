import tkinter as tk
import pickle
import time
import os
import webbrowser
from ttkwidgets.autocomplete import AutocompleteEntry
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

        # create object for directory of images and logo object
        self.img_dir = os.path.dirname(os.path.realpath(__file__)) + "/Images"
        self.ppp_logo = ImageTk.PhotoImage(Image.open(self.img_dir + "/PPP_Logo.jpg"))
        self.background = ImageTk.PhotoImage(Image.open(self.img_dir + "/background.jpg"))

        # generate features to add to main menu
        self.make_home()

        # holding place for plot objects on home search page
        self.listing_table = None
        self.price_plot = None
        self.analysis_plot = None

        # axis values for plot of house prices over time
        self.house_price = []
        self.interest_rates = []
        self.x_axis = []

        # extract and load data tables
        self.listings = ObjectifyCSV('data/listings.csv')
        self.interest = ObjectifyCSV('data/mortgage.csv')

        self.populate_interest()

        # generate list of unique cities
        self.cities = []
        arb_set = set()
        for key, city in self.listings.data['CITY'].items():
            arb_set.add(city)
        for city in arb_set:
            self.cities.append(city)

        # start the application
        self.window.mainloop()

    def populate_interest(self):
        """
        populate the interest rate data
        """
        for key, item in self.interest.data['Interest Rate'].items():
            self.interest_rates.append(float(item))

    def make_home(self):
        """
        makes elements on the home screen
        """

        background_label = tk.Label(self.window, image=self.background)
        background_label.place(x=0, y=0)

        # generate logo
        logo_panel = tk.Label(self.window, image=self.ppp_logo)
        logo_panel.place(x=0, y=0)
        self.window.iconbitmap(self.img_dir + "/PPP_Logo.ico")

        # generate pane for application description text
        description_pane = tk.Frame(self.window,
                                    bg='white')
        description_pane.place(x=50, y=150)

        about_label_label = tk.Label(description_pane,
                                     text='About PP+',
                                     font=('Arial', 16),
                                     bg='white')
        about_label_label.pack(anchor='w')

        # load about message
        with open('desc_files/about.txt', 'r') as f:
            about_message = str(f.readlines())
        # trim brackets and quotes
        about_message = about_message[2:-2]

        # generate about of application
        about_label = tk.Label(description_pane,
                               text=about_message,
                               font=('Arial', 12),
                               bg='white',
                               anchor='w',
                               wraplength=600)
        about_label.pack(anchor='w')

        blank1 = tk.Label(description_pane, bg='white').pack()

        goal_label_label = tk.Label(description_pane,
                                    text='Goal PP+',
                                    font=('Arial', 16),
                                    bg='white',
                                    pady=10,
                                    anchor='w')
        goal_label_label.pack(anchor='w')

        # load goal message
        with open('desc_files/goal.txt', 'r') as f:
            goal_message = str(f.readlines())
        # trim brackets and quotes
        goal_message = goal_message[2:-2]

        goal_label = tk.Label(description_pane,
                              text=goal_message,
                              font=('Arial', 12),
                              bg='white',
                              anchor='w',
                              wraplength=600)
        goal_label.pack(anchor='w')

        blank2 = tk.Label(description_pane, bg='white').pack()

        inst_label_label = tk.Label(description_pane,
                                    text='Instruction PP+',
                                    font=('Arial', 16),
                                    bg='white',
                                    pady=10,
                                    anchor='w')
        inst_label_label.pack(anchor='w')

        # load instruction message
        with open('desc_files/instruction.txt', 'r') as f:
            inst_message = str(f.readlines())
        # trim brackets and quotes
        inst_message = inst_message[2:-2]

        inst_label = tk.Label(description_pane,
                              text=inst_message,
                              font=('Arial', 12),
                              bg='white',
                              anchor='w',
                              wraplength=600)
        inst_label.pack(anchor='w')

        # generate home search button
        home_butt = tk.Button(self.window, width=70, height=2,
                              text=' Start Searching Homes ',
                              command=lambda: [self.window.withdraw(),
                                               self.open_home_search()])
        home_butt.place(x=100, y=70)

    def open_home_search(self):
        """
        close current screen and open the home search screen
        """
        home_search = tk.Toplevel(self.window)
        home_search.geometry("1000x700+50+50")
        home_search.title("Home Search")

        self.make_home_search(home_search)

    def make_home_search(self, window):
        """
        generate features on the home search page
        """

        # generate logo
        logo_panel = tk.Label(window, image=self.ppp_logo)
        logo_panel.place(x=0, y=0)
        window.iconbitmap(self.img_dir + "\PPP_Logo.ico")
        CreateToolTip(logo_panel, "Property Professionals Plus")

        # generate main label for home search screen
        main_title = tk.Label(window,
                              text='Search Homes',
                              font=('Arial', 36),
                              wraplength=800)
        main_title.place(x=100, y=0)

        # generate return home button
        return_home_butt = tk.Button(window,
                                     text=' Return Home ',
                                     command=lambda: [self.window.deiconify(),
                                                      window.destroy()])
        return_home_butt.place(x=875, y=640)
        CreateToolTip(return_home_butt, "Return to the home page")

        # city filter Label
        city_title = tk.Label(window,
                              text='City:',
                              font=('Arial', 14))
        city_title.place(x=30, y=70)

        # city Filter Entry
        city_filter = AutocompleteEntry(window, completevalues=self.cities)
        city_filter.insert(0, 'Corvallis')
        city_filter.place(x=90, y=75)

        # zip code filter Label
        zip_code_title = tk.Label(window,
                                  text='Zip:',
                                  font=('Arial', 14))
        zip_code_title.place(x=30, y=95)

        # city Filter Entry
        zip_filter = tk.Entry(window)
        zip_filter.place(x=90, y=100)

        # bed filter Label
        bed_title = tk.Label(window,
                             text='Beds:',
                             font=('Arial', 14))
        bed_title.place(x=30, y=120)

        # bed Filter Entry
        bed_filter = tk.Entry(window)
        bed_filter.insert(0, 'any')
        bed_filter.place(x=90, y=125)

        # bath filter Label
        bath_title = tk.Label(window,
                              text='Baths:',
                              font=('Arial', 14))
        bath_title.place(x=30, y=145)

        # bed Filter Entry
        bath_filter = tk.Entry(window)
        bath_filter.insert(0, 'any')
        bath_filter.place(x=90, y=150)

        # generate use filter button
        filter_butt = tk.Button(window,
                                text='   Apply Filters   ',
                                command=lambda: [self.update_listings(str(city_filter.get()),
                                                 window,
                                                 baths=bath_filter.get(),
                                                 beds=bed_filter.get(),
                                                 zip_code=zip_filter.get())])
        filter_butt.place(x=220, y=145)
        CreateToolTip(filter_butt, "Must click to apply filters")

        self.listing_table = ScrollyTable(window,
                                          width=350,
                                          height=485,
                                          loc_x=30,
                                          loc_y=200,
                                          cursor='hand1',
                                          text='blue')

        self.update_listings('Corvallis', window)

        heading = ScrollyTable(window,
                               width=350,
                               height=25,
                               loc_x=30,
                               loc_y=175)
        heading.add_row(['Address', 'Bedrooms', 'Price ($)'])

    def plot_price(self, window):
        # the figure that will contain the plot
        fig = Figure(figsize=(8, 4),
                     dpi=70)

        # adding the subplot
        plot1 = fig.add_subplot(111)
        plot2 = plot1.twinx()

        # plotting the graph
        plot1.plot(self.x_axis, self.house_price, 'b-')
        plot2.plot(self.x_axis, self.interest_rates, 'g-')

        # label plot
        plot1.set_xlabel('Date')
        plot1.set_ylabel('Housing Prices', color='b')
        plot2.set_ylabel('Interest Rates', color='g')

        # creating the Tkinter canvas containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()

        return canvas.get_tk_widget()

    def plot_analysis(self, window):
        # the figure that will contain the plot
        fig = Figure(figsize=(8, 4),
                     dpi=70)

        # adding the subplot
        plot1 = fig.add_subplot(111)
        plot2 = plot1.twinx()

        # generate payment graph
        payments = []
        inflation = []
        base = 0
        for index, price in enumerate(self.house_price):
            if index == 0:
                payments.append(1)
                inflation.append(1)
                base = price + price * self.interest_rates[index] / 100 * 30
            else:
                payments.append((price + price * self.interest_rates[index]/100 * 30) / base)
                inflation.append(inflation[index - 1] * (1 + .026/12))

        # plotting the graph
        plot1.plot(self.x_axis, payments, 'b-')
        plot1.plot(self.x_axis, inflation, 'g-')

        # label plot
        plot1.set_xlabel('Date')
        plot1.set_ylabel('Mortgage Payment Change (Jan 2000 baseline)', color='b')

        # creating the Tkinter canvas containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()

        return canvas.get_tk_widget()

    def update_listings(self, city, window, beds='', baths='', zip_code=''):
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
                                                  ['ADDRESS', 'BEDS', 'PRICE', 'URL', 'BATHS', 'ZIP']):
            row = [listing[0], listing[1], listing[2], listing[3]]
            checker = True
            if beds != '' and beds != 'any' and listing[1] != beds:
                checker = False
            if baths != '' and baths != 'any' and listing[4] != baths:
                checker = False
            if zip_code != '' and listing[5] != zip_code:
                checker = False
            if checker:
                self.listing_table.add_row(row)

        update_instruction('instruction_share_microservice', True)
        plot_data = read_output('output_share_microservice')

        self.house_price = list(map(int, plot_data['price']))
        self.x_axis = []
        for date in plot_data['date']:
            self.x_axis.append(datetime.strptime(date, '%m/%d/%Y'))

        # generate housing prices plot
        self.price_plot = self.plot_price(window)
        self.price_plot.place(x=400, y=70)

        self.analysis_plot = self.plot_analysis(window)
        self.analysis_plot.place(x=400, y=355)

        title_text = city + ' House Prices Over Time'
        # plot title
        plot_title = tk.Label(window,
                              text=title_text,
                              font=('Arial', 16),
                              bg='white')
        plot_title.place(x=545, y=70)

        # plot analysis plot title
        analysis_plot_title = tk.Label(window,
                              text='Average Mortgage Payments',
                              font=('Arial', 16),
                              bg='white')
        analysis_plot_title.place(x=545, y=355)
        CreateToolTip(analysis_plot_title,
                      "Green line represents a 2.54% annual inflation increase\n"
                      "Blue line shows the change in mortgage payments relative to January, 2000\n"
                      "Essentially, if the blue line is below the green line, houses are more affordable than they"
                      "were in January 2000 and vice versa if the blue line is above the green.")


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


class ScrollyTable(object):
    """
    Table object in tkInter
    Generates columns
    """
    def __init__(self, root, width=300, height=500, loc_x=0, loc_y=0, scroller=False, cursor='arrow', text='black'):

        self.main_frame = tk.Frame(root, width=width, height=height+10, bg='white', padx=5, pady=5)
        self.main_frame.place(x=loc_x, y=loc_y)
        self.main_frame.pack_propagate(False)

        self.cursor = cursor
        self.fg = text

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

        obj1 = tk.Label(self.col_1, text=row[0], anchor='w', bg='white', cursor=self.cursor, fg=self.fg)
        obj1.pack()
        obj1.bind("<Button-1>", lambda e: webbrowser.open_new(row[3]))

        obj2 = tk.Label(self.col_2, text=row[1], anchor='w', bg='white', cursor=self.cursor, fg=self.fg)
        obj2.pack()
        obj2.bind("<Button-1>", lambda e: webbrowser.open_new(row[3]))

        obj3 = tk.Label(self.col_3, text=row[2], anchor='w', bg='white', cursor=self.cursor, fg=self.fg)
        obj3.pack()
        obj3.bind("<Button-1>", lambda e: webbrowser.open_new(row[3]))


if __name__ == "__main__":
    PPPApp()
