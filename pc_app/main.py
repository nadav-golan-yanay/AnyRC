import sys
sys.path.append("c:/Users/nadav/OneDrive/Desktop/RealSIm5.0/pc_app")
import tkinter as tk
from src.appUI import PS5ControllerApp  # Correct import for the src directory

def main():
    root = tk.Tk()
    app = PS5ControllerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    print("Exiting...")