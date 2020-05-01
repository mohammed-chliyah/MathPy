from math import *
from operator import *
from tkinter import *
from tkinter import _cnfmerge as cnfmerge

# version 2.5.1
# Add Function Re-Click Equal Button, still Don't work in Keyboard Bind
btn_prm = {'padx': 16,
           'pady': 1,
           'bd': 4,
           'fg': 'white',
           'bg': '#666666',
           'font': ('Segoe UI Symbol', 16),
           'width': 2,
           'height': 1,
           'relief': 'flat',
           'activebackground': '#666666',
           'activeforeground': "white"}
big_prm = {'padx': 16,
           'pady': 1,
           'bd': 4,
           'fg': 'white',
           'bg': 'slate gray',
           'font': ('Segoe UI Symbol', 16),
           'width': 5,
           'height': 1,
           'relief': 'raised',
           'activebackground': 'dim gray',
           'activeforeground': "white"}
ent_prm = {'bd': 4,
           'fg': 'white',
           'bg': 'gray94',
           'font': ('Segoe UI Symbol', 18),
           'relief': 'flat'}


class EntryBox(Entry, Widget, XView):
    def __init__(self, master=None, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        kw = cnfmerge((kw, cnf))
        kw['justify'] = kw.get('justify', 'left')
        kw['state'] = 'readonly'
        super(EntryBox, self).__init__(master=master, **kw)


def Exit():
    return win.destroy()


class Calculator:
    def __init__(self, master):
        # expression that will be displayed on screen
        self.expression = ''
        # store expressions by order
        self.store = []
        # answer of operation
        self.ans = ''
        # store last answer of operation
        self.storeans = ['']
        # float numbers of equation
        self.a = ''
        self.b = ''
        self.c = ''
        # int range numbers of function
        self.v = ''
        self.w = ''
        # used to switch between buttons those will be displayed on screen
        self.first = ''
        self.secend = ''
        # used to switch between modes of Operation, Equation and Function
        self.mode = ''
        # default variable
        self.equal = False
        self.clear = False
        self.full = False
        self.half = False
        # string variable for text input
        self.TextVariable = StringVar()
        self.FastTextVariable = StringVar()

        # Master Display ROW 0==========================================================================================
        # First Text Display
        self.FirstTextDisplay = EntryBox(master, width=44, **ent_prm, textvariable=self.TextVariable)
        self.FirstTextDisplay.grid(row=0, column=0, columnspan=2)
        self.FirstTextDisplay.configure(fg='black', font=('Segoe UI Symbol', 35))
        self.FirstTextDisplay.bind('<Key>', self.KeyboardInput)
        # Second Text Display
        self.SecondTextDisplay = Entry(master, width=36, **ent_prm, textvariable=self.FastTextVariable)
        self.SecondTextDisplay.grid(row=1, column=1)
        self.SecondTextDisplay.configure(bg='slate gray', font=('Segoe UI Symbol', 26), justify='right')
        # Full Text Display
        self.FullTextDisplay = Text(master, width=52, height=13, **ent_prm)
        self.FullTextDisplay.grid(row=2, column=1, rowspan=2)
        self.FullTextDisplay.configure(bg='#4d4d4d')
        # ROW 1 set frame showing top buttons
        top_frame = Frame(master, relief='flat', bg='slate gray')
        top_frame.grid(row=1, column=0)
        # ROW 2 set frame showing middle buttons
        self.middle_frame = Frame(master, relief='flat', bg='#666666')
        self.middle_frame.grid(row=2, column=0)
        # ROW 3 set frame showing bottom buttons
        bottom_frame = Frame(master, relief='flat', bg='#666666')
        bottom_frame.grid(row=3, column=0)
        # buttons that will be displayed on top frame ROW 0=============================================================
        # Operation
        self.Operation = Button(top_frame, **big_prm, text="Operation",
                                command=lambda: self.SwitchFunction("Operation"))
        self.Operation.grid(row=0, column=0, columnspan=2)
        # Equation
        self.Equation = Button(top_frame, **big_prm, text="Equation", command=lambda: self.SwitchFunction("Equation"))
        self.Equation.grid(row=0, column=2, columnspan=2)
        # Function
        self.Function = Button(top_frame, **big_prm, text="Function", command=lambda: self.SwitchFunction("Function"))
        self.Function.grid(row=0, column=4, columnspan=2)
        # COMPLEX
        self.Complex = Button(top_frame, **big_prm, text='Complex', command=lambda: self.SwitchFunction("Complex"))
        self.Complex.grid(row=0, column=6, columnspan=2)

        # buttons that will be displayed on middle frame ROW 0==========================================================
        pad = ['(', ')', "", '', '', ""]
        txt = ['(', ')', "", 'Answer', 'r', "Õ"]
        btn = []
        i = 0
        for k in range(6):
            btn.append(Button(self.middle_frame, **btn_prm, text=txt[i]))
            btn[i].grid(row=1, column=k)
            btn[i]["command"] = lambda n=pad[i]: self.Input(n)
            i += 1
        # Answer Stored
        btn[3].configure(bg='SeaGreen3', activebackground='SeaGreen3',
                         command=lambda: self.Input(str(self.storeans[-1])))
        # Clear
        btn[4].configure(width=1, bg='indian red', activebackground='indian red', font=('Marlett', 23),
                         command=lambda: self.Clear())
        # Remove
        btn[5].configure(width=1, bg='Royalblue2', activebackground='Royalblue2', font=('Wingdings', 21),
                         command=lambda: self.Remove())
        # ROW 3
        # ========================Logarithm=============================================================================
        Logarithm_pad = ['log(', 'log10(', "log2(", 'log1p(', 'exp(', "expm1("]
        Logarithm_txt = ['logₑ', 'log¹º', "log²", 'log1p', 'exp', "expm1"]
        btn = []
        i = 0
        for k in range(6):
            btn.append(Button(self.middle_frame, **btn_prm, text=Logarithm_txt[i]))
            btn[i].grid(row=3, column=k)
            btn[i]["command"] = lambda n=Logarithm_pad[i]: self.Input(n)
            i += 1
        # buttons that will be displayed on bottom frame ROW 0==========================================================
        # ========================Numbers===============================================================================
        btn = ["7", "8", "9", "+", '**2', 'x', "4", "5", "6", "-", "**", "1j", "1", "2", "3", "*", "sqrt(",
               'e', '0', ".", "=", "/", "factorial(", 'pi']
        btn_txt = ["7", "8", "9", "+", 'n²', 'x', "4", "5", "6", "-", "nˣ", "j", "1", "2", "3", "*", "√n",
                   'e', '0', ".", "=", "/", "!n", 'π']
        self.btn = []
        i = 0
        for j in range(4):
            for k in range(6):
                self.btn.append(Button(bottom_frame, **btn_prm, text=btn_txt[i]))
                self.btn[i].grid(row=j, column=k)
                self.btn[i].configure(bg="#4d4d4d", activebackground="#4d4d4d", command=lambda n=btn[i]: self.Input(n))
                i += 1
        # Equals
        self.btn[20].configure(bg='#ff9950', activebackground='#ff9950', command=self.InputEquals)

        # run button switcher and display switcher mode=================================================================
        self.SwitchButtons('1st'), self.SwitchFunction('Operation')
        # Switch Menu In Bare Display=================================================================================
        filemenu.add_command(label="Operation", command=lambda: self.SwitchFunction("Operation"))
        filemenu.add_command(label='Equation', command=lambda: self.SwitchFunction('Equation'))
        filemenu.add_command(label='Function', command=lambda: self.SwitchFunction('Function'))
        filemenu.add_command(label='Complex', command=lambda: self.SwitchFunction('Complex'))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=Exit)

    def SwitchButtons(self, side):
        page = side
        # buttons that will be Switched on middle frame
        if page == '1st':
            # ROW 1
            # 2nd
            secend = Button(self.middle_frame, **btn_prm, text="1st", command=lambda: self.SwitchButtons("2nd"))
            secend.grid(row=1, column=2)
            secend.configure(foreground='orange', activeforeground='indian red')
            # ROW 2
            # ========================Trigonometry======================================================================
            Trigonometry_pad = ['cos(', 'sin(', "tan(", 'cosh(', 'sinh(', "tanh("]
            Trigonometry_txt = ['cos', 'sin', "tan", 'cosh', 'sinh', "tanh"]
            btn = []
            i = 0
            for k in range(6):
                btn.append(Button(self.middle_frame, **btn_prm, text=Trigonometry_txt[i]))
                btn[i].grid(row=2, column=k)
                btn[i]["command"] = lambda n=Trigonometry_pad[i]: self.Input(n)
                i += 1

        elif page == '2nd':
            # ROW 1
            # 1st
            first = Button(self.middle_frame, **btn_prm, text="2nd", command=lambda: self.SwitchButtons("1st"))
            first.grid(row=1, column=2)
            first.configure(foreground='orange', activeforeground='indian red')
            # ROW 2
            # ========================Trigonometry======================================================================
            Trigonometry_pad = ['acos(', 'asin(', "atan(", 'acosh(', 'asinh(', "atanh("]
            Trigonometry_txt = ['acos', 'asin', "atan", 'acosh', 'asinh', "atanh"]
            btn = []
            i = 0
            for k in range(6):
                btn.append(Button(self.middle_frame, **btn_prm, text=Trigonometry_txt[i]))
                btn[i].grid(row=2, column=k)
                btn[i]["command"] = lambda n=Trigonometry_pad[i]: self.Input(n)
                i += 1

    def SwitchFunction(self, passmode):
        self.mode = passmode
        self.FullTextDisplay.delete(1.0, END)
        if self.mode == 'Operation':
            self.FullTextDisplay.insert(INSERT, 'Mode Operation :')
            self.FastTextVariable.set('')
            self.Operation['bg'] = 'indian red'
            self.Equation['bg'] = 'slate gray'
            self.Function['bg'] = 'slate gray'
            self.Complex['bg'] = 'slate gray'
            self.btn[5]['state'] = ['disabled']
            self.btn[11]['state'] = ['disabled']

        elif self.mode == 'Equation':
            self.FullTextDisplay.insert(INSERT, 'Mode Equation : aX² + bX + c = 0')
            self.FastTextVariable.set('aX² + bX + c = 0')
            self.Equation['bg'] = 'indian red'
            self.Function['bg'] = 'slate gray'
            self.Operation['bg'] = 'slate gray'
            self.Complex['bg'] = 'slate gray'
            self.btn[5].config(state=DISABLED)
            self.btn[11].config(state=DISABLED)

        elif self.mode == 'Function':
            self.FullTextDisplay.insert(INSERT, 'Mode Function : f(x)')
            self.FastTextVariable.set(f'From : A --> To : B | f(x) = Function')
            self.Function['bg'] = 'indian red'
            self.Equation['bg'] = 'slate gray'
            self.Operation['bg'] = 'slate gray'
            self.Complex['bg'] = 'slate gray'
            self.btn[5]['state'] = ['normal']
            self.btn[11]['state'] = ['disabled']

        elif self.mode == 'Complex':
            self.FullTextDisplay.insert(INSERT, 'Mode Complex :')
            self.FastTextVariable.set('')
            self.Function['bg'] = 'slate gray'
            self.Equation['bg'] = 'slate gray'
            self.Operation['bg'] = 'slate gray'
            self.Complex['bg'] = 'indian red'
            self.btn[5].config(state=DISABLED)
            self.btn[11].config(state=NORMAL)

        self.Clear()

    def Clear(self):
        self.store = []
        self.expression = ''
        self.TextVariable.set('')
        self.FastTextVariable.set('')

        if self.mode == 'Equation':
            self.TextVariable.set(f'a = ')
            self.FastTextVariable.set('aX² + bX + c = 0')

        elif self.mode == 'Function':
            self.TextVariable.set(f'From : ')
            self.FastTextVariable.set(f'From : A --> To : B | f(x) = Function')

        self.equal = False
        self.clear = False
        self.full = False
        self.half = False

    def Remove(self):
        if self.clear:
            self.Clear()

        try:
            self.expression = str(self.expression).replace(self.store[-1], '')
            self.store.remove(self.store[-1])

        except IndexError:
            self.FastTextVariable.set('IndexError')

        self.Click()

    def Input(self, keyword):
        if self.clear:
            self.Clear()

        self.store.append((str(keyword)))
        self.expression += str(keyword)

        self.Click()

    def KeyboardInput(self, keyword):
        if self.clear:
            self.Clear()
        try:
            if keyword.keysym == 'BackSpace':
                self.expression = str(self.expression).replace(self.store[-1], '')
                self.store.remove(self.store[-1])

            elif keyword.keysym == 'Delete':
                self.Clear()

            elif keyword.keysym == 'slash':
                self.store.append((str('/')))
                self.expression += str('/')

            elif keyword.keysym == 'asterisk':
                self.store.append((str('*')))
                self.expression += str('*')

            elif keyword.keysym == 'minus':
                self.store.append((str('-')))
                self.expression += str('-')

            elif keyword.keysym == 'plus':
                self.store.append((str('+')))
                self.expression += str('+')

            elif keyword.keysym == 'period':
                self.store.append((str('.')))
                self.expression += str('.')

            elif keyword.keysym == 'parenleft':
                self.store.append((str('(')))
                self.expression += str('(')

            elif keyword.keysym == 'parenright':
                self.store.append((str(')')))
                self.expression += str(')')

            elif keyword.keysym == 'Return' or keyword.keysym == 'equal':
                return self.InputEquals()

            elif keyword.keysym == 'Shift_R' or keyword.keysym == 'Shift_L':
                pass

            else:
                self.store.append((str(keyword.keysym)))
                self.expression += str(keyword.keysym)

        except IndexError:
            self.FastTextVariable.set('IndexError')

        self.Click()

    def Click(self):
        try:
            if self.mode == 'Operation':
                self.FastTextVariable.set('')
                self.TextVariable.set(self.expression)
                self.FastTextVariable.set(eval(self.expression))

            elif self.mode == 'Equation':
                if not self.full and not self.half:
                    self.TextVariable.set(f'a = {self.expression}')
                    self.FastTextVariable.set(f'{self.expression}X² + bX + c = 0')

                elif not self.full and self.half:
                    self.TextVariable.set(f'b = {self.expression}')
                    self.FastTextVariable.set(f'{self.a}X² + ({self.expression})X + c = 0')

                elif self.full:
                    self.TextVariable.set(f'c = {self.expression}')
                    self.FastTextVariable.set(f'{self.a}X² + ({self.b})X + ({self.expression}) = 0')

            elif self.mode == "Function":
                if not self.full and not self.half:
                    self.TextVariable.set(f'From : {self.expression}')
                    self.FastTextVariable.set(f'From : {self.expression} --> To : B | f(x) = Function')

                elif not self.full and self.half:
                    self.TextVariable.set(f'To : {self.expression}')
                    self.FastTextVariable.set(f'From : {self.v} --> To : {self.expression} | f(x) = Function')

                elif self.full:
                    self.TextVariable.set(f'f(x) = {self.expression}')
                    self.FastTextVariable.set(f'From : {self.v} --> To : {int(self.w) - 1} | f(x) = {self.expression}')

            elif self.mode == 'Complex':
                self.FastTextVariable.set('')
                self.TextVariable.set(self.expression)
                self.FastTextVariable.set(eval(self.expression))

        except ZeroDivisionError:
            pass
        except ValueError:
            pass
        except SyntaxError:
            pass
        except NameError:
            pass
        except TypeError:
            pass

    def InputEquals(self):
        try:
            if self.mode == 'Operation':
                if not self.equal:
                    self.ans = eval(self.expression)
                    self.FastTextVariable.set('')
                    self.TextVariable.set(f'{self.expression} = {self.ans}')
                    self.FullTextDisplay.insert(INSERT, f'\n{self.expression} = {self.ans}')
                    self.clear = True
                    self.equal = True

                elif self.equal:
                    self.expression = str(self.storeans[-1])+str(self.store[-2])+str(self.store[-1])
                    self.ans = eval(self.expression)
                    self.FastTextVariable.set(self.ans)
                    self.TextVariable.set(f'{self.expression} = {self.ans}')
                    self.FullTextDisplay.insert(INSERT, f'\n{self.expression} = {self.ans}')

            elif self.mode == 'Equation':
                if not self.full:
                    if not self.half:
                        self.a = float(eval(self.expression))
                        self.expression = ""
                        self.TextVariable.set(f'b = ')
                        self.half = True

                    elif self.half:
                        self.b = float(eval(self.expression))
                        self.expression = ""
                        self.TextVariable.set(f'c = ')
                        self.full = True

                elif self.full:
                    c = float(eval(self.expression))
                    d = float((self.b ** 2) - 4 * self.a * c)
                    nd = neg(d)
                    nb = neg(self.b)
                    cx = complex
                    self.TextVariable.set(f'a = {self.a} | b = {self.b} | c = {c}')
                    self.FastTextVariable.set(f'{self.a}X² + ({self.b})X + ({c}) = 0')
                    if self.a > 0 or self.a < 0:
                        self.FullTextDisplay.insert(INSERT, f'''\n
The Equation : {self.a}X² + ({self.b})X + ({c}) = 0

 The Equation Have Two Solutions For X :

  ∆ =  b² - 4ac

  ∆ = {self.b}² - (4 x ({self.a}) x ({c})) 
      = {self.b ** 2} - ({4 * self.a * c}) 
      = {d}''')
                        if d == 0:
                            self.FullTextDisplay.insert(INSERT, f'''\n 
∆=0 : X = -b / 2a

    X[1] = X[2] = ({neg(self.b)}) / (2 x {self.a})
    X[1] = X[2] = {(neg(self.b)) / (2 * self.a)}''')
                        elif d >= 0:
                            self.FullTextDisplay.insert(INSERT, f'''\n
∆>0 : X = (-b ± √∆) / 2a

 X[1] = ({nb} + √{d}) / (2 x {self.a})
       = ({nb} + {sqrt(d)}) / ({2 * self.a})
       = {(nb + sqrt(d)) / (2 * self.a)}

 X[2] = ({nb} - √{d}) / (2 x {self.a})
       = ({nb} - {sqrt(d)}) / ({2 * self.a})
       = {(nb - sqrt(d)) / (2 * self.a)}''')
                        elif d <= 0:
                            self.FullTextDisplay.insert(INSERT, f'''\n          = {nd}j²

∆<0 : X = (-b ± j√∆) / 2a

 X[1] = ({nb} + √({nd})j) / (2 x {self.a})
       = {cx(nb + sqrt(nd) * 1j)} / ({2 * self.a})
       = {cx((nb + sqrt(nd) * 1j) / (2 * self.a))}

 X[2] = ({nb} - √({nd})j) / (2 x {self.a})
       = {cx(nb - sqrt(nd) * 1j)} / ({2 * self.a})
       = {cx((nb - sqrt(nd) * 1j) / (2 * self.a))}

  z = a ± bj

   a = {nb / (2 * self.a)}
   b = {sqrt(nd) / (2 * self.a)}''')
                    elif self.a == 0:
                        if self.b == 0 and c == 0:
                            self.TextVariable.set(f"Empty Solution {{Ꞩ}}")
                        elif self.b == 0:
                            self.TextVariable.set(f"Empty Solution {{Ꞩ}}")
                        elif c == 0:
                            self.FastTextVariable.set(f'{self.a}X² + ({self.b})X + ({c}) = 0')
                            self.FullTextDisplay.insert(INSERT, f'''\nThe Equation : {self.b}X + ({c}) = 0

 The Equation Have One Solution For X :

  {self.b}X = 0
  X = 0''')
                        else:
                            self.FullTextDisplay.insert(INSERT, f'''\nThe Equation : {self.b}X + ({c}) = 0 

 The Equation Have One Solution For X :  

  {self.b}X = {neg(c)}    
  X = {neg(c)} / {self.b}
  X = {neg(c) / self.b}''')

                    self.clear = True
                    self.full = False
                    self.half = False

            elif self.mode == 'Function':
                if not self.full:
                    if not self.half:
                        self.v = int(self.expression)
                        self.FullTextDisplay.insert(INSERT, f'\nfrom : {self.expression}')
                        self.expression = ""
                        self.TextVariable.set(f'To : ')
                        self.half = True

                    elif self.half:
                        self.w = int(self.expression) + 1
                        self.FullTextDisplay.insert(INSERT, f'\nTo : {self.expression}')
                        self.expression = ""
                        self.TextVariable.set(f'f(x) = ')
                        self.full = True

                elif self.full:
                    self.FullTextDisplay.insert(INSERT, f'\nf(x) = {self.expression}')
                    for x in range(self.v, self.w):
                        self.FullTextDisplay.insert(INSERT, f'\nf({x}) = {eval(self.expression)}')

                    self.clear = True
                    self.full = False
                    self.half = False

            elif self.mode == 'Complex':
                if not self.equal:
                    self.ans = eval(self.expression)
                    self.FastTextVariable.set('')
                    self.TextVariable.set(f'{self.expression} = {self.ans}')
                    self.FullTextDisplay.insert(INSERT, f'\n{self.expression} = {self.ans}')
                    self.clear = True
                    self.equal = True

                elif self.equal:
                    self.expression = str(self.storeans[-1]) + str(self.store[-2]) + str(self.store[-1])
                    self.ans = eval(self.expression)
                    self.FastTextVariable.set(self.ans)
                    self.TextVariable.set(f'{self.expression} = {self.ans}')
                    self.FullTextDisplay.insert(INSERT, f'\n{self.expression} = {self.ans}')

        except ZeroDivisionError:
            self.FastTextVariable.set('ZeroDivisionError')
        except ValueError:
            self.FastTextVariable.set('ValueError')
        except SyntaxError:
            self.FastTextVariable.set('SyntaxError')
        except NameError:
            self.FastTextVariable.set('NameError')
        except TypeError:
            self.FastTextVariable.set('TypeError')

        self.storeans.append(str(self.ans))


if __name__ == "__main__":
    win = Tk()
    menubare = Menu(win)
    filemenu = Menu(menubare, tearoff=0)
    menubare.add_cascade(label="File", menu=filemenu)
    # run calculator
    Calculator(win)
    # Window configuration
    # win.configure(menu=menubare, bg='#666666')
    win.configure(menu=menubare, bg='#4d4d4d')
    win.resizable(False, False)
    win.title("Scientific Calculator v2.5.1")
    win.mainloop()
