import os.path
import pathlib
import platform
import subprocess
import time

try:
    import win32api
    WINDOWS = True
except ImportError:
    WINDOWS = False

PLATFORM = platform.system()

if PLATFORM == "Darwin":
    MACOS = True
else:
    MACOS = False


if WINDOWS:
    JLINK_PATH = "C:\Program Files (x86)\SEGGER\JLink\JLink.exe"
elif MACOS:
    JLINK_PATH = "JlinkExe"


def _find_drive_by_name_windows(name):
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for drive in drives:
        info = win32api.GetVolumeInformation(drive)
        if info[0] == name:
            return drive
    raise RuntimeError(f"No drive {name} found.")


def _find_drive_by_name_macos(name):
    drive = os.path.join(f"/Volumes/{name}")
    if os.path.exists(drive):
        return drive
    raise RuntimeError(f"No drive {name} found, expected at {drive}.")


def find_drive_by_name(name):
    if WINDOWS:
        return _find_drive_by_name_windows(name)
    elif MACOS:
        return _find_drive_by_name_macos(name)
    else:
        raise EnvironmentError("Idk what platform I'm running on.")


def wait_for_drive(name, timeout=10):
    for n in range(timeout):
        try:
            path = find_drive_by_name(name)
            if n > 1:
                # Wait a second because the drive may not be fully mounted.
                time.sleep(1)
            return path
        except RuntimeError:
            time.sleep(1)
            pass
    
    raise RuntimeError(f"Drive {path} never showed up.")

def flush(path):
    if WINDOWS:
        drive, _ = os.path.splitdrive(path)
        subprocess.run(["sync", drive], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif MACOS:
        mountpoint = os.path.join(os.path.join(*os.path.split(path)[:2]))
        fd = os.open(mountpoint, os.O_RDONLY)
        os.fsync(fd)
        os.close(fd)


def unmount(path):
    if WINDOWS:
        pass
    elif MACOS:
        disk = None
        mount_output = subprocess.check_output(["mount"]).decode("utf-8").splitlines()

        for line in mount_output:
            items = line.split(" ")
            if items[2] == path:
                disk = items[0].split("/").pop()
                break
        
        if disk is None:
            print(f"Warning: unable to find device for {path}")
            return

        subprocess.check_output(["diskutil", "unmount", disk])


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