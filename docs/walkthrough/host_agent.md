# Host agent walkthrough

`host/intent_nlu.py` maps only a closed set of supported phrases to typed frames. `host_agent.py` then checks an exact verb allow-list, maps project IDs to fixed repository paths, and returns status frames. It does not invoke a shell. The ngspice adapter uses an argv list and a fixed executable name, with tests covering path traversal and injected arguments.

Viva questions: Why IDs instead of paths? To prevent traversal. Why no shell? It prevents command injection. Why confirmation? Risky actions need a physical user signal. How are projects selected? A closed registry. What is currently measured? Only virtual protocol success; simulation metrics remain TARGET.
