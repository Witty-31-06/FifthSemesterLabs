class ANSI_COLOR:


    def __init__(self):
        self.ansi_colors = {
        0: "\033[38;5;255m",
        1: "\033[38;5;1m",   # Red
        2: "\033[38;5;2m",   # Green
        3: "\033[38;5;3m",   # Yellow
        4: "\033[38;5;4m",   # Blue
        5: "\033[38;5;5m",   # Magenta
        6: "\033[38;5;6m",   # Cyan
        7: "\033[38;5;7m",   # White
        8: "\033[38;5;8m",   # Bright Black (Gray)
        9: "\033[38;5;9m",   # Bright Red
        10: "\033[38;5;10m", # Bright Green
        11: "\033[38;5;11m", # Bright Yellow
        12: "\033[38;5;12m", # Bright Blue
        13: "\033[38;5;13m", # Bright Magenta
        14: "\033[38;5;14m", # Bright Cyan
        15: "\033[38;5;15m", # Bright White
        # 216 RGB colors (16-231)
        }
        for i in range(16, 255):
            self.ansi_colors[i] = f"\033[38;5;{i}m"
        self.ansi_colors[255] = "\033[38;5;0m"