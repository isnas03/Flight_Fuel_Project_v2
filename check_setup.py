"""Run with the project's .runtime interpreter to diagnose GUI dependencies."""
import sys
print('Python executable:', sys.executable)
print('Python version:', sys.version)
try:
    import tkinter as tk
    import _tkinter
    import matplotlib
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    print('Tk module:', _tkinter.__file__)
    print('Matplotlib:', matplotlib.__version__)
    root = tk.Tk()
    root.title('Setup check — close this window to finish')
    version = root.tk.call('package', 'require', 'Tk')
    print('Tk version:', version, flush=True)
    if tuple(int(x) for x in version.split('.')[:2]) < (8, 6):
        root.destroy()
        raise RuntimeError('Tk 8.6+ required. Use the supplied project environment.')
    figure = Figure(figsize=(6, 3), layout='constrained')
    axis = figure.add_subplot(111)
    axis.bar(['Required', 'Available'], [184, 200])
    axis.set_ylabel('Litres')
    axis.set_title('If you see two bars, Tkinter + Matplotlib are rendering')
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    root.mainloop()
except Exception as error:
    print('SETUP CHECK FAILED:', error)
    sys.exit(1)
print('Setup check finished. Confirm the chart was visible.')
