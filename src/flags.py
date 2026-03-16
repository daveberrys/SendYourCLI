import argparse
import os

import src.print as print
from src.sendFile import buzzheavier, catbox, litterbox

maxSizes = {
    "Catbox": 200 * 1024 * 1024,
    "Litterbox": 1024 * 1024 * 1024,
    "Buzzheavier": None,
}
providerMap = {
    "catbox": "Catbox",
    "litterbox": "Litterbox",
    "buzzheavier": "Buzzheavier",
}
validDurations = {"1h", "12h", "24h", "72h"}

def normalizeFile(path):
    path = path.strip()
    if len(path) >= 2 and ((path[0] == path[-1]) and path[0] in ("'", '"')):
        path = path[1:-1].strip()
    path = os.path.expanduser(path)
    return os.path.abspath(path)

def runFlags(argv):
    parser = argparse.ArgumentParser(
        prog="SendYourCLI",
        description="Upload a file via CLI flags.",
    )
    parser.add_argument(
        "--provider",
        required=True,
        choices=sorted(providerMap.keys()),
        help="Upload provider (catbox, litterbox, buzzheavier).",
    )
    parser.add_argument(
        "--file",
        required=True,
        help="File path to upload.",
    )
    parser.add_argument(
        "--duration",
        default="1h",
        help="Litterbox duration: 1h, 12h, 24h, 72h.",
    )

    args = parser.parse_args(argv)

    provider = providerMap[args.provider]
    filePath = normalizeFile(args.file)

    if filePath == "":
        print.warning("No file selected. Exiting...")
        return
    if not os.path.isfile(filePath):
        print.warning("Selected path is not a file. Exiting...")
        return

    if provider == "Litterbox" and args.duration not in validDurations:
        print.error("Invalid duration. Use: 1h, 12h, 24h, 72h.")
        return
    if provider != "Litterbox" and args.duration != "1h":
        print.warning("Duration is only used for Litterbox. Ignoring.")

    maxSize = maxSizes.get(provider)
    fileSize = os.path.getsize(filePath)
    if maxSize is not None and fileSize > maxSize:
        sizeMb = fileSize / (1024 * 1024)
        maxMb = maxSize / (1024 * 1024)
        print.error(
            f"Selected file is {sizeMb:.2f} MB, which exceeds {provider}'s "
            f"limit of {maxMb:.0f} MB. Exiting..."
        )
        return

    print.log(f"Uploading {filePath} to {provider}...")
    if provider == "Catbox":
        result = catbox(filePath)
    elif provider == "Litterbox":
        result = litterbox(filePath, duration=args.duration)
    elif provider == "Buzzheavier":
        result = buzzheavier(filePath)
    else:
        result = "Error: Unknown provider."
        print.error(result)
        return

    print.success(result)