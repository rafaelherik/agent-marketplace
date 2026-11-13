#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
VERSION=$(cat "$ROOT/.github/agent-marketplace-version")
DEST=${1:?Usage: bash scripts/install-cli.sh /absolute/bin/directory}
case "$(uname -s)" in
  Darwin) OS=darwin ;;
  Linux) OS=linux ;;
  *) echo 'Only macOS and Linux are supported.' >&2; exit 1 ;;
esac
case "$(uname -m)" in
  arm64|aarch64) ARCH=arm64 ;;
  x86_64|amd64) ARCH=amd64 ;;
  *) echo 'Unsupported CPU architecture.' >&2; exit 1 ;;
esac

ASSET="agent-marketplace-${VERSION}-${OS}-${ARCH}"
BASE="https://github.com/Adyen/agent-marketplace/releases/download/${VERSION}"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
curl --fail --silent --show-error --location "$BASE/$ASSET" -o "$WORK/$ASSET"
curl --fail --silent --show-error --location "$BASE/SHA256SUMS" -o "$WORK/SHA256SUMS"
(
  cd "$WORK"
  awk -v asset="$ASSET" '$2 == asset { print; found = 1 } END { if (!found) exit 1 }' SHA256SUMS > selected.sha256
  if command -v sha256sum >/dev/null; then
    sha256sum --check selected.sha256
  else
    shasum -a 256 --check selected.sha256
  fi
)
mkdir -p "$DEST"
install -m 755 "$WORK/$ASSET" "$DEST/agent-marketplace"
"$DEST/agent-marketplace" --version
