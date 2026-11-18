"""Educational flight fuel estimator. Run: python fuel_calculator.py.

Uses Tkinter for the interface and Matplotlib for the embedded chart.
Constant average speed and consumption; not for operational flight planning.
"""
import csv
import math
from datetime import datetime
from pathlib import Path

FIELDS = (
    ('distance_km', 'Flight distance (km)', '600'),
    ('speed_kmh', 'Average speed (km/h)', '300'),
    ('consumption_lph', 'Fuel consumption (L/hour)', '80'),
    ('reserve_percent', 'Reserve (% of trip fuel)', '15'),
    ('available_l', 'Available fuel (L)', '200'),
)


def calculate(raw):
    """Validate inputs and return full-precision values and calculated results."""
    values = {}
    for key, label, _ in FIELDS:
        try:
            number = float(raw[key])
        except (ValueError, TypeError, KeyError, OverflowError):
            raise ValueError(f'{label}: enter a number, using a decimal point if needed.') from None
        if not math.isfinite(number):
            raise ValueError(f'{label}: enter a finite number.')
        positive = key in ('distance_km', 'speed_kmh', 'consumption_lph')
        if number < 0 or (positive and number == 0):
            raise ValueError(f'{label}: must be {"greater than zero" if positive else "zero or greater"}.')
        values[key] = number
    hours = values['distance_km'] / values['speed_kmh']
    trip = hours * values['consumption_lph']
    reserve = trip * (values['reserve_percent'] / 100)
    required = trip + reserve
    balance = values['available_l'] - required
    if not all(math.isfinite(n) for n in (hours, trip, reserve, required, balance)):
        raise ValueError('These values are too large to calculate. Enter smaller values.')
    if hours <= 0 or trip <= 0:
        raise ValueError('These values are too small to calculate reliably.')
    # Accommodate insignificant floating-point noise at exact equality.
    if math.isclose(values['available_l'], required, rel_tol=1e-12, abs_tol=0):
        balance = 0.0
    status = 'Shortfall' if balance < 0 else ('Exact requirement' if balance == 0 else 'Surplus')
    return {**values, 'duration_h': hours, 'trip_fuel_l': trip,
            'reserve_fuel_l': reserve, 'required_fuel_l': required,
            'balance_l': balance, 'status': status}


def export_csv(path, result):
    """Write one calculation snapshot with units encoded in column names."""
    record = {'saved_at': datetime.now().astimezone().isoformat(timespec='seconds'), **result}
    with Path(path).open('w', newline='', encoding='utf-8-sig') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(record))
        writer.writeheader()
        writer.writerow(record)


def display_number(value):
    if value and (abs(value) < 0.01 or abs(value) >= 1e9):
        return f'{value:.4g}'
    return f'{value:,.2f}'


