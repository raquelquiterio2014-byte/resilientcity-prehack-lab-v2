# ResilientCity AI — Pre-Hackathon Learning Lab
Disposable learning environment, not the competition implementation.

## Run on Windows
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
python -m pytest -q

## Desktop graphical interface

A Tkinter desktop interface is available in `gui.py`.

Windows quick start:

```bat
run_gui.bat
```

Or manually:

```bash
python gui.py
```

The GUI accepts incident data and displays the final recommendation, confidence, safety/human-review status, complete agent trace, and shared workflow state.

## Web demo

`web/index.html` is a self-contained page (open it in any browser, no install) that reproduces the same deterministic agent rules in JavaScript, with example scenarios, the agent workflow, the execution trace and the final report.

Photos in the web demo come from Wikimedia Commons, used under their licenses (CC BY 4.0, CC BY-SA 2.0, CC BY 2.0, CC0); authors and links are credited in the page footer.
