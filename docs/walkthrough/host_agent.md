# Host agent walkthrough

`host_agent.py` accepts typed frames, checks an exact verb allow-list, maps project IDs to fixed repository paths, and returns status frames. It does not invoke a shell. A future ngspice adapter must use an argv list and a fixed executable path, with tests covering path traversal and injected arguments.

Viva questions: Why IDs instead of paths? To prevent traversal. Why no shell? It prevents command injection. Why confirmation? Risky actions need a physical user signal. How are projects selected? A closed registry. What is currently measured? Only virtual protocol success; simulation metrics remain TARGET.
