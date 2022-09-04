import tkinter as tk
import core
import json


class App:
    class Rule(core.Password.Rule, tk.Frame):
        def __init__(self, parent, on_delete=None, rule_from='', rule_to=''):
            """`Rule` is a special frame that have two entry fields, values in
            first are replaced with values in second. 
            
            Possible BUG: Checkbox is there to temporarily disable a rule but
            it seems like it's not working.
            
            For some reason Debian's graphical toolkit libraries don't show 
            whether a checkbox/radio is toggled, so I can't test it rn. 
            
            Is used in result() function of parent class
            """
            # Defining
            core.Password.Rule.__init__(self, rule_from, rule_to)
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
            # Packing
            self.pack()
            self.checkbox.pack(side=tk.LEFT)
            self.entry_from.pack(side=tk.LEFT)
            self.arrow_point_label.pack(side=tk.LEFT)
            self.entry_to.pack(side=tk.LEFT)
            self.remove_button.pack(side=tk.LEFT, padx=(19,0))

        def delete(self):
            """To delete a frame two actions are required:
            1) Destroying widget in TKinter, so it won't be drawn
            2) Removing element from list it's stored in, so it won't be applied
            
            To achieve this, the second function - remove_rule() - is written
            in parent App class and passed in add_rule() and then to __init__()
            when a new Rule is instantiated. 

            Explanation w/ examples: stackoverflow.com/questions/72852388/
            """
            self.destroy()
            if self.on_delete:
                self.on_delete(self)

        def get(self):
            """Returns the rule as dict. Keys will be replaced with values.
            
            Example: | A,b,c | => | x | will return {A: x, b: x, c: x}
            """
            return {rule: self.entry_to.get() for rule in self.entry_from.get().split(',')}
    # End of Rule 


    def remove_rule(self, item):
        """Removes the rule from the list it's stored in
        """
        self.password.rule_list.remove(item)

    def add_rule(self, rule_from='', rule_to=''):
        """Instantiates a rule and puts it in the list
        """
        self.password.rule_list.append(self.Rule(
            self.rule_frame, 
            self.remove_rule, 
            rule_from, 
            rule_to
        ))
 
    def result(self) -> dict[str, str]:
        """Iterates through all replacement rules and combines them to a single
        dictionary. Uses `Rule`'s .get() method.
        """
        result_dict = {}
        for each in self.password.rule_list:
            result_dict = {**result_dict, **each.get()} if each.checked else result_dict
        return result_dict
    # End of Rule functions

    def set_case(self, new_case):
        """Changes password's case w/o regenerating anything else
        """
        self.password.set_case(new_case)
        self.update_buttons()

    def to_clipboard(self, root: tk.Tk):
        """Copies the password to clipboard
        """
        root.clipboard_clear()
        root.clipboard_append(self.password.get())

    def update_config(self):
        """Updates header, dividers and tails w/o regenerating anything else
        
        Feeds new configuration to the child password object
        """
        self.password.config['header_flag'] = self.header_flag.get()
        self.password.config['divider_flag'] = self.divider_flag.get()
        self.password.config['tail_flag'] = self.tail_flag.get()
        self.password.config['header'] = self.header_field.get()
        self.password.config['divider'] = self.divider_field.get()
        self.password.config['tail'] = self.tail_field.get()
        # .replace part is required to recognize the backslashes
        self.password.config['special_chars'] = self.special_chars_field.get()#.replace("\\", "\\\\")
        self.password.update_dividers()
        # self.password.config['rules_init'] = {each.rule_from: each.rule_to for each in self.password.rule_list}
        self.password.set_sequence(self.sequence_field.get())
        # update_buttons() is called twice in regen, shouldn't be a problem,
        # but better solution should be considered
        self.password.config['rules_init'] = {}
        for each in self.password.rule_list:
            if each.entry_from.get():
                self.password.config['rules_init'].update({
                    each.entry_from.get(): each.entry_to.get()
                })
        self.update_buttons()

    def regen_one(self, number: int):
        self.update_config()
        self.password.regen_one(number)
        self.update_buttons()

    def regen_whole(self):
        self.update_config()
        self.password.regen_whole()
        self.update_buttons()

    def use_passphrase(self):
        self.update_config()
        self.password.use_passphrase(self.passphrase_field.get())
        self.update_buttons()

    def update_buttons(self):
        """Quick breakdown:

        clear the frame
        place header
        place first word button
        cycle:
            place divider
            place word button
        place tail

        """
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        for label in self.labels:
            label.destroy()
        self.labels = []
        self.labels.append(tk.Label(
            self.button_frame,
            text=self.password.config['header']
        ))
        self.labels[0].pack(side=tk.LEFT)
        # Button generator for N buttons:
        first = True
        for i in range(len(self.password.words)):
            # Run 1: generate button
            if first:
                self.buttons.append(tk.Button(
                    self.button_frame, # width=15, # Fixed width
                    text=self.password.words[0],
                    command=lambda: self.regen_one(0)
                ))
                self.buttons[0].pack(side=tk.LEFT)
                first = False
            # Runs 2 to N: generate divider+button
            else:
                self.labels.append(tk.Label(
                    self.button_frame,
                    text=self.password.config['divider']
                ))
                self.labels[i].pack(side=tk.LEFT)
                self.buttons.append(tk.Button(
                    self.button_frame, # width=15, # Fixed width
                    text=self.password.words[i],
                    command=lambda x = i: self.regen_one(x)
                ))
                self.buttons[i].pack(side=tk.LEFT)
        self.labels.append(tk.Label(
            self.button_frame,
            text=self.password.config['tail']
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

    def save_config(self):
        self.update_config()
        with open("config.json", "w") as f:
            json.dump(self.password.config, f, indent=4)
        
    def __init__(self, root):
        self.password = core.Password()

        # PASSPHRASE FRAME
        self.passphrase_frame = tk.LabelFrame(root, text='Custom passphrase')
        self.passphrase_frame.pack(pady=10)
        self.passphrase_field = tk.Entry(self.passphrase_frame, width=35)
        self.passphrase_field.insert(0, self.password.config['passphrase'])
        self.passphrase_field.pack(padx=1, side=tk.LEFT)
        self.passphrase_button = tk.Button(
            self.passphrase_frame,
            text='Use',
            command=self.use_passphrase
        )
        self.passphrase_button.pack(side=tk.LEFT)

        self.button_frame = tk.Frame(root, padx=10, pady=10)
        self.button_frame.pack()

        # MGMT FRAME
        self.management_frame = tk.LabelFrame(root, padx=10)
        self.management_frame.pack(ipadx=3,pady=10)
        # Copy button
        self.copy_button = tk.Button(
            self.management_frame,
            text="Copy to CB",
            command=lambda: self.to_clipboard(root)
        )
        self.copy_button.grid(row=0,column=1)
        # Leetify checkbox
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

        # STRUCTURE FRAME
        self.structure_frame = tk.Frame(root)
        self.structure_frame.pack()
        # SEQUENCE FRAME, inside structure, currently only holds one field
        self.sequence_frame = tk.LabelFrame(
            self.structure_frame, 
            text='Generation from sequence'
        )
        self.sequence_frame.pack()
        self.sequence_field = tk.Entry(self.sequence_frame, width=35)
        self.sequence_field.insert(0, ''.join(self.password.config['sequence']))
        self.sequence_field.pack(padx=1, side=tk.LEFT)

        # SYMBOLS TABLE-FRAME:
        # Header:    | Custom (radio, entry) | Random (radio) | Chars (entry) |
        # Dividers:  | Custom (radio, entry) | Random (radio) | Match (radio) |
        # Tail:      | Custom (radio, entry) | Random (radio) | Match (radio) |
        self.symbols_frame = tk.Frame(root)
        self.symbols_frame.pack()
        # Header - Custom
        self.header_flag = tk.StringVar()
        self.header_flag.set('custom')
        self.header_custom = tk.LabelFrame(self.symbols_frame, text='Header')
        self.header_custom.grid(row=0, column=0)
        self.header_custom_radio = tk.Radiobutton(
            self.header_custom,
            variable=self.header_flag, 
            value='custom', 
            command=self.update_config
        )
        self.header_custom_radio.pack(side=tk.LEFT)
        self.header_field = tk.Entry(self.header_custom, width=7)
        self.header_field.insert(0, self.password.config['header'])
        self.header_field.pack(side=tk.LEFT)
        # Header - Random
        self.header_random = tk.Radiobutton(
            self.symbols_frame,
            text="Random",
            variable=self.header_flag, 
            value='random', 
            command=self.update_config
        )
        self.header_random.grid(row=0, column=1, padx=(5,10), pady=(15,0))
        # Chars
        self.special_chars = tk.LabelFrame(
            self.symbols_frame,
            text='Char pool'
        )
        self.special_chars.grid(row=0, column=2)
        self.special_chars_field = tk.Entry(self.special_chars, width=14)
        self.special_chars_field.insert(0, self.password.config['special_chars'])
        self.special_chars_field.pack()

        # Dividers - Custom
        self.divider_flag = tk.StringVar()
        self.divider_flag.set('custom')
        self.divider_custom = tk.LabelFrame(self.symbols_frame, text='Divider')
        self.divider_custom.grid(row=1, column=0)
        self.divider_custom_radio = tk.Radiobutton(
            self.divider_custom,
            variable=self.divider_flag, 
            value='custom', 
            command=self.update_config
        )
        self.divider_custom_radio.pack(side=tk.LEFT)
        self.divider_field = tk.Entry(self.divider_custom, width=7)
        self.divider_field.insert(0, self.password.config['divider'])
        self.divider_field.pack()
        # Dividers - Random
        self.divider_random = tk.Radiobutton(
            self.symbols_frame,
            text="Random",
            variable=self.divider_flag, 
            value='random', 
            command=self.update_config
        )
        self.divider_random.grid(row=1, column=1, padx=(5,10), pady=(15,0))
        # Dividers - Match header
        self.divider_match = tk.Radiobutton(
            self.symbols_frame,
            text="Match header",
            variable=self.divider_flag, 
            value='match header', 
            command=self.update_config
        )
        self.divider_match.grid(row=1, column=2, padx=(5,10), pady=(15,0))

        # Tail - Custom
        self.tail_flag = tk.StringVar()
        self.tail_flag.set('custom')
        self.tail_custom = tk.LabelFrame(self.symbols_frame, text='Tail')
        self.tail_custom.grid(row=2, column=0)
        self.tail_custom_radio = tk.Radiobutton(
            self.tail_custom,
            variable=self.tail_flag, 
            value='custom', 
            command=self.update_config
        )
        self.tail_custom_radio.pack(side=tk.LEFT)
        self.tail_field = tk.Entry(self.tail_custom, width=7)
        self.tail_field.insert(0, self.password.config['tail'])
        self.tail_field.pack()
        # Tail - Random
        self.tail_random = tk.Radiobutton(
            self.symbols_frame,
            text="Random",
            variable=self.tail_flag, 
            value='random', 
            command=self.update_config
        )
        self.tail_random.grid(row=2, column=1, padx=(5,10), pady=(15,0))
        # Tail - Match header
        self.tail_match = tk.Radiobutton(
            self.symbols_frame,
            text="Match header",
            variable=self.tail_flag, 
            value='match header', 
            command=self.update_config
        )
        self.tail_match.grid(row=2, column=2, padx=(5,10), pady=(15,0))

        # CASE FRAME
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
            command=lambda: self.set_case('lower')
        )
        self.radio_lower.pack(side=tk.LEFT)
        # Capitalized
        self.radio_capital = tk.Radiobutton(
            self.case_frame,
            text="Capitalized",
            variable=self.case_var,
            value='capital',
            command=lambda: self.set_case('capital')
        )
        self.radio_capital.pack(side=tk.LEFT)
        # Uppercase
        self.radio_upper = tk.Radiobutton(
            self.case_frame,
            text="Uppercase",
            variable=self.case_var,
            value='upper',
            command=lambda: self.set_case('upper')
        )
        self.radio_upper.pack(side=tk.LEFT)

        # RULE FRAME
        self.rule_frame = tk.LabelFrame(root)
        self.rule_frame.pack()
        self.password.rule_list = []
        for key, value in self.password.config['rules_init'].items():
            self.add_rule(key, value)
        add_rule_button = tk.Button(
            root,
            text="+",
            width=36,
            command=self.add_rule
        )
        add_rule_button.pack(pady=(0,10))

        # CONFIG FRAME
        self.save_config = tk.Button(
            root,
            text="Save config",
            width=36,
            command=self.save_config
        )
        self.save_config.pack()

        # Initializing lists
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
