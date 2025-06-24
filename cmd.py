from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Static
from commands import VirtualFileSystem

# To exit the shell interface, just type "exit"


class BPlusTreeShell(App):
    CSS_PATH = None  # No custom CSS, minimal
    BINDINGS = [("ctrl+c", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Static("B+ Tree Virtual Filesystem", id="header")
        yield Static("", id="output", expand=True)
        yield Input(placeholder="Digite um comando...", id="input")
        yield Static(f"CWD: /", id="cwd")

    def on_mount(self):
        self.vfs = VirtualFileSystem()
        self.output = self.query_one("#output", Static)
        self.input = self.query_one("#input", Input)
        self.cwd_label = self.query_one("#cwd", Static)
        self.prompt()

    def prompt(self, text=""):
        self.output.update(f"{self.vfs.cwd}$ {text}")

    async def on_input_submitted(self, event: Input.Submitted):
        cmd = event.value.strip()
        if not cmd:
            return
        args = cmd.split()
        op = args[0]
        params = args[1:]
        output = ""

        if op == "mkdir" and params:
            output = self.vfs.mkdir(params[0])
        elif op == "ls":
            output = self.vfs.ls(params[0] if params else None)
        elif op == "cd" and params:
            output = self.vfs.cd(params[0])
        elif op == "touch" and params:
            output = self.vfs.touch(params[0])
        elif op == "rm" and params:
            output = self.vfs.rm(params[0])
        elif op == "exit":
            await self.action_quit()
            return
        else:
            output = f"Unknown or incomplete command: {cmd}"

        # Update the output and cwd
        self.output.update(f"{self.vfs.cwd}$ {cmd}\n{output}")
        self.cwd_label.update(f"CWD: {self.vfs.cwd}")
        self.input.value = ""


if __name__ == "__main__":
    BPlusTreeShell().run()
