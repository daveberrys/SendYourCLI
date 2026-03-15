import os
import src.print as print
from InquirerPy import inquirer
from src.sendFile import buzzheavier, catbox, litterbox

maxSizes = {
    "Catbox": 200 * 1024 * 1024,
    "Litterbox": 1024 * 1024 * 1024,
    "Buzzheavier": None,
}

provider = inquirer.select(
    message="What Provider?",
    choices=["Catbox", "Litterbox", "Buzzheavier"],
).execute()

limit = None
if provider == "Litterbox":
    limit = inquirer.select(
        message="How many hours?",
        choices=["1h", "12h", "24h", "72h"],
    ).execute()
    
file = inquirer.filepath(
    message="Select a file",
    default="",
).execute()

file = file.strip()
if (
    len(file) >= 2
    and ((file[0] == file[-1]) and file[0] in ("'", '"'))
):
    file = file[1:-1].strip()
file = os.path.expanduser(file)
file = os.path.abspath(file)

if file == "":
    print.warning("  No file selected. Exiting...")
    exit()
if not os.path.isfile(file):
    print.warning("Selected path is not a file. Exiting...")
    exit()
else:
    maxSize = maxSizes.get(provider)
    fileSize = os.path.getsize(file)
    if maxSize is not None and fileSize > maxSize:
        sizeMb = fileSize / (1024 * 1024)
        maxMb = maxSize / (1024 * 1024)
        print.error(
            f"  Selected file is {sizeMb:.2f} MB, which exceeds {provider}'s "
            f"  limit of {maxMb:.0f} MB. Exiting..."
        )
        exit()

    confirm = inquirer.confirm(
        message=f"""You are about to upload {file} to {provider}.
  Are you sure you want to proceed?""",
    ).execute()
    
    if confirm == True:
        print.log(f"Uploading {file} to {provider}...")
        if provider == "Catbox":
            result = catbox(file)
        elif provider == "Litterbox":
            result = litterbox(file, duration=limit or "1h")
        elif provider == "Buzzheavier":
            result = buzzheavier(file)
        else:
            result = "Error: Unknown provider."
            print.error(result)
            exit()

        print.success(result)
    else:
        print.log("Upload cancelled.")
