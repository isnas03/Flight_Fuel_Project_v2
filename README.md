# Flight Fuel Estimation and Analysis System — START HERE

A beginner-friendly Python project for CS-117 Applications of ICT.
This version uses **Tkinter for the application window and Matplotlib for the chart**.

## 1. What you need

- A supported Windows 10/11 64-bit PC, a supported Intel/Apple Silicon Mac, or a Linux desktop supported by the installer below.
- Internet for first-time installation. The calculator works offline afterwards.
- Permission to install software and several GB of free disk space for the Python environment.
- Cursor is optional: it lets you read/edit code and run commands. It does not install Python or Tkinter for you.

This is Python source code, not an EXE. Setup is required on each computer. No application can be guaranteed to work on literally every laptop; unsupported older operating systems, restricted school PCs and headless servers may need additional help. Windows ARM is not covered by this beginner setup.

**Use the supplied setup and run scripts. Do not launch with a generic `python` or `python3` command:** it may select an older Python installed by Apple, pyenv, Homebrew or another environment. The run scripts select this project's Python by its exact path.

## 2. Extract and place the project

1. Download the ZIP and copy it to the destination computer.
2. Windows: right-click the ZIP > Extract All. Mac: double-click the ZIP. Linux: use your archive manager's Extract option.
3. Open the extracted **Flight_Fuel_Project_v2** folder. You should see `fuel_calculator.py`, this README and the setup scripts.
4. Keep it in a permanent local folder with a short path, preferably without spaces. Avoid running inside the ZIP or placing it in a synced/network folder.
5. Choose the operating-system instructions below. Run commands one at a time. Do not type the terminal prompt, `(base)`, `$`, `%` or the Markdown backticks.

## 3. Install Conda once

If `conda --version` already prints a version, skip installing another copy and go to Step 4.

Otherwise, install **Miniforge**, which provides Conda. You do not need to install Python separately: the project setup installs Python, Tk and Matplotlib together.

Official download: https://conda-forge.org/download/
Detailed installer instructions: https://github.com/conda-forge/miniforge

### Windows

1. Choose Windows x86_64 and download the `.exe` installer.
2. Run it and complete installation for your user. Default options are appropriate; you do not need to add it globally to PATH.
3. Open **Miniforge Prompt** from the Start menu. Use this prompt for the first setup; a normal Cursor terminal may not yet know the conda command.
4. Type `conda --version` and press Enter. A version should appear.

### Mac

1. Open Apple menu > About This Mac. If Chip says Apple M1/M2/M3/M4 or another Apple chip, choose **arm64 / Apple Silicon**. If it says Intel, choose **x86_64 / Intel**.
2. Download the matching Miniforge installer from the official page. Use the `.pkg` installer when offered and follow its instructions.
3. If you downloaded a `.sh` installer instead: open Terminal, type `bash ` (including the space), drag the downloaded `.sh` file into Terminal and press Enter. Review the license, accept it if you agree, use the suggested installation location and allow shell initialization when prompted.
4. Close and reopen Terminal/Cursor after installation. Run `conda --version`.
5. If Conda is still not found, use the installer-provided terminal initialization instructions. For a default installation in your home folder, this temporary fix is usually sufficient:

```bash
export PATH="$HOME/miniforge3/bin:$PATH"
conda --version
```

Only use that path if you installed Miniforge there. An existing Anaconda/Miniconda installation can be used instead.

### Linux desktop

1. In Terminal run `uname -m`: `x86_64` means choose Linux x86_64; `aarch64` means choose Linux aarch64.
2. Download the matching `.sh` installer from the official Miniforge page.
3. In Terminal, type `bash `, followed by the full path to the downloaded installer. Press Enter and follow its prompts, including shell initialization.
4. Reopen the terminal and run `conda --version`.
5. A graphical desktop is required. Do not use a headless SSH session or plain WSL for this beginner setup.

## 4. First-time project setup

### Windows

In **Miniforge Prompt**, move into the project folder. Replace the example path with your actual folder path:

```bat
cd /d "C:\Users\YourName\Documents\Flight_Fuel_Project_v2"
```

Then run:

```bat
setup_windows.bat
```

Wait for **Setup complete**. Package downloads and solving may take several minutes. Do not run the app while setup is still in progress. If setup reports an error, read the troubleshooting section rather than continuing.

### Mac or Linux

