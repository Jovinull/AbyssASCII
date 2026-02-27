# healthbar.py
"""
Módulo para exibição de barras de status (health/mana/energia) em ASCII, com suporte a cores e customização.
"""

class BarStyle:
    def __init__(self, symbol_full="█", symbol_empty="_", length=20, color_full="\033[92m", color_empty="\033[90m", color_text="\033[0m"):
        self.symbol_full = symbol_full
        self.symbol_empty = symbol_empty
        self.length = length
        self.color_full = color_full
        self.color_empty = color_empty
        self.color_text = color_text

class StatusBar:
    def __init__(self, label, current, maximum, style: BarStyle, color_warning="\033[93m", color_critical="\033[91m"):
        self.label = label
        self.current = current
        self.maximum = maximum
        self.style = style
        self.color_warning = color_warning
        self.color_critical = color_critical

    def get_color(self):
        ratio = self.current / self.maximum if self.maximum else 0
        if ratio > 0.66:
            return self.style.color_full
        elif ratio > 0.33:
            return self.color_warning
        else:
            return self.color_critical

    def render(self):
        filled = round(self.current / self.maximum * self.style.length) if self.maximum else 0
        empty = self.style.length - filled
        color = self.get_color()
        bar = f"{color}{self.style.symbol_full * filled}{self.style.color_empty}{self.style.symbol_empty * empty}{self.style.color_text}"
        return f"{self.label}: {self.current} / {self.maximum}\n|{bar}|"

    def update(self, current):
        self.current = max(0, min(current, self.maximum))

# Exemplo de uso:
if __name__ == "__main__":
    import time
    health_style = BarStyle(symbol_full="█", symbol_empty="_", length=30, color_full="\033[92m", color_empty="\033[90m")
    mana_style = BarStyle(symbol_full="█", symbol_empty="_", length=30, color_full="\033[96m", color_empty="\033[90m")
    health = StatusBar("HEALTH", 100, 100, health_style)
    mana = StatusBar("MANA", 50, 50, mana_style)
    for i in range(51):
        print("\033c", end="")  # Limpa terminal
        print(health.render())
        print(mana.render())
        health.update(health.current - 2)
        mana.update(mana.current - 1)
        time.sleep(0.1)
