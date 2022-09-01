import tkinter as tk
import core


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
            self.entry_from = tk.Entry(self, width=17)
            self.entry_from.insert(0, rule_from)
            self.arrow_point_label = tk.Label(self, text='=>', padx=10)
            self.entry_to = tk.Entry(self, width=5)
            self.entry_to.insert(0, rule_to)
            self.remove_button = tk.Button(self, text='X', command=self.delete)

            self.pack()
            self.checkbox.pack(side=tk.LEFT)
            self.entry_from.pack(side=tk.LEFT)
            self.arrow_point_label.pack(side=tk.LEFT)
            self.entry_to.pack(side=tk.LEFT)
            self.remove_button.pack(side=tk.LEFT, padx=(19,0))

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

    def set_case(self, new_case):
        self.password.set_case(new_case)
        self.update_buttons()

    def update_dividers(self):
        self.password.header_flag = self.header_flag.get()
        self.password.divider_flag = self.divider_flag.get()
        self.password.tail_flag = self.tail_flag.get()
        self.password.header = self.header_field.get()
        self.password.divider = self.divider_field.get()
        self.password.tail = self.tail_field.get()
        # .replace part is required for app to recognize the backslashes
        self.password.special_chars = self.special_chars_field.get().replace("\\", "\\\\")
        self.password.update_dividers()
        self.update_buttons()

    def to_clipboard(self, root: tk.Tk):
        root.clipboard_clear()
        root.clipboard_append(self.password.get())

    def update_param(self):
        self.password.leetrules = self.result() if self.leetify_var.get() else {}
        self.password.set_sequence(self.sequence_field.get())
        self.password.divider = self.divider_field.get()

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
        self.labels.append(tk.Label(
            self.button_frame,
            text=self.password.header
        ))
        self.labels[0].pack(side=tk.LEFT)
        # Button generator for N buttons:
        first = True
        for i in range(len(self.password.words)):
            # Run 1: generate button
            if first:
                self.buttons.append(tk.Button(
                    self.button_frame, width=15,
                    text=self.password.words[0],
                    command=lambda: self.regen_one(0)
                ))
                self.buttons[0].pack(side=tk.LEFT)
                first = False
            # Runs 2 to N: generate divider+button
            else:
                self.labels.append(tk.Label(
                    self.button_frame,
                    text=self.password.divider
                ))
                self.labels[i].pack(side=tk.LEFT)
                self.buttons.append(tk.Button(
                    self.button_frame, width=15,
                    text=self.password.words[i],
                    command=lambda x = i: self.regen_one(x)
                ))
                self.buttons[i].pack(side=tk.LEFT)
        self.labels.append(tk.Label(
            self.button_frame,
            text=self.password.tail
        ))
        self.labels[len(self.password.words)].pack(side=tk.LEFT)
        # Run N+1: generate 'Regen PW' button
        self.buttons.append(tk.Button(
            self.management_frame,
            text="Regenerate",
            command=lambda: self.regen_whole()
        ))
        self.buttons[-1].grid(row=0,column=0)
        # Button generation completed

    def __init__(self, root):
        self.password = core.Password()

        self.button_frame = tk.Frame(root, padx=10, pady=10)
        self.button_frame.pack()
        self.management_frame = tk.LabelFrame(root, padx=10)
        self.management_frame.pack(ipadx=3,pady=10)

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

        self.structure_frame = tk.Frame(root)
        self.structure_frame.pack()

        self.sequence_frame = tk.LabelFrame(self.structure_frame, text='Sequence')
        self.sequence_frame.pack(side=tk.LEFT)
        self.sequence_field = tk.Entry(self.sequence_frame, width=29)
        self.sequence_field.insert(0, ' '.join(self.password.sequence))
        self.sequence_field.pack(padx=1)

        # Special symbols in the beginning of the password are strongly recommended
        # Frame for headers, dividers and tails
        self.symbols_frame = tk.Frame(root)
        self.symbols_frame.pack()

        # Header - custom
        self.header_flag = tk.StringVar()
        self.header_flag.set('custom')
        self.header_custom = tk.LabelFrame(self.symbols_frame, text='Header')
        self.header_custom.grid(row=0, column=0)
        self.header_custom_radio = tk.Radiobutton(
            self.header_custom,
            variable=self.header_flag, 
            value='custom', 
            command=self.update_dividers)
        self.header_custom_radio.pack(side=tk.LEFT)
        self.header_field = tk.Entry(self.header_custom, width=7)
        self.header_field.insert(0, '~')
        self.header_field.pack(side=tk.LEFT)
        # Header - random
        self.header_random = tk.Radiobutton(
            self.symbols_frame,
            text="Random",
            variable=self.header_flag, 
            value='random', 
            command=self.update_dividers)
        self.header_random.grid(row=0, column=1, padx=(5,10), pady=(15,0))
        # Special chars field
        self.special_chars = tk.LabelFrame(self.symbols_frame, text='Char pool')
        self.special_chars.grid(row=0, column=2)
        self.special_chars_field = tk.Entry(self.special_chars, width=14)
        self.special_chars_field.insert(0, self.password.special_chars)
        self.special_chars_field.pack()

        # Dividers - custom
        self.divider_flag = tk.StringVar()
        self.divider_flag.set('custom')
        self.divider_custom = tk.LabelFrame(self.symbols_frame, text='Divider')
        self.divider_custom.grid(row=1, column=0)
        self.divider_custom_radio = tk.Radiobutton(
            self.divider_custom,
            variable=self.divider_flag, 
            value='custom', 
            command=self.update_dividers)
        self.divider_custom_radio.pack(side=tk.LEFT)
        self.divider_field = tk.Entry(self.divider_custom, width=7)
        self.divider_field.insert(0, self.password.divider)
        self.divider_field.pack()
        # Dividers - random
        self.divider_random = tk.Radiobutton(
            self.symbols_frame,
            text="Random",
            variable=self.divider_flag, 
            value='random', 
            command=self.update_dividers)
        self.divider_random.grid(row=1, column=1, padx=(5,10), pady=(15,0))
        # Dividers - match header
        self.divider_match = tk.Radiobutton(
            self.symbols_frame,
            text="Match header",
            variable=self.divider_flag, 
            value='match header', 
            command=self.update_dividers)
        self.divider_match.grid(row=1, column=2, padx=(5,10), pady=(15,0))

        # Tail - custom
        self.tail_flag = tk.StringVar()
        self.tail_flag.set('custom')
        self.tail_custom = tk.LabelFrame(self.symbols_frame, text='Tail')
        self.tail_custom.grid(row=2, column=0)
        self.tail_custom_radio = tk.Radiobutton(
            self.tail_custom,
            variable=self.tail_flag, 
            value='custom', 
            command=self.update_dividers)
        self.tail_custom_radio.pack(side=tk.LEFT)
        self.tail_field = tk.Entry(self.tail_custom, width=7)
        self.tail_field.insert(0, '#')
        self.tail_field.pack()
        # Tail - random
        self.tail_random = tk.Radiobutton(
            self.symbols_frame,
            text="Random",
            variable=self.tail_flag, 
            value='random', 
            command=self.update_dividers)
        self.tail_random.grid(row=2, column=1, padx=(5,10), pady=(15,0))
        # Tail - match header
        self.tail_match = tk.Radiobutton(
            self.symbols_frame,
            text="Match header",
            variable=self.tail_flag, 
            value='match header', 
            command=self.update_dividers)
        self.tail_match.grid(row=2, column=2, padx=(5,10), pady=(15,0))

        # Case frame
        self.case_frame = tk.LabelFrame(root)
        self.case_frame.pack(ipadx=10, ipady=10, pady=10)
        self.case_var = tk.StringVar()
        self.case_var.set('capital')
        # Lowercase
        self.radio_lower = tk.Radiobutton(
            self.case_frame,
            text="Lowercase",
            variable=self.case_var,
            value='lower',
            command=lambda: self.set_case('lower'))
        self.radio_lower.pack(side=tk.LEFT)
        # Capitalized
        self.radio_capital = tk.Radiobutton(
            self.case_frame,
            text="Capitalized",
            variable=self.case_var,
            value='capital',
            command=lambda: self.set_case('capital'))
        self.radio_capital.pack(side=tk.LEFT)
        # Uppercase
        self.radio_upper = tk.Radiobutton(
            self.case_frame,
            text="Uppercase",
            variable=self.case_var,
            value='upper',
            command=lambda: self.set_case('upper'))
        self.radio_upper.pack(side=tk.LEFT)


        self.rule_frame = tk.LabelFrame(root)
        self.rule_frame.pack()
        self.rule_list = []
        self.add_rule('O,o', '0')
        self.add_rule('I,i', '1')
        self.add_rule('B,b', '8')
        self.add_rule('S,s', '$')
        self.add_rule('L,l', '!')

        add_rule_button = tk.Button(root, text="+", width=36, command=self.add_rule)
        add_rule_button.pack(pady=(0,10))

        self.buttons = []
        self.labels = []
        # Should be max possible length in pixels:
        # self.password.words = [20*'W' for each in range(4)] # DEBUG
        self.update_buttons()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Secure-Obscure Password Generator")
    app = App(root)
    root.mainloop()
