import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        
        # Configure colors
        self.bg_color = "#2C3E50"
        self.btn_color = "#34495E"
        self.operator_color = "#3498DB"
        self.equals_color = "#2ECC71"
        self.clear_color = "#E74C3C"
        self.text_color = "#ECF0F1"
        
        self.root.configure(bg=self.bg_color)
        
        # Current calculation
        self.current_input = ""
        self.result_displayed = False
        
        self.create_widgets()
        self.setup_keyboard_bindings()
    
    def create_widgets(self):
        # Create display frame
        display_frame = tk.Frame(self.root, bg=self.bg_color, height=100)
        display_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        # Display for current calculation
        self.display = tk.Entry(
            display_frame,
            font=('Arial', 20),
            bd=0,
            justify='right',
            bg="#1C2833",
            fg=self.text_color,
            insertbackground=self.text_color,
            readonlybackground="#1C2833"
        )
        self.display.pack(fill="both", expand=True, ipady=15)
        self.display.config(state='readonly')
        
        # Mini display for previous operations
        self.mini_display = tk.Label(
            display_frame,
            font=('Arial', 12),
            bg=self.bg_color,
            fg="#7F8C8D",
            anchor='e',
            height=1
        )
        self.mini_display.pack(fill="x")
        
        # Create buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Button layout
        buttons = [
            ('C', 1, 0, self.clear_color), ('⌫', 1, 1, self.clear_color), ('%', 1, 2, self.operator_color), ('/', 1, 3, self.operator_color),
            ('7', 2, 0, self.btn_color), ('8', 2, 1, self.btn_color), ('9', 2, 2, self.btn_color), ('×', 2, 3, self.operator_color),
            ('4', 3, 0, self.btn_color), ('5', 3, 1, self.btn_color), ('6', 3, 2, self.btn_color), ('-', 3, 3, self.operator_color),
            ('1', 4, 0, self.btn_color), ('2', 4, 1, self.btn_color), ('3', 4, 2, self.btn_color), ('+', 4, 3, self.operator_color),
            ('±', 5, 0, self.btn_color), ('0', 5, 1, self.btn_color), ('.', 5, 2, self.btn_color), ('=', 5, 3, self.equals_color),
        ]
        
        # Configure grid
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1)
        
        # Create buttons
        self.buttons = {}
        for (text, row, col, color) in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=('Arial', 16, 'bold'),
                bg=color,
                fg=self.text_color,
                activebackground=self.lighten_color(color),
                activeforeground=self.text_color,
                bd=0,
                relief='flat',
                command=lambda t=text: self.button_click(t)
            )
            btn.grid(row=row, column=col, sticky='nsew', padx=3, pady=3)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.lighten_color(b['bg'])))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
            self.buttons[text] = btn
    
    def setup_keyboard_bindings(self):
        # Number keys
        for i in range(10):
            self.root.bind(str(i), lambda e, num=i: self.button_click(str(num)))
        
        # Operator keys
        self.root.bind('+', lambda e: self.button_click('+'))
        self.root.bind('-', lambda e: self.button_click('-'))
        self.root.bind('*', lambda e: self.button_click('×'))
        self.root.bind('/', lambda e: self.button_click('/'))
        
        # Other keys
        self.root.bind('.', lambda e: self.button_click('.'))
        self.root.bind('%', lambda e: self.button_click('%'))
        self.root.bind('<Return>', lambda e: self.button_click('='))
        # <Equal> event'ini kaldırdık, yerine '=' tuşunu ekledik
        self.root.bind('=', lambda e: self.button_click('='))
        self.root.bind('<BackSpace>', lambda e: self.button_click('⌫'))
        self.root.bind('<Delete>', lambda e: self.button_click('C'))
        self.root.bind('<Escape>', lambda e: self.button_click('C'))
        self.root.bind('<KeyPress>', self.on_key_press)
    
    def lighten_color(self, color):
        # Convert hex to RGB
        if color.startswith('#'):
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            # Lighten by 20%
            r = min(255, int(r * 1.2))
            g = min(255, int(g * 1.2))
            b = min(255, int(b * 1.2))
            return f'#{r:02x}{g:02x}{b:02x}'
        return color
    
    def button_click(self, text):
        if self.result_displayed and text not in ['+', '-', '×', '/', '%']:
            self.current_input = ""
            self.result_displayed = False
        
        if text == 'C':  # Clear
            self.current_input = ""
            self.mini_display.config(text="")
        
        elif text == '⌫':  # Backspace
            self.current_input = self.current_input[:-1]
        
        elif text == '±':  # Plus/Minus
            if self.current_input and self.current_input[-1].isdigit():
                # Find the last number
                last_num = ""
                for char in reversed(self.current_input):
                    if char.isdigit() or char == '.':
                        last_num = char + last_num
                    else:
                        break
                if last_num:
                    new_num = f"(-{last_num})" if not last_num.startswith('(-') else last_num[2:-1]
                    self.current_input = self.current_input[:-len(last_num)] + new_num
        
        elif text == '%':  # Percentage
            try:
                # Calculate percentage
                result = eval(self.current_input.replace('×', '*')) / 100
                self.current_input = str(result)
                self.result_displayed = True
            except:
                self.current_input = "Error"
                self.result_displayed = True
        
        elif text == '=':  # Equals
            try:
                # Replace display symbols with Python operators
                expression = self.current_input.replace('×', '*')
                result = eval(expression)
                
                # Update mini display with the calculation
                self.mini_display.config(text=f"{self.current_input} =")
                
                # Format result
                if isinstance(result, float):
                    # Remove trailing zeros
                    result_str = ('%.10f' % result).rstrip('0').rstrip('.')
                    if len(result_str) > 10:
                        result_str = f"{result:.6g}"
                else:
                    result_str = str(result)
                
                self.current_input = result_str
                self.result_displayed = True
            except ZeroDivisionError:
                self.current_input = "Error: Division by zero"
                self.result_displayed = True
            except:
                self.current_input = "Error"
                self.result_displayed = True
        
        else:  # Numbers and operators
            # Replace × with * for internal processing
            if text == '×':
                internal_text = '*'
            else:
                internal_text = text
            
            # Check if we're adding an operator after a result
            if self.result_displayed and text in ['+', '-', '×', '/']:
                self.result_displayed = False
            elif self.result_displayed:
                self.current_input = ""
                self.result_displayed = False
            
            self.current_input += internal_text
        
        # Update display
        display_text = self.current_input.replace('*', '×')
        self.update_display(display_text)
    
    def update_display(self, text):
        self.display.config(state='normal')
        self.display.delete(0, tk.END)
        self.display.insert(0, text)
        self.display.config(state='readonly')
        
        # Update button states based on input
        self.update_button_states()
    
    def update_button_states(self):
        # Enable/disable decimal point based on current number
        current_text = self.current_input
        
        # Find the last number in the expression
        if current_text:
            # Split by operators to find last number
            operators = ['+', '-', '*', '/']
            last_num = ""
            for char in reversed(current_text):
                if char.isdigit() or char == '.':
                    last_num = char + last_num
                elif char in operators or char == '(':
                    break
            
            # Disable decimal if last number already has one
            if '.' in last_num:
                self.buttons['.'].config(state='disabled')
            else:
                self.buttons['.'].config(state='normal')
        else:
            self.buttons['.'].config(state='normal')
    
    def on_key_press(self, event):
        # Visual feedback for keyboard presses
        key = event.char
        
        # Map keyboard keys to calculator buttons
        key_map = {
            '*': '×',
            'c': 'C',
            'C': 'C',
            '\r': '=',  # Enter key
            '\x08': '⌫',  # Backspace
            '\x7f': 'C',  # Delete
        }
        
        if key in key_map:
            btn_text = key_map[key]
        elif key.isdigit() or key in ['+', '-', '/', '.', '%', '=']:
            btn_text = key
        else:
            return
        
        # Visual feedback
        if btn_text in self.buttons:
            btn = self.buttons[btn_text]
            original_color = btn['bg']
            btn.config(bg=self.lighten_color(original_color))
            self.root.after(100, lambda: btn.config(bg=original_color))

def main():
    root = tk.Tk()
    
    # Set application icon (optional)
    try:
        root.iconbitmap('calculator.ico')  # You can create an icon file
    except:
        pass
    
    # Create calculator instance
    calculator = Calculator(root)
    
    # Center the window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()
