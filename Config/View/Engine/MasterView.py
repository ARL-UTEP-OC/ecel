from Tkinter import *
from Config.View.Engine import DynamicView


class MakeMasterView:
    def __init__(self, base_dir, config_file_name):
        root = Tk()

        label_plugins = Label(root, text="Engine Settings")

        label_plugins.grid(sticky="W", row=0)

        DynamicView.MakeView(root, base_dir, config_file_name)

        button_close = Button(root, text="Close", command=root.destroy)

        label_plugins.grid(sticky="W", row=0)
        button_close.grid(sticky="W", row=1)

        root.minsize(width=500, height=250)
        root.wm_title("Configure Engine Settings")
        mainloop()
