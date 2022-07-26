import tkinter as tk
import sopg_cli as core


class App:
    def to_clipboard(self, root: tk.Tk):
        root.clipboard_clear()
        root.clipboard_append(self.password.get())

    def update_param(self):
        self.password.leetrules = self.leetrules if self.leetify_var.get() else {}
        self.password.set_sequence(self.sequence_field.get())
        self.password.set_divider(self.divider_field.get())

    def regen_one(self, number: int):
        self.update_param()
        self.password.regen_one(number)
        self.update_buttons()

    def regen_whole(self):
        self.update_param()
        self.password.regen_whole()
        self.update_buttons()

    def update_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        for i in range(len(self.password.words)):
            self.buttons.append(tk.Button(self.button_frame, text=self.password.words[i], command=lambda x = i: self.regen_one(x)))
            self.buttons[i].pack(side=tk.LEFT)
        self.buttons.append(tk.Button(self.management_frame, text="Regen PW", command=lambda: self.regen_whole()))
        self.buttons[-1].grid(row=0,column=0)

    def __init__(self, root):
        self.password = core.Password()
        self.leetrules = {
                'O': '0',
                'o': '0',
                'I': '1',
                'i': '1',
                'B': '8',
                'b': '8',
                'S': '$',
                's': '$',
                'L': '!',
                'l': '!'
        }

        self.header = tk.LabelFrame(root, text="Header")
        self.header.pack(fill=tk.X)

        self.button_frame = tk.LabelFrame(self.header, text="Button frame")
        self.button_frame.pack(fill=tk.X, side=tk.LEFT)
        self.management_frame = tk.LabelFrame(self.header, text="MGMT frame")
        self.management_frame.pack(side=tk.RIGHT)
        self.structure_frame = tk.Frame(root)
        self.structure_frame.pack()

        self.copy_button = tk.Button(self.management_frame, text="Copy to CB", command=lambda: self.to_clipboard(root))
        self.copy_button.grid(row=0,column=1)

        self.leetify_var = tk.BooleanVar()
        self.leetify_box = tk.Checkbutton(self.management_frame, text='Leetify', variable=self.leetify_var, offvalue=False, onvalue=True)
        self.leetify_box.grid(row=0,column=2)
        self.leetify_box.select()

        self.sequence_frame = tk.LabelFrame(self.structure_frame, text='Sequence')
        self.sequence_frame.pack(side=tk.LEFT)
        self.sequence_field = tk.Entry(self.sequence_frame, width=100)
        self.sequence_field.insert(0, 'adj,nou,ver,adv')
        self.sequence_field.pack()
        self.divider_frame = tk.LabelFrame(self.structure_frame, text='Divider')
        self.divider_frame.pack(side=tk.LEFT)
        self.divider_field = tk.Entry(self.divider_frame, width=15)
        self.divider_field.insert(0, '/')
        self.divider_field.pack()

        self.buttons = []
        self.update_buttons()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Secure-Obscure Password Generator")
    app = App(root)
    root.mainloop()
