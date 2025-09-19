from gui.main_window import MainWindow
from utils.config_manager import ConfigManager


if __name__ == "__main__":
    config = ConfigManager()
    app = MainWindow(config)
    app.mainloop()