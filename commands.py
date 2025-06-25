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

        path = path.rstrip("/")
        if not path:
            path = "/"

        if not self.tree.search_value(path):
            return f"No such directory: {path}"

        # Get all paths and filter children
        contents = []
        prefix = path if path == "/" else path + "/"

        for key in self.tree.get_all_leaf_keys():
            if key != path and key.startswith(prefix):
                name = key.split("/")[-1]
                if name:
                    # Check if it's a directory
                    item_type = self.tree.search_value(key).get("type")
                    if item_type == "dir":
                        name = name + "/"
                    contents.append(name)

        return " ".join(contents) if contents else "[empty]"

    def cd(self, path=None):
        if not path:
            self.cwd = "/"
            return "Moved to the root directory"

        if path == "..":
            if self.cwd == "/":
                return "Already at root directory"
            self.cwd = "/".join(self.cwd.rstrip("/").split("/")[:-1])
            if not self.cwd:
                self.cwd = "/"
            return f"Moved to {self.cwd}"

        if path == "/":
            self.cwd = "/"
            return "Moved to the root directory"

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

    def touch(self, name):
        path = self.__full__path(name)
        if self.tree.search_value(path):
            return f"File '{name}' already exists"
        self.tree.insert(path, {"type": "file"})
        return f"File '{name}' created"

    def rm(self, name):
        path = self.__full__path(name)
        if self.tree.search_value(path):
            self.tree.delete(path)
            return f"File '{name}' deleted"
        else:
            return f"File '{name}' does not exist"
