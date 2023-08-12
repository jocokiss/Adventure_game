class Color:
    def __init__(self):
        self.pink = '\033[95m'
        self.blue = '\033[94m'
        self.cyan = '\033[96m'
        self.green = '\033[92m'
        self.gold = '\033[93m'
        self.red = '\033[91m'
        self.end_of_modification = '\033[0m'
        self.bold = '\033[1m'
        self.underline = '\033[4m'

    def paint(self, color, text):
        if hasattr(self, color):
            color_code = getattr(self, color)
            return f"{color_code}{text}{self.end_of_modification}"
        else:
            return text