import tkinter as tk
import sopg_cli as core


class App:
    class Rule(tk.Frame):
        def __init__(self, parent, on_delete=None, rule_from='', rule_to=''):
            tk.Frame.__init__(self, parent)
            self.on_delete = on_delete
            self.checked = tk.BooleanVar()
            self.checkbox = tk.Checkbutton(self,
                variable=self.checked,
                offvalue=False,
                onvalue=True)
            self.checkbox.select()
            self.entry_from = tk.Entry(self, width=9)
            self.entry_from.insert(0, rule_from)
            self.arrow_point_label = tk.Label(self, text='->', padx=10)
            self.entry_to = tk.Entry(self, width=4)
            self.entry_to.insert(0, rule_to)
            self.remove_button = tk.Button(self, text='X', command=self.delete)

            self.pack()
            self.checkbox.pack(side=tk.LEFT)
            self.entry_from.pack(side=tk.LEFT)
            self.arrow_point_label.pack(side=tk.LEFT)
            self.entry_to.pack(side=tk.LEFT)
            self.remove_button.pack(side=tk.LEFT)

        def delete(self):
            self.destroy()
            if self.on_delete:
                self.on_delete(self)

        def get(self):
            return {rule: self.entry_to.get() for rule in self.entry_from.get().split(',')}

    def remove_rule(self, item):
        self.rule_list.remove(item)

    def add_rule(self, rule_from='', rule_to=''):
        self.rule_list.append(self.Rule(self.rule_frame, self.remove_rule, rule_from, rule_to))

    def result(self) -> dict[str, str]:
        result_dict = {}
        for each in self.rule_list:
            result_dict = {**result_dict, **each.get()} if each.checked else result_dict
        return result_dict
    # End of rule functions

    def to_clipboard(self, root: tk.Tk):
        root.clipboard_clear()
        root.clipboard_append(self.password.get())

    def update_param(self):
        self.password.leetrules = self.result() if self.leetify_var.get() else {}
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
        for label in self.labels:
            label.destroy()
        self.labels = []
        # Button generator for N buttons:
        # Run 1: generate button
        first = True
        # Runs 2 to N: generate divider+button
        # Run N+1: generate 'Regen PW' button
        for i in range(len(self.password.words)):
            # Run 1:
            if first:
                self.buttons.append(tk.Button(
                    self.button_frame,
                    text=self.password.words[0],
                    command=lambda: self.regen_one(0)
                ))
                self.buttons[0].pack(side=tk.LEFT)
                first = False
            # Runs 2 to N:
            else:
                self.labels.append(tk.Label(
                    self.button_frame,
                    text=self.password.divider
                ))
                self.labels[i-1].pack(side=tk.LEFT)
                self.buttons.append(tk.Button(
                    self.button_frame,
                    text=self.password.words[i],
                    command=lambda x = i: self.regen_one(x)
                ))
                self.buttons[i].pack(side=tk.LEFT)
        # Run N+1
        self.buttons.append(tk.Button(
            self.management_frame,
            text="Regen PW",
            command=lambda: self.regen_whole()
        ))
        self.buttons[-1].grid(row=0,column=0)
        # Done

    def __init__(self, root):
        self.password = core.Password()

        #self.header = tk.Frame(root)
        self.header = tk.LabelFrame(root, text="Header")
        self.header.pack(fill=tk.X)

        self.button_frame = tk.LabelFrame(self.header, text="Button frame")
        self.button_frame.pack(fill=tk.X, side=tk.LEFT)
        self.management_frame = tk.LabelFrame(self.header, text="MGMT frame")
        self.management_frame.pack(side=tk.RIGHT)
        self.structure_frame = tk.Frame(root)
        self.structure_frame.pack()

        self.copy_button = tk.Button(
            self.management_frame,
            text="Copy to CB",
            command=lambda: self.to_clipboard(root)
        )
        self.copy_button.grid(row=0,column=1)

        self.leetify_var = tk.BooleanVar()
        self.leetify_box = tk.Checkbutton(
            self.management_frame,
            text='Leetify',
            variable=self.leetify_var,
            offvalue=False,
            onvalue=True
        )
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
        self.divider_field.insert(0, '-')
        self.divider_field.pack()

        self.rule_frame = tk.LabelFrame(root)
        self.rule_frame.pack()
        self.rule_list = []
        self.add_rule('O,o', '0')
        self.add_rule('I,i', '1')
        self.add_rule('B,b', '8')
        self.add_rule('S,s', '$')
        self.add_rule('L,l', '!')

        add_rule_button = tk.Button(root, text="+", width=25, command=self.add_rule)
        add_rule_button.pack()

        self.buttons = []
        self.labels = []
        self.update_buttons()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Secure-Obscure Password Generator")
    app = App(root)
    root.mainloop()
