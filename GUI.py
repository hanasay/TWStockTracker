import tkinter as tk
import plot

def Startup():
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
        print(kwargs)
        plot.Plot_stock(**kwargs)

    ### Initialize GUI
    root = tk.Tk()
    root.title("TW Stock Tracker")

    ### Stock ID Part
    sid_label = tk.Label(root, text="輸入股票代號 *")
    sid_label.pack()
    sid_entry = tk.Entry(root, width=20)
    sid_entry.pack()

    ### Dropdown Part
    selected_option = tk.StringVar(root)
    selected_option.set("技術指標")

    # All supported Indicators
    options = ["MA", "MACD", "KD", "RSI"]
    option_menu = tk.OptionMenu(root, selected_option, *options, command=on_option_select)
    option_menu.pack()

    #selected_option.trace("w", on_option_select)

    ### MA Part
    MA_label = tk.Label(root, text="輸入MA週期 (預設10)") # Input box title
    MA_label.pack_forget()                               # Default Hide This Item
    MA_entry = tk.Entry(root, width=20)                  # Input box
    MA_entry.insert(-1, '10')                            # Default Value
    MA_entry.pack_forget()                               # Default Hide This Item

    MA_Element = ["MA_label", "MA_entry"]                # Enable store list

    ### MACD Part
    MACD_fast_label = tk.Label(root, text="輸入Fast Period (預設12)")
    MACD_fast_label.pack_forget()
    MACD_fast_entry = tk.Entry(root, width=20)
    MACD_fast_entry.insert(-1, '12')
    MACD_fast_entry.pack_forget()

    MACD_slow_label = tk.Label(root, text="輸入Slow Period (預設26)")
    MACD_slow_label.pack_forget()
    MACD_slow_entry = tk.Entry(root, width=20)
    MACD_slow_entry.insert(-1, '26')
    MACD_slow_entry.pack_forget()

    MACD_signal_label = tk.Label(root, text="輸入Signal Period (預設9)")
    MACD_signal_label.pack_forget()
    MACD_signal_entry = tk.Entry(root, width=20)
    MACD_signal_entry.insert(-1, '9')
    MACD_signal_entry.pack_forget()

    MACD = ["MACD_fast_label", "MACD_fast_entry", "MACD_slow_label", "MACD_slow_entry", "MACD_signal_label", "MACD_signal_entry"]

    ### KD Part
    KD_fastk_label = tk.Label(root, text="輸入Fast K Period (預設9)")
    KD_fastk_label.pack_forget()
    KD_fastk_entry = tk.Entry(root, width=20)
    KD_fastk_entry.insert(-1, '9')
    KD_fastk_entry.pack_forget()

    KD_slowk_label = tk.Label(root, text="輸入Slow K Period (預設3)")
    KD_slowk_label.pack_forget()
    KD_slowk_entry = tk.Entry(root, width=20)
    KD_slowk_entry.insert(-1, '3')
    KD_slowk_entry.pack_forget()

    KD_slowd_label = tk.Label(root, text="輸入Slow D Period (預設3)")
    KD_slowd_label.pack_forget()
    KD_slowd_entry = tk.Entry(root, width=20)
    KD_slowd_entry.insert(-1, '3')
    KD_slowd_entry.pack_forget()

    KD = ["KD_fastk_label", "KD_fastk_entry", "KD_slowk_label", "KD_slowk_entry", "KD_slowd_label", "KD_slowd_entry"]

    ### RSI Part
    RSI_label = tk.Label(root, text="輸入RSI週期 (預設14)")
    RSI_label.pack_forget()
    RSI_entry = tk.Entry(root, width=20)
    RSI_entry.insert(-1, '14')
    RSI_entry.pack_forget()

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
        "KD_fastk_label": KD_fastk_label,
        "KD_fastk_entry": KD_fastk_entry,
        "KD_slowk_label": KD_slowk_label,
        "KD_slowk_entry": KD_slowk_entry,
        "KD_slowd_label": KD_slowd_label,
        "KD_slowd_entry": KD_slowd_entry,
        "RSI_label": RSI_label,
        "RSI_entry": RSI_entry
    }

    ### Apply Button
    submit_button = tk.Button(root, text="提交", command=submit)
    submit_button.pack()

    ### Run GUI
    tk.mainloop()