import tkinter as tk
import gc
from src.appUI import AnyRC

def main():
    try:
        root = tk.Tk()
        # Set up exception handling for the Tk instance
        root.report_callback_exception = lambda exc, val, tb: print(f"Error in Tk callback: {exc}, {val}")
        
        app = AnyRC(root)
        
        # Enable garbage collection
        gc.enable()
        
        root.mainloop()
    except Exception as e:
        print(f"Critical error in main: {e}")
    finally:
        gc.collect()  # Final cleanup

if __name__ == "__main__":
    main()