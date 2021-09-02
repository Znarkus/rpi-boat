import tkinter as tk
import RPi.GPIO as GPIO
import time
import sys

GPIO_IN = [
    3, 5, 7, 29, 31, 26, 24, 21
]

LABELS = [
    'Belysning',
    'Länspump fram',
    'Länspump bak',
    'Maserator',
    'Lanternor',
    'Torpeder',
    'Katapultstol',
    'Undervattensläge'
]

buttons = {x: None for x in range(8)}
state = {x: False for x in range(8)}

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master,
                         bg='black',
                         cursor='none')
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        for x, button in buttons.items():
            buttons[x] = tk.Button(
                self,
                width=25,
                height=2,
                bg='black',
                fg='white',
                activebackground='black',
                activeforeground='white',
                font = ("Helvetica", 16)
            )
            buttons[x]["text"] = LABELS[x]
            buttons[x]["command"] = lambda x=x: self.toggle(x)
            buttons[x].grid(
                row=x,
                column=0,
                padx=10,
                pady=14)
        

        self.quit = tk.Button(self, text="Self destruct", bg='black', fg="red",
                              command=self.master.destroy,
                              activebackground='black',
                              activeforeground='red')
        self.quit.grid(row=len(buttons),column=0,pady=10)

    def toggle(self, idx):
        state[idx] = not state[idx]
        output = GPIO.LOW if state[idx] else GPIO.HIGH
        pin = GPIO_IN[idx]
        print("Toggle output pin", pin, "value", output)
        GPIO.output(pin, output)
        if state[idx]:
            buttons[idx].configure(bg='slate gray',
                                   activebackground='slate gray')
        else:
            buttons[idx].configure(bg='black',
                                   activebackground='black')

GPIO.setmode(GPIO.BOARD)
try:
    print("Setting up")
    for pin in GPIO_IN:
        print("Set up pin", pin, "for output")
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
except IndexError as err:
    print("Error: {0}".format(err))

root = tk.Tk()
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()

root.configure(bg='black')
app = Application(master=root)
app.master.title("I'm a boat")
app.mainloop()

print("Cleaning up")
GPIO.cleanup()