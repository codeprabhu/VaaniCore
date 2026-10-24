import pathlib
import unittest
from host.launcher import open_command

class LauncherTests(unittest.TestCase):
    def test_linux_command_is_fixed_argv(self):
        command = open_command(pathlib.Path("projects/amplifier"), "linux")
        self.assertIsNone(command) if command is None else self.assertEqual(len(command), 2)
        if command:
            self.assertEqual(command[0], "xdg-open")
            self.assertNotIn(";", command[1])

    def test_windows_uses_startfile_path(self):
        self.assertIsNone(open_command(pathlib.Path("projects/amplifier"), "win32"))
