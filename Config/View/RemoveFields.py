class RemoveFields:
    def __init__(self, root):
        for label in root.grid_slaves():
            if int(label.grid_info()["column"]) == 1:
                label.grid_forget()
        for field in root.grid_slaves():
            if int(field.grid_info()["column"]) == 1:
                field.grid_forget()
        for label in root.grid_slaves():
            if int(label.grid_info()["column"]) == 2:
                label.grid_forget()
        for field in root.grid_slaves():
            if int(field.grid_info()["column"]) == 2:
                field.grid_forget()
