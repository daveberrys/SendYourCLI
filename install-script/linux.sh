#!/usr/bin/env sh
set -eu

url="${URL:-https://nightly.link/daveberrys/SendYourCLI/workflows/main/main/SendYourCLI-Linux.zip}"
installDir="${INSTALL_DIR:-$HOME/.local/bin}"
binName="${BIN_NAME:-syc}"

need_cmd() {
  command -v "$1" >/dev/null 2>&1
}

if ! need_cmd curl; then
  echo "Error: curl is required." >&2
  exit 1
fi

if ! need_cmd unzip; then
  echo "Error: unzip is required." >&2
  exit 1
fi

tmpDir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmpDir"
}
trap cleanup EXIT

zipPath="$tmpDir/SendYourCLI-Linux.zip"
echo "Downloading SendYourCLI..."
curl -fsSL "$url" -o "$zipPath"

unzip -q "$zipPath" -d "$tmpDir"

binPath="$(find "$tmpDir" -maxdepth 2 -type f -name 'SendYourCLI*' | head -n 1)"
if [ -z "$binPath" ]; then
  echo "Error: Could not find extracted binary." >&2
  exit 1
fi

mkdir -p "$installDir"
installPath="$installDir/$binName"
cp "$binPath" "$installPath"
chmod +x "$installPath"

echo "Installed to $installPath"
echo "Make sure $installDir is on your PATH."
