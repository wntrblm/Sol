import os.path
import pathlib
import win32api
import subprocess

def find_drive_by_name(name):
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for drive in drives:
        info = win32api.GetVolumeInformation(drive)
        if info[0] == name:
            return drive
    raise RuntimeError(f"No drive {name} found.")


def flush(path):
    drive, _ = os.path.splitdrive(path)
    subprocess.run(["sync", drive], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def copyfile(src, dst):
    # shutil can be a little wonky, so do this manually.
    with open(src, "rb") as fh:
        contents = fh.read()

    with open(dst, "wb") as fh:
        fh.write(contents)
        fh.flush()

    flush(dst)

def clean_pycache(root):
    for p in pathlib.Path(root).rglob('*.py[co]'):
        p.unlink()
    for p in pathlib.Path(root).rglob('__pycache__'):
        p.rmdir()