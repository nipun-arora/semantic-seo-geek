#!/bin/sh
set -eu

usage() {
  echo "Usage: scripts/sync-public.sh [--apply] EXPORT_DIR DESTINATION" >&2
  exit 2
}

apply=false
if [ "${1:-}" = "--apply" ]; then
  apply=true
  shift
fi
[ "$#" -eq 2 ] || usage

export_directory=$1
destination=$2
script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)

[ -d "$export_directory" ] || {
  echo "Export directory does not exist: $export_directory" >&2
  exit 1
}
[ ! -L "$export_directory" ] || {
  echo "Export directory must not be a symlink" >&2
  exit 1
}
if [ -e "$export_directory/.git" ] || [ -L "$export_directory/.git" ]; then
  echo "Refusing an export that contains .git" >&2
  exit 1
fi
[ -n "$destination" ] && [ "$destination" != "/" ] || {
  echo "Refusing unsafe destination: $destination" >&2
  exit 1
}
[ ! -L "$destination" ] || {
  echo "Destination must not be a symlink" >&2
  exit 1
}
if [ -e "$destination/.git" ] || [ -L "$destination/.git" ]; then
  if [ -L "$destination/.git" ]; then
    echo "Destination .git must not be a symlink" >&2
    exit 1
  fi
  if [ -f "$destination/.git" ]; then
    gitdir_line=$(sed -n '1p' "$destination/.git")
    case "$gitdir_line" in
      "gitdir: "?*) ;;
      *)
        echo "Destination .git file is not a Git worktree pointer" >&2
        exit 1
        ;;
    esac
  elif [ ! -d "$destination/.git" ]; then
    echo "Destination .git must be a real directory or regular worktree file" >&2
    exit 1
  fi
fi

export_absolute=$(python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).resolve())' "$export_directory")
destination_absolute=$(python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).resolve())' "$destination")
case "$destination_absolute/" in
  "$export_absolute/"*)
    echo "Destination must not be inside the export directory" >&2
    exit 1
    ;;
esac
case "$export_absolute/" in
  "$destination_absolute/"*)
    echo "Export directory must not be inside the destination" >&2
    exit 1
    ;;
esac
export_directory=$export_absolute
destination=$destination_absolute

python3 "$script_directory/validate.py" check --strict "$export_directory"

echo "Public export files:"
find "$export_directory" -type f -print | LC_ALL=C sort

if [ "$apply" != true ]; then
  echo "Dry run only; re-run with --apply to copy these files to: $destination"
  exit 0
fi

if [ -e "$destination" ] && [ ! -d "$destination" ]; then
  echo "Destination exists and is not a directory: $destination" >&2
  exit 1
fi
if [ -d "$destination" ]; then
  stale_entry=$(
    find "$destination" \
      ! -path "$destination" \
      ! -path "$destination/.git" \
      ! -path "$destination/.git/*" \
      -print -quit
  )
  if [ -n "$stale_entry" ]; then
    echo "Refusing non-empty destination; only .git may already exist: $stale_entry" >&2
    exit 1
  fi
fi

mkdir -p "$destination"
cp -R "$export_directory"/. "$destination"/
echo "Copied public export to: $destination"
echo "The destination .git entry, if present, was preserved."
