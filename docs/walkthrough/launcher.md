# Launcher walkthrough

`host/launcher.py` maps an already validated project directory to a platform opener. It returns an argv list on Linux/macOS and uses `os.startfile` on Windows; no shell string is constructed. Virtual mode uses dry-run behavior, while real mode is only reached through the host agent after project validation.

Viva questions: Why validate before launching? To enforce the project registry. Why no shell? To prevent command injection. Why dry-run? CI must not launch desktop apps. What is fixed? The executable and one resolved project path. What does the test cover? Platform command shape and traversal-safe registry use.