def main():
    # Import GUI modules here so the calculation engine can be tested headlessly.
    try:
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
    except ImportError:
        raise SystemExit('Tkinter is missing. See README.md for Python/Tkinter installation instructions.')

    try:
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    except ImportError:
        raise SystemExit('Matplotlib is missing. Follow the setup steps in README.md.')

    class FuelApp:
        def __init__(self, root):
            self.root = root
            self.result = None
            root.title('Flight Fuel Estimator | CS-117')
            root.geometry('940x740')
            root.minsize(820, 690)
            style = ttk.Style(root)
            style.configure('Title.TLabel', font=('Arial', 20, 'bold'))
            style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
            outer = ttk.Frame(root, padding=20)
            outer.pack(fill='both', expand=True)
            ttk.Label(outer, text='Flight Fuel Estimator', style='Title.TLabel').pack(anchor='w')
            ttk.Label(outer, text='CS-117 Applications of ICT | Educational simulation').pack(anchor='w', pady=(4, 16))
            content = ttk.Frame(outer)
            content.pack(fill='x')
            content.columnconfigure(0, weight=1)
            content.columnconfigure(1, weight=1)
            inputs = ttk.LabelFrame(content, text='Flight inputs', padding=14)
            inputs.grid(row=0, column=0, sticky='nsew', padx=(0, 12))
            inputs.columnconfigure(1, weight=1)
            self.variables = {}
            for row, (key, label, default) in enumerate(FIELDS):
                ttk.Label(inputs, text=label).grid(row=row, column=0, sticky='w', pady=7, padx=(0, 12))
                variable = tk.StringVar(value=default)
                self.variables[key] = variable
                ttk.Entry(inputs, textvariable=variable, width=16).grid(row=row, column=1, sticky='ew', pady=7)
                variable.trace_add('write', self.invalidate)
            results = ttk.LabelFrame(content, text='Calculated results', padding=14)
            results.grid(row=0, column=1, sticky='nsew')
            self.outputs = {}
            for row, (key, label) in enumerate((('duration_h', 'Flight duration (hours)'), ('trip_fuel_l', 'Trip fuel (L)'), ('reserve_fuel_l', 'Reserve fuel (L)'), ('required_fuel_l', 'Total required (L)'), ('balance_l', 'Fuel balance (L)'))):
                ttk.Label(results, text=label).grid(row=row, column=0, sticky='w', pady=7, padx=(0, 20))
                self.outputs[key] = tk.StringVar(value='—')
                ttk.Label(results, textvariable=self.outputs[key], style='Header.TLabel').grid(row=row, column=1, sticky='e')
            buttons = ttk.Frame(outer)
            buttons.pack(fill='x', pady=14)
            ttk.Button(buttons, text='Calculate', command=self.run).pack(side='left', padx=(0, 8))
            ttk.Button(buttons, text='Load example', command=self.example).pack(side='left', padx=(0, 8))
            ttk.Button(buttons, text='Clear', command=self.clear).pack(side='left')
            self.save = ttk.Button(buttons, text='Export CSV', command=self.save_csv, state='disabled')
            self.save.pack(side='right')
            self.status = tk.StringVar(value='Enter values, then select Calculate.')
            ttk.Label(outer, textvariable=self.status, wraplength=850, style='Header.TLabel').pack(anchor='w', pady=(0, 8))
            self.figure = Figure(figsize=(7, 2.5), dpi=100, layout='constrained')
            self.axes = self.figure.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(self.figure, master=outer)
            self.canvas.get_tk_widget().pack(fill='both', expand=True)
            self.draw()
            ttk.Label(outer, text='Educational estimate only. Assumes constant speed and fuel consumption; excludes wind, weather, weight and flight phases. Reserve is user-defined. Not for actual flight planning.', wraplength=850).pack(anchor='w', pady=(12, 0))
            root.bind('<Return>', lambda event: self.run())

        def invalidate(self, *_):
            # Never export stale results after an input changes.
            self.result = None
            if hasattr(self, 'save'):
                self.save.configure(state='disabled')
                for output in self.outputs.values():
                    output.set('—')
                self.status.set('Inputs changed. Select Calculate to update the results.')
                self.draw()

        def run(self):
            self.invalidate()
            try:
                self.result = calculate({key: var.get() for key, var in self.variables.items()})
            except ValueError as error:
                self.status.set('Please correct the input values.')
                messagebox.showerror('Invalid input', str(error), parent=self.root)
                return
            for key, output in self.outputs.items():
                output.set(display_number(self.result[key]))
            balance = self.result['balance_l']
            if balance < 0:
                text = f'Shortfall: {display_number(-balance)} L additional fuel required under these assumptions.'
            elif balance == 0:
                text = 'Available fuel exactly meets the estimated requirement.'
            else:
                text = f'Surplus: {display_number(balance)} L above the estimated requirement.'
            self.status.set(text)
            self.save.configure(state='normal')
            self.draw()

        def example(self):
            for key, _, default in FIELDS:
                self.variables[key].set(default)
            self.run()

        def clear(self):
            for var in self.variables.values():
                var.set('')

        def draw(self):
            ax = self.axes
            ax.clear()
            if self.result is None:
                ax.set_axis_off()
                ax.text(0.5, 0.5, 'Calculate to compare required and available fuel.',
                        ha='center', va='center', transform=ax.transAxes)
            else:
                ax.set_axis_on()
                values = [self.result['required_fuel_l'], self.result['available_l']]
                bars = ax.barh(['Required', 'Available'], values, color=['#195b91', '#16877d'])
                ax.invert_yaxis()
                ax.set_xlabel('Fuel (litres)')
                ax.set_title('Required and available fuel')
                ax.set_xlim(left=0)
                ax.margins(x=0.25)
                ax.bar_label(bars, labels=[display_number(v) + ' L' for v in values], padding=5)
                ax.grid(axis='x', alpha=0.2)
                ax.set_axisbelow(True)
            self.canvas.draw_idle()

        def save_csv(self):
            if self.result is None:
                return
            path = filedialog.asksaveasfilename(parent=self.root, title='Save calculation', defaultextension='.csv', initialfile='flight_fuel_calculation.csv', filetypes=[('CSV file', '*.csv')])
            if not path:
                return
            try:
                export_csv(path, self.result)
            except OSError as error:
                messagebox.showerror('Could not save', f'Choose a writable folder and close the CSV in Excel if it is open.\n\n{error}', parent=self.root)
                return
            messagebox.showinfo('Saved', f'Calculation saved to:\n{path}', parent=self.root)

    try:
        root = tk.Tk()
    except tk.TclError as error:
        raise SystemExit(f'Cannot open the graphical interface: {error}\nRun on a desktop with Tkinter installed.')
    # Reject the obsolete macOS Tk version rather than showing a blank window.
    version = tuple(int(x) for x in root.tk.call('package', 'require', 'Tk').split('.')[:2])
    if version < (8, 6):
        root.destroy()
        raise SystemExit('Tk 8.6 or newer is required. Use the supplied launcher; see README.md.')
    FuelApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
