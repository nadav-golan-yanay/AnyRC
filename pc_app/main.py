import tkinter as tk
from src.appUI import AnyRC

def main():
    # Launch the UI
    root = tk.Tk()
    app = AnyRC(root)
    app.update_rc_display_periodically()  # Start periodic updates
    root.mainloop()

if __name__ == "__main__":
    main()