Open Terminal, type `cd ` (with a space), drag the extracted project folder into Terminal, and press Enter. On Linux you can also use your file manager's Open in Terminal option.

Then run:

```bash
bash setup_mac_linux.sh
```

Wait for **Setup complete**. Do not close the terminal during installation.

### What setup does

It creates a separate environment inside the project's `.runtime` folder, containing Python 3.12, Tk 8.6+ (below 9), Matplotlib 3.8+ (below 4), and dependencies from conda-forge. It does not change your application code or replace your other Python environments. Rerunning setup updates/repairs the project environment within those version ranges. Exact dependency builds can differ between computers.

## 5. Start the calculator

### Windows

Double-click **run_windows.bat**. Or run it in a terminal:

```bat
run_windows.bat
```

In Cursor's PowerShell terminal, use:

```powershell
.\run_windows.bat
```

### Mac or Linux

From the project folder:

```bash
bash run_mac_linux.sh
```

No `conda activate` is needed. The launcher uses the exact Python inside `.runtime` and avoids the pyenv conflict encountered on Mac. Leave the terminal open while using the application. Close the calculator window to exit normally.

**Every subsequent run needs only this step, not a new installation.**

## 6. Use the project in Cursor

1. Install/open Cursor if desired: https://cursor.com/
2. Select **File > Open Folder** and choose the extracted `Flight_Fuel_Project_v2` folder.
3. Open `README.md` to read the instructions. Open `fuel_calculator.py` to inspect the code.
4. Open a terminal in Cursor. Confirm it is in the folder containing the scripts.
5. If setup has already succeeded, run `bash run_mac_linux.sh` on Mac/Linux or `.\run_windows.bat` on Windows PowerShell.
6. If you have not completed setup, follow Step 4 first. On Windows, Miniforge Prompt is the simplest place to run setup if Cursor says Conda is not found.
7. Avoid a generic editor Run button unless you have explicitly selected the interpreter below. The supplied launchers are the recommended method.

Optional interpreter paths for Cursor's Python tooling:
- Windows: `<project folder>\.runtime\python.exe`
- Mac/Linux: `<project folder>/.runtime/bin/python`

## 7. Use and verify the application

Click **Load example**. You should see:

| Item | Value |
|---|---:|
| Distance | 600 km |
| Speed | 300 km/h |
| Consumption | 80 L/hour |
| Reserve | 15% |
| Available fuel | 200 L |
| Duration | 2 hours |
| Trip fuel | 160 L |
| Reserve fuel | 24 L |
| Total required | 184 L |
| Surplus | 16 L |

The Matplotlib chart compares **Required: 184 L** and **Available: 200 L**, starting at zero.

- **Calculate** (or Enter): validate inputs and update results/chart.
- **Load example**: restore and calculate the example.
- **Clear**: empty the inputs and results.
- **Export CSV**: choose a location and filename. Saves one calculation with inputs, results, status and timestamp. Open the CSV with Excel or another spreadsheet app. It does not append to a history file.
- Changing an input clears previous results/chart and disables export until you recalculate.
- Use decimal points, not commas or units, in input fields.

Before presenting, check: example, available fuel 100 (84 L shortfall), available fuel 184 (exact), zero speed (error), Clear, chart resize and CSV export. Verify the saved CSV matches the displayed calculation.

## 8. Troubleshooting

### Mac warning about system Tk, a blank window, or Tk 8.5.9

This normally means the wrong Python is running. In the earlier setup, `conda run ... python` unexpectedly resolved to `/Users/admin/.pyenv/...`, so merely naming an environment did not solve the problem.

Use **`bash run_mac_linux.sh`**, not `python3 fuel_calculator.py` and not the previous named flightfuel command. This version checks for Tk 8.6+ and stops with guidance if it finds older Tk. Suppressing the warning does not upgrade Tk.

### Conda command not found

- Windows: open Miniforge Prompt and run setup there.
- Mac/Linux: reopen the terminal after installation and follow Step 3's initialization instructions.
- Installing Cursor alone does not install Conda.

### No module named matplotlib / tkinter or cannot find .runtime Python

The setup did not finish, or you used the wrong interpreter. Rerun the appropriate setup script, wait for success and use the run script. Tkinter is provided by the Tk/Python packages; do not run `pip install tkinter`.

### Setup remains on collecting metadata / solving

Initial downloads can be slow. Keep your internet connected. If there is no progress for a prolonged period, press Ctrl+C, retain the error/output and retry setup. If it fails again, send the full output to the person helping you. Do not disable SSL verification or security software as a workaround.

