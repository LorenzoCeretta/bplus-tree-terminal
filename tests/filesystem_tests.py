from commands import VirtualFileSystem

# To test it, run python3 -m tests.filesystem_tests

# Sixth Test - Testing all filesystem features

fs = VirtualFileSystem()

print("--- Testing mkdir and ls ---")
print("mkdir projects")
print(fs.mkdir("projects"))

print("\nmkdir documents")
print(fs.mkdir("documents"))

print("\nls")
print(fs.ls())

print("\n--- Testing cd ---")
print("cd projects")
print(fs.cd("projects"))

print("\ncd ..")
print(fs.cd(".."))

print("\ncd /")
print(fs.cd("/"))

print("\ncd")
print(fs.cd())

print("\n--- Testing nested directories ---")
print("cd projects")
print(fs.cd("projects"))

print("\nmkdir python")
print(fs.mkdir("python"))

print("\ncd python")
print(fs.cd("python"))

print("\nls")
print(fs.ls())

print("\n--- Testing file operations ---")
print("touch test.txt")
print(fs.touch("test.txt"))

print("\ntouch example.py")
print(fs.touch("example.py"))

print("\nls")
print(fs.ls())

print("\n--- Testing rm ---")
print("rm test.txt")
print(fs.rm("test.txt"))

print("\nls")
print(fs.ls())

print("\n--- Testing error cases ---")
print("cd /projects")
print(fs.cd("/projects"))

print("\nmkdir python")  # Try to create existing directory
print(fs.mkdir("python"))

print("\ncd nonexistent")  # Directory doesn't exist
print(fs.cd("nonexistent"))

print("\nrm nonexistent.txt")  # File doesn't exist
print(fs.rm("nonexistent.txt"))
