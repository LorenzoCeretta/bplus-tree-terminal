from bplus_tree import BPlusTree

class VirtualFileSystem:
    def __init__(self, order=4):
        self.tree = BPlusTree(order)
        self.cwd = "/"
        self.tree.insert("/", {"type": "dir"})

    def mkdir(self, name):
        path = self.__full__path(name)
        if self.tree.search_value(path):
            return f"Directory '{name}' already exists"
        self.tree.insert(path, {"type": "dir"})
        return f"Directory '{name}' created"

    def ls(self, path=None):
        if not path:
            path = self.cwd
        node = self.tree.search(path)
        if not node:
            return f"No such directory: {path}"
        # Shows the keys of the node (for simplicity)
        if hasattr(node, "keys"):
            return " ".join(node.keys) if node.keys else "[empty]"
        return "[unknown node]"

    def cd(self, path):
        if path == "..":
            if self.cwd == "/":
                return "Already at root directory"
            self.cwd = "/".join(self.cwd.rstrip("/").split("/")[:-1])
            if not self.cwd:
                self.cwd = "/"
            return f"Moved to {self.cwd}"
            
        path = self.__full__path(path)
        val = self.tree.search_value(path)
        if val and val.get("type") == "dir":
            self.cwd = path
            return f"Moved to {path}"
        else:
            return f"No such directory: {path}"

    def __full__path(self, name):
        if name.startswith("/"):
            return name.rstrip("/")
        if self.cwd == "/":
            return "/" + name.rstrip("/")
        return self.cwd.rstrip("/") + "/" + name.rstrip("/")
