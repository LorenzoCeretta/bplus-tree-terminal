from commands import VirtualFileSystem


def create_sample_filesystem():
    """Create a filesystem for visualization"""

    vfs = VirtualFileSystem(order=4)

    vfs.mkdir("houses")
    vfs.cd("houses")

    vfs.mkdir("stark")
    vfs.cd("stark")
    vfs.touch("ned.txt")
    vfs.touch("jon_snow.txt")
    vfs.touch("arya.txt")

    vfs.cd("/houses")

    vfs.mkdir("lannister")
    vfs.cd("lannister")
    vfs.touch("cersei.txt")
    vfs.touch("jaime.txt")
    vfs.touch("tyrion.txt")


    vfs.cd("/")
    print("Filesystem ready")
    return vfs


if __name__ == "__main__":
    fs = create_sample_filesystem()
    print("\nFilesystem structure:")
    fs.tree.visualization()
