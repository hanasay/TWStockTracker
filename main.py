import plot
import simulator
from tkcalendar import DateEntry

try:
    import tkinter as tk                # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk     # python 2
    import tkFont as tkfont  # python 2

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('400x600')
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, IndicatorsPage, SimulatorPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ### Apply Button
        Indicators_button = tk.Button(self, text="技術指標", command=lambda: controller.show_frame("IndicatorsPage"), height=3,width=15)
        Indicators_button.pack(pady=8)

        ### Apply Button
        simulator_button = tk.Button(self, text="模擬策略", command=lambda: controller.show_frame("SimulatorPage"), height=3,width=15)
        simulator_button.pack(pady=8)


class IndicatorsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="回首頁",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        # Add Calendar
        cal_label = tk.Label(self, text="選擇追蹤日期 *")
        cal_label.pack()
        cal = DateEntry(self, locale='en_US', date_pattern='yyyy/MM/dd')
        cal.pack(pady=10)

        ### Dropdown Event function
        def on_option_select(event):
            selected = selected_option.get()
            # Hide All widget
            for name, widget in widgets.items():
                widget.pack_forget()

            # Show only selected Indicator widget
            for name, widget in widgets.items():
                if name.split('_')[0] == selected:
                    widget.pack()

        ### Submit Button Event
        def submit():
            sid = str(sid_entry.get())
            Indicators_mode = selected_option.get()
            kwargs = {'sid': sid, 'mode': Indicators_mode}
            for name, widget in widgets.items():
                if name.split('_')[0] == selected_option.get() and name.split('_')[-1] == 'entry':
                    kwargs[name[:-6]] = int(widget.get())
            kwargs['date'] = cal.get_date()
            print(kwargs['date'], type(kwargs['date']))
            print(kwargs)
            plot.Plot_stock(**kwargs)

        ### Stock ID Part
        sid_label = tk.Label(self, text="輸入股票代號 *")
        sid_label.pack()
        sid_entry = tk.Entry(self, width=20)
        sid_entry.pack()

        ### Dropdown Part
        selected_option = tk.StringVar(self)
        selected_option.set("技術指標")

        # All supported Indicators
        options = ["MA", "MACD", "KDJ", "RSI"]
        option_menu = tk.OptionMenu(self, selected_option, *options, command=on_option_select)
        option_menu.pack()

        #selected_option.trace("w", on_option_select)

        ### MA Part
        MA_label = tk.Label(self, text="輸入MA週期 (預設10)") # Input box title
        MA_label.pack_forget()                               # Default Hide This Item
        MA_entry = tk.Entry(self, width=20)                  # Input box
        MA_entry.insert(-1, '10')                            # Default Value
        MA_entry.pack_forget()                               # Default Hide This Item

        MA_Element = ["MA_label", "MA_entry"]                # Enable store list

        ### MACD Part
        MACD_fast_label = tk.Label(self, text="輸入Fast Period (預設12)")
        MACD_fast_label.pack_forget()
        MACD_fast_entry = tk.Entry(self, width=20)
        MACD_fast_entry.insert(-1, '12')
        MACD_fast_entry.pack_forget()

        MACD_slow_label = tk.Label(self, text="輸入Slow Period (預設26)")
        MACD_slow_label.pack_forget()
        MACD_slow_entry = tk.Entry(self, width=20)
        MACD_slow_entry.insert(-1, '26')
        MACD_slow_entry.pack_forget()

        MACD_signal_label = tk.Label(self, text="輸入Signal Period (預設9)")
        MACD_signal_label.pack_forget()
        MACD_signal_entry = tk.Entry(self, width=20)
        MACD_signal_entry.insert(-1, '9')
        MACD_signal_entry.pack_forget()

        MACD = ["MACD_fast_label", "MACD_fast_entry", "MACD_slow_label", "MACD_slow_entry", "MACD_signal_label", "MACD_signal_entry"]

        ### KDJ Part
        KDJ_fastk_label = tk.Label(self, text="輸入Period (預設9)")
        KDJ_fastk_label.pack_forget()
        KDJ_fastk_entry = tk.Entry(self, width=20)
        KDJ_fastk_entry.insert(-1, '9')
        KDJ_fastk_entry.pack_forget()

        KDJ_slowk_label = tk.Label(self, text="輸入Slow K Period (預設3) *暫時停用")
        KDJ_slowk_label.pack_forget()
        KDJ_slowk_entry = tk.Entry(self, width=20)
        KDJ_slowk_entry.insert(-1, '3')
        KDJ_slowk_entry.pack_forget()

        KDJ_slowd_label = tk.Label(self, text="輸入Slow D Period (預設3) *暫時停用")
        KDJ_slowd_label.pack_forget()
        KDJ_slowd_entry = tk.Entry(self, width=20)
        KDJ_slowd_entry.insert(-1, '3')
        KDJ_slowd_entry.pack_forget()

        KDJ = ["KDJ_fastk_label", "KDJ_fastk_entry", "KDJ_slowk_label", "KDJ_slowk_entry", "KDJ_slowd_label", "KDJ_slowd_entry"]

        ### RSI Part
        RSI_1_label = tk.Label(self, text="輸入RSI週期1 (預設5)")
        RSI_1_label.pack_forget()
        RSI_1_entry = tk.Entry(self, width=20)
        RSI_1_entry.insert(-1, '5')
        RSI_1_entry.pack_forget()

        RSI_2_label = tk.Label(self, text="輸入RSI週期2 (預設10)")
        RSI_2_label.pack_forget()
        RSI_2_entry = tk.Entry(self, width=20)
        RSI_2_entry.insert(-1, '10')
        RSI_2_entry.pack_forget()

        RSI = ["RSI_label", "RSI_entry"]

        widgets = {
            "MA_label": MA_label,
            "MA_entry": MA_entry,
            "MACD_fast_label": MACD_fast_label,
            "MACD_fast_entry": MACD_fast_entry,
            "MACD_slow_label": MACD_slow_label,
            "MACD_slow_entry": MACD_slow_entry,
            "MACD_signal_label": MACD_signal_label,
            "MACD_signal_entry": MACD_signal_entry,
            "KDJ_fastk_label": KDJ_fastk_label,
            "KDJ_fastk_entry": KDJ_fastk_entry,
            "KDJ_slowk_label": KDJ_slowk_label,
            "KDJ_slowk_entry": KDJ_slowk_entry,
            "KDJ_slowd_label": KDJ_slowd_label,
            "KDJ_slowd_entry": KDJ_slowd_entry,
            "RSI_1_label": RSI_1_label,
            "RSI_1_entry": RSI_1_entry,
            "RSI_2_label": RSI_2_label,
            "RSI_2_entry": RSI_2_entry
        }

        ### Apply Button
        submit_button = tk.Button(self, text="提交", command=submit)
        submit_button.pack()


class SimulatorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        def submit():
            kwargs = {'sid': str(sid_entry.get()),'date': cal.get_date(), 'fund': str(fund_entry.get())}
            simulator.setup(**kwargs)

        button = tk.Button(self, text="回首頁",
                        command=lambda: controller.show_frame("StartPage"))
        button.pack()
        
        # Add Calendar
        cal_label = tk.Label(self, text="選擇追蹤日期 *")
        cal_label.pack()
        cal = DateEntry(self, locale='en_US', date_pattern='yyyy/MM/dd')
        cal.pack(pady=10)

        ### Stock ID Part
        sid_label = tk.Label(self, text="輸入股票代號 *")
        sid_label.pack()
        sid_entry = tk.Entry(self, width=20)
        sid_entry.pack()

        ### Startup foundation Part
        fund_label = tk.Label(self, text="輸入模擬初始資金 (單位 新台幣) *")
        fund_label.pack()
        fund_entry = tk.Entry(self, width=20)
        fund_entry.pack()

        ### Apply Button
        submit_button = tk.Button(self, text="提交", command=submit)
        submit_button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()