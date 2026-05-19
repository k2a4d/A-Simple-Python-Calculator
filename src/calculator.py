import math
import tkinter as tk

# --- YOUR CALCULATOR BACKEND ---
class Calculator:
    def __init__(self, memory=0):
        self.memory = memory

    def reset_memory(self):
        self.memory = 0

    def sum(self, a, b=None):
        try:
            if b is None: b = self.memory
            self.memory = float(a) + float(b)
            return self.memory
        except: return 'Invalid input'

    def subtract(self, a, b=None):
        try:
            if b is None: b = a; a = self.memory
            self.memory = float(a) - float(b)
            return self.memory
        except: return 'Invalid input'

    def multiply(self, a, b=None):
        try:
            if b is None: b = self.memory
            self.memory = float(a) * float(b)
            return self.memory
        except: return 'Invalid input'

    def divide(self, a, b=None):
        try:
            if b is None: b = a; a = self.memory
            self.memory = float(a) / float(b)
            return self.memory
        except ZeroDivisionError: return 'Can not divide by zero.'
        except: return 'Invalid input'

    def square(self, a=None):
        try:
            if a is None: a = self.memory
            self.memory = float(a) ** 2
            return self.memory
        except: return 'Invalid input'

    def sqrt(self, a=None):
        try:
            if a is None: a = self.memory
            self.memory = math.sqrt(float(a))
            return self.memory
        except: return 'Invalid input'


# --- PERFECTED PROPORTIONAL GUI ---
class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")
        self.root.geometry("360x520")
        
        self.calc = Calculator()
        self.current_input = ""
        self.stored_value = None
        self.active_operator = None
        
        self.themes = {
            "light": {"bg": "#F4F4F4", "display_bg": "#FFFFFF", "fg": "#000000", "btn_bg": "#EAEAEA", "op_bg": "#FF9500", "op_fg": "#FFFFFF"},
            "dark":  {"bg": "#17171C", "display_bg": "#25252B", "fg": "#FFFFFF", "btn_bg": "#2E2F38", "op_bg": "#FF9500", "op_fg": "#FFFFFF"}
        }
        self.current_theme = "dark" 
        self.buttons_list = []
        self.toggle_canvas = None 
        
        self.setup_ui()
        self.bind_keyboard() 
        self.apply_theme()

    def setup_ui(self):
        self.screen = tk.Label(self.root, text="0", font=("Arial", 32), anchor="e", padx=15, pady=25)
        self.screen.pack(fill="both", expand=False)

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(fill="both", expand=True)

        layout = [
            ("TOGGLE", 0, 0, 'sys'),  ("C", 0, 1, 'sys'),    ("x²", 0, 2, 'op'),   ("√", 0, 3, 'op'),
            ("7", 1, 0, 'num'),      ("8", 1, 1, 'num'),    ("9", 1, 2, 'num'),   ("/", 1, 3, 'op'),
            ("4", 2, 0, 'num'),      ("5", 2, 1, 'num'),    ("6", 2, 2, 'num'),   ("*", 2, 3, 'op'),
            ("1", 3, 0, 'num'),      ("2", 3, 1, 'num'),    ("3", 3, 2, 'num'),   ("-", 3, 3, 'op'),
            ("0", 4, 0, 'num'),      (".", 4, 1, 'num'),    ("=", 4, 2, 'sys'),   ("+", 4, 3, 'op')
        ]

        # Force all 4 columns and 5 rows to scale COMPLETELY identically using 'uniform' strings
        for j in range(4):
            self.grid_frame.columnconfigure(j, weight=1, uniform="equal_cols")
        for i in range(5):
            self.grid_frame.rowconfigure(i, weight=1, uniform="equal_rows")

        for text, row, col, b_type in layout:
            if text == "TOGGLE":
                # Explicitly set height/width here to prevent it from forcing row 0 to stretch out
                self.toggle_canvas = tk.Canvas(self.grid_frame, borderwidth=0, highlightthickness=0, cursor="hand2", width=1, height=1)
                self.toggle_canvas.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
                self.toggle_canvas.bind("<Button-1>", lambda event: self.toggle_theme())
                continue
                
            if text == "=":
                cmd = self.calculate_result
            elif text == "C":
                cmd = self.clear_screen
            elif b_type == 'num':
                cmd = lambda t=text: self.press_number(t)
            else:
                cmd = lambda t=text: self.press_operator(t)

            btn = tk.Button(self.grid_frame, text=text, font=("Arial", 14, "bold"), borderwidth=1, relief="flat", command=cmd)
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            self.buttons_list.append((btn, b_type))

    def bind_keyboard(self):
        for num in "0123456789.":
            self.root.bind(num, lambda event, digit=num: self.press_number(digit))
        for op in "+-*/":
            self.root.bind(op, lambda event, operator=op: self.press_operator(operator))
        self.root.bind("<Return>", lambda event: self.calculate_result())
        self.root.bind("=", lambda event: self.calculate_result())
        self.root.bind("<Escape>", lambda event: self.clear_screen())
        self.root.bind("<BackSpace>", lambda event: self.clear_screen())

    def press_number(self, num):
        if self.current_input == "0" and num != ".":
            self.current_input = num
        else:
            self.current_input += num
        self.screen.config(text=self.current_input)

    def press_operator(self, operator):
        val = self.current_input if self.current_input else "0"
        if operator == "x²":
            res = self.calc.square(val)
            self.update_display_direct(res)
        elif operator == "√":
            res = self.calc.sqrt(val)
            self.update_display_direct(res)
        else:
            self.stored_value = float(val)
            self.active_operator = operator
            self.current_input = ""

    def calculate_result(self):
        if self.active_operator is None or not self.current_input:
            return

        second_val = float(self.current_input)
        result = 0

        if self.active_operator == "+":
            result = self.calc.sum(self.stored_value, second_val)
        elif self.active_operator == "-":
            result = self.calc.subtract(self.stored_value, second_val)
        elif self.active_operator == "*":
            result = self.calc.multiply(self.stored_value, second_val)
        elif self.active_operator == "/":
            result = self.calc.divide(self.stored_value, second_val)

        self.update_display_direct(result)
        self.active_operator = None

    def update_display_direct(self, output_value):
        if isinstance(output_value, float) and output_value.is_integer():
            output_value = int(output_value)
        self.current_input = str(output_value)
        self.screen.config(text=self.current_input)

    def clear_screen(self):
        self.calc.reset_memory()
        self.current_input = ""
        self.stored_value = None
        self.active_operator = None
        self.screen.config(text="0")

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def draw_vector_icon(self, color, op_color):
        self.toggle_canvas.delete("all")
        
        w = self.toggle_canvas.winfo_width()
        h = self.toggle_canvas.winfo_height()
        
        # Safe defaults
        if w <= 1: w = 86
        if h <= 1: h = 76
        
        cx, cy = w / 2, h / 2  
        
        if self.current_theme == "dark":
            # Sun core
            r = 10
            self.toggle_canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color, outline=color)
            # Sun rays
            ray_len = 16
            ray_start = 13
            for i in range(8):
                angle = math.radians(i * 45)
                x1 = cx + ray_start * math.cos(angle)
                y1 = cy + ray_start * math.sin(angle)
                x2 = cx + ray_len * math.cos(angle)
                y2 = cy + ray_len * math.sin(angle)
                self.toggle_canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        else:
            # Moon crescent
            r = 12
            self.toggle_canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color, outline=color)
            offset = 5
            self.toggle_canvas.create_oval(cx-r+offset, cy-r-offset, cx+r+offset, cy+r-offset, fill=op_color, outline=op_color)

    def apply_theme(self):
        colors = self.themes[self.current_theme]
        self.root.config(bg=colors["bg"])
        self.screen.config(bg=colors["display_bg"], fg=colors["fg"])
        self.grid_frame.config(bg=colors["bg"])

        for btn, b_type in self.buttons_list:
            if b_type == 'op' or btn.cget("text") == "=":
                btn.config(bg=colors["op_bg"], fg=colors["op_fg"], activebackground="#E08500")
            else:
                btn.config(bg=colors["btn_bg"], fg=colors["fg"], activebackground=colors["btn_bg"])
                
        if self.toggle_canvas:
            self.toggle_canvas.config(bg=colors["btn_bg"])
            self.root.update_idletasks()
            self.draw_vector_icon(colors["fg"], colors["btn_bg"])


if __name__ == "__main__":
    window = tk.Tk()
    app = CalculatorGUI(window)
    window.bind("<Configure>", lambda e: app.draw_vector_icon(app.themes[app.current_theme]["fg"], app.themes[app.current_theme]["btn_bg"]))
    window.mainloop()