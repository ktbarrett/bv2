major = "0"
minor = "0"
patch = "0"
release = "dev0"

if release != "":
    __version__ = f"{major}.{minor}.{patch}.{release}"
else:
    __version__ = f"{major}.{minor}.{patch}"
