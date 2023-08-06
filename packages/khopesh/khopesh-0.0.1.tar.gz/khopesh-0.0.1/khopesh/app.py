from chuda import App, autorun, Parameter
from argparse import REMAINDER
import sh
import sys
import os
from pathlib import Path
import importlib.util
import stat


@autorun()
class KhopeshApp(App):

    arguments = [
        Parameter("executable"),
        Parameter("everything", nargs=REMAINDER)
    ]

    def filter_command_name(self, string):
        return not (string.startswith("-") or string.startswith(".") or string.startswith("/"))

    def make_executable(self, file):
        st = os.stat(file)
        os.chmod(file, st.st_mode | stat.S_IEXEC)

    def get_hooks(self, command_name):
        hooks_folder = Path(f"./hooks/{self.arguments.executable}")

        hooks = {}
        if hooks_folder.is_dir():
            pre_hook_sh = (hooks_folder / f"pre-{command_name}-hook.sh")
            pre_hook_py = (hooks_folder / f"pre-{command_name}-hook.py")
            post_hook_sh = (hooks_folder / f"post-{command_name}-hook.sh")
            post_hook_py = (hooks_folder / f"post-{command_name}-hook.py")

            if pre_hook_sh.is_file() and not pre_hook_py.is_file():
                self.make_executable(pre_hook_sh)
                hooks["pre"] = {"type": "sh", "path": pre_hook_sh}

            if pre_hook_py.is_file():
                hooks["pre"] = {"type": "py", "path": pre_hook_py}

            if post_hook_sh.is_file() and not post_hook_py.is_file():
                self.make_executable(post_hook_sh)
                hooks["post"] = {"type": "sh", "path": post_hook_sh}

            if post_hook_py.is_file():
                hooks["post"] = {"type": "py", "path": post_hook_py}

        return hooks

    def exec_hook(self, hook):
        if hook["type"] == "sh":
            sh.Command(hook["path"])(_out=sys.stdout, _err=sys.stderr)

        if hook["type"] == "py":
            module_name = hook["path"].stem.replace("-", "_")
            spec = importlib.util.spec_from_file_location(module_name, str(hook["path"]))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.hook()

    def main(self):
        try:
            executable = sh.Command(self.arguments.executable)
            potential_commands = [arg for arg in self.arguments.everything if self.filter_command_name(arg)]

            command_name = None
            if len(potential_commands) >= 1:
                command_name = potential_commands[0]

            hooks = self.get_hooks(command_name)

            if hooks.get("pre", None):
                self.exec_hook(hooks["pre"])

            executable(self.arguments.everything, _out=sys.stdout, _err=sys.stderr)

            if hooks.get("post", None):
                self.exec_hook(hooks["post"])

        except sh.ErrorReturnCode as exc:
            sys.stdout.write(exc.stdout.decode("UTF-8"))
            sys.stderr.write(exc.stderr.decode("UTF-8"))

        except sh.CommandNotFound:
            self.logger.error(f"{self.arguments.executable} not found")