### You moved or renamed the folder after setup

Conda environments contain absolute paths and should not be moved between folders/computers. Keep the project in its original location. If it was moved, close the app, delete ONLY the generated `.runtime` subfolder in this project, and rerun setup. Do not delete your global Python/Conda folders. Transfer the original ZIP, not an installed environment, to another computer.

### Mac/Linux Permission denied on a script

Use `bash run_mac_linux.sh` or `bash setup_mac_linux.sh` exactly as shown; executable permissions are not needed with this method.

### Windows DLL load error

Use `run_windows.bat`, which adds the project's DLL directories. If it persists, rerun setup. Confirm your OS/CPU matches the Miniforge installer and send the complete error if needed.

### CSV cannot be saved

Close the existing file in Excel, choose a writable folder such as Documents, then retry. Cancelling the save dialog is harmless.

### Window appears but is behind Cursor

Use the Dock/taskbar or switch applications to select Flight Fuel Estimator. On small screens, maximize the window; a display of roughly 1024x768 or larger is preferable.

## 9. Diagnostic check

If setup succeeds but the GUI is still broken, run the check using this project's interpreter.

Mac/Linux:

```bash
./.runtime/bin/python -E -s check_setup.py
```

Windows, in Miniforge Prompt (or Command Prompt with conda available):

```bat
call conda activate "%CD%\.runtime"
"%CD%\.runtime\python.exe" -E -s check_setup.py
```

This prints the interpreter path, Tk and Matplotlib versions, then displays a two-bar test chart. Close it to finish. If you ask for help, send the complete printed output and a screenshot of the chart/window. The Python path should point inside THIS project's `.runtime`, not `.pyenv` or `/usr/bin`.

## 10. Automated tests

Mac/Linux:

```bash
./.runtime/bin/python -E -s -m unittest -v
```

Windows Command Prompt:

```bat
".runtime\python.exe" -E -s -m unittest -v
```

Windows PowerShell:

```powershell
& .\.runtime\python.exe -E -s -m unittest -v
```

Six calculation/export tests pass in the development environment. They cover the worked example, shortfall/exact fuel, zero reserve, invalid inputs, overflow and CSV content. Syntax checks also cover the Python files and Unix scripts. This release has not been interactively verified on every operating system; the manual checks in Step 7 and the diagnostic chart are required on the destination computer before presenting.

## 11. How the code works

- `calculate()`: validates finite numeric inputs and computes duration, trip/reserve/total fuel and balance.
- `export_csv()`: saves one complete calculation snapshot.
- `main()` / `FuelApp`: builds the Tkinter window, handles buttons and embeds a Matplotlib figure through FigureCanvasTkAgg.
- `draw()`: updates the fuel comparison bars; clears them after inputs change.

Formulae:

Duration = distance / speed
Trip fuel = duration * hourly consumption
Reserve fuel = trip fuel * reserve percentage / 100
Total required = trip fuel + reserve fuel
Balance = available fuel - total required

Positive distance, speed and consumption are required; reserve and available fuel may be zero. Display values are usually rounded to two decimal places, while calculations and CSV retain floating-point precision. A relative tolerance of 1e-12 handles numerical noise at equality.

## 12. Files included

- README.md and START_HERE.txt: these setup instructions and quick-start pointer.
- fuel_calculator.py: application source.
- setup_windows.bat / run_windows.bat: Windows setup and launcher.
- setup_mac_linux.sh / run_mac_linux.sh: Mac/Linux setup and launcher.
- check_setup.py: dependency and visual diagnostic.
- test_calculator.py: automated tests.
- requirements.txt: Matplotlib requirement for experienced users with an existing compatible Python/Tk installation. Beginners should use the setup scripts.

## 13. Project scope

Educational simulation only. Assumes constant average speed and consumption, with a user-defined reserve. Does not account for wind, weather, weight, flight phases, certified performance or operational fuel requirements. Not for actual flight planning. Students should understand the source and explain the assumptions during the presentation.

## Official references

- Miniforge download: https://conda-forge.org/download/
- Miniforge installation: https://github.com/conda-forge/miniforge
- Conda environment paths: https://docs.conda.io/projects/conda/en/stable/commands/create.html
- Tkinter: https://docs.python.org/3/library/tkinter.html
- Matplotlib embedded in Tk: https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
