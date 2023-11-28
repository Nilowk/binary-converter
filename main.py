from tkinter import *

class App(Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.geometry("265x290")
        self.maxsize(265, 290)
        self.minsize(265, 290)
        self.initialize()

    def initialize(self):
        self.mode_frame = Mode(self)
        self.binary_selector = BinarySelector(self)
        self.binary_display = BinaryDisplay(self, self.binary_selector.binary)

    def update(self):
        self.binary_selector.update()
        self.binary_display.update(self.binary_selector.binary)

    def update_entry(self, sv):
        s = sv.get()
        if not s.lstrip("-").isdigit():
            return
        if (self.mode_frame.mode.get() == "unsigned"):
            if int(s) <= 255 and int(s) >= 0:
                self.binary_selector.update_entry(int(s))
        elif (self.mode_frame.mode.get() == "signed"):
            if int(s) >= -127 and int(s) <= 127:
                self.binary_selector.update_entry(int(s))
        elif (self.mode_frame.mode.get() == "signed2"):
            if int(s) >= -128 and int(s) <= 127:
                self.binary_selector.update_entry(int(s))
        
    def run(self):
        self.mainloop()

class Mode(LabelFrame):
    def __init__(self, app):
        super().__init__(app, text="Mode")
        self.grid()
        self.app = app
        self.mode = StringVar(value="unsigned")
        self.initialize()

    def initialize(self):
        buttons = {"entier non signé": "unsigned", "entier signé (bit de signe)": "signed", "entier signé (complément à 2)": "signed2"}
        i = 0
        for button in buttons.keys():
            radio = Radiobutton(self, text=button, value=buttons[button], variable=self.mode, command=self.app.update)
            radio.grid(column=0, row=i, ipadx=10, ipady=10)
            i += 1

class BinarySelector(Frame):
    def __init__(self, app):
        super().__init__(app)
        self.grid(column=0, row=1, padx=20, pady=20)
        self.app = app
        self.binary = [IntVar() for i in range(8)]
        self.labels = [Label(self, text="0") for i in range(8)]
        self.checkboxs = [None for i in range(8)]
        self.initialize()
    
    def update(self):
        i = 0
        for bit in self.binary:
            self.labels[i].config(text=str(bit.get()))
            i += 1

    def decimal_to_binary(self, decimal):
        result = [0 for i in range(8)]
        for i in range(8):
            result[i] = decimal % 2
            decimal = decimal // 2
        result.reverse()
        return result

    def decimal_to_signed_binary(self, decimal):
        result = [0 for i in range(8)]
        if decimal < 0:
            result[0] = 1
        decimal = abs(decimal)
        for i in range(7):
            I = 7 - i
            result[I] = decimal % 2
            decimal = decimal // 2 
        return result

    def decimal_to_signed2_binary(self, decimal):
        result = self.decimal_to_binary(decimal)
        if (decimal < 0):
            result = self.decimal_to_binary(decimal + 2**8)
        return result

    def update_entry(self, decimal):
        bin = self.decimal_to_binary(decimal)
        if (self.app.mode_frame.mode.get() == "signed"):
            bin = self.decimal_to_signed_binary(decimal)
        elif (self.app.mode_frame.mode.get() == "signed2"):
            bin = self.decimal_to_signed2_binary(decimal)
        for i in range(8):
            checkbox = self.checkboxs[i]
            self.binary[i].set(bin[i])
            checkbox.config(variable=self.binary[i])
        self.update()

    def initialize(self):
        i = 0
        for bit in self.binary:
            checkbox = Checkbutton(self, variable=bit, onvalue=1, offvalue=0, command=self.app.update)
            checkbox.grid(column=i, row=0)
            self.checkboxs[i] = checkbox
            self.labels[i].grid(column=i, row=1)
            i += 1

class BinaryDisplay(Entry):
    def __init__(self, app, binary):
        self.app = app
        self.display = StringVar(app, value=self.binary_to_decimal(binary))
        super().__init__(app, textvariable=self.display)
        self.grid(column=0, row=2, padx=20, pady=20)

    def binary_to_decimal(self, binary):
        result = 0
        if (self.app.mode_frame.mode.get() == "unsigned"):
            for i in range(8):
                I = 7 - i
                x = binary[I].get()*2**i
                result += x
        elif (self.app.mode_frame.mode.get() == "signed"):
            for i in range(7):
                I = 7 - i
                x = binary[I].get()*2**i
                result += x
            if (binary[0].get() == 1):
                result -= 2*result
        elif (self.app.mode_frame.mode.get() == "signed2"):
            for i in range(8):
                I = 7 - i
                x = binary[I].get()*2**i
                result += x
            if (binary[0].get() == 1):
                result -= 2**8
        return str(result)

    def update(self, binary):
        self.display = StringVar(self.app, value=self.binary_to_decimal(binary))
        self.display.trace("w", lambda name, index, mode, sv=self.display: self.app.update_entry(sv))
        self.config(textvariable=self.display)


app = App("Convertisseur Binaire")
app.run()