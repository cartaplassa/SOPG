import tkinter as tk
import sopg_cli as core


def to_clipboard(root: tk.Tk, password: core.Password):
    root.clipboard_clear()
    root.clipboard_append(password.get())


def regen_one(password: core.Password, buttons: list[tk.Button], button_frame: tk.Frame, number: int):
    password.leetrules = leetrules if leetify_var.get() else {}
    password.regen_one(number)
    update_buttons(password, buttons, button_frame)


def regen_whole(password: core.Password, buttons: list[tk.Button], button_frame: tk.Frame):
    password.leetrules = leetrules if leetify_var.get() else {}
    password.regen_whole()
    update_buttons(password, buttons, button_frame)


def update_buttons(password: core.Password, buttons: list[tk.Button], button_frame: tk.Frame):
    for button in buttons:
        button.destroy()
    buttons = []
    for i in range(len(password.words)):
        buttons.append(tk.Button(button_frame, text=password.words[i], command=lambda x = i: regen_one(password, buttons, button_frame, x)))
        buttons[i].pack(side=tk.LEFT)
    buttons.append(tk.Button(button_frame, text="Regen PW", command=lambda: regen_whole(password, buttons, button_frame)))
    buttons[-1].pack(side=tk.LEFT)


def main():
    global buttons
    global leetrules
    global leetify_var
    password = core.Password()
    leetrules = {
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
    root = tk.Tk()
    root.title("Secure-Obscure Password Generator")

    header = tk.Frame(root)
    header.pack()

    button_frame = tk.Frame(header)
    button_frame.grid(row=0,column=0)
    mgmt_frame = tk.Frame(header)
    mgmt_frame.grid(row=0,column=1)

    buttons = []
    update_buttons(password, buttons, button_frame)

    copy_button = tk.Button(mgmt_frame, text="Copy to CB", command=lambda: to_clipboard(root, password))
    copy_button.pack(side=tk.LEFT)

    leetify_var = tk.BooleanVar()
    leetify_box = tk.Checkbutton(mgmt_frame, text='Leetify', variable=leetify_var, offvalue=False, onvalue=True)
    leetify_box.pack(side=tk.LEFT)
    leetify_box.select()


    root.mainloop()


if __name__ == '__main__':
    main()
