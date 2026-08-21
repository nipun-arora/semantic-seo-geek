#!/usr/bin/env bash

set -u

usage() {
  echo "Usage: page-structure-audit.sh [--format auto|markdown|html] FILE" >&2
  echo "Performs mechanical, line-oriented checks and does not calculate an SEO score." >&2
}

format="auto"
if [ "${1:-}" = "--format" ]; then
  if [ "$#" -lt 3 ]; then
    usage
    exit 2
  fi
  format="$2"
  shift 2
fi

if [ "$#" -ne 1 ]; then
  usage
  exit 2
fi

input_path="$1"
if [ ! -f "$input_path" ] || [ ! -r "$input_path" ]; then
  echo "ERROR: cannot read file: $input_path" >&2
  exit 2
fi

case "$input_path" in
  */*) awk_input="$input_path" ;;
  *) awk_input="./$input_path" ;;
esac

if [ "$format" = "auto" ]; then
  case "$input_path" in
    *.[Hh][Tt][Mm][Ll]|*.[Hh][Tt][Mm]) format="html" ;;
    *) format="markdown" ;;
  esac
fi

if [ "$format" != "markdown" ] && [ "$format" != "html" ]; then
  echo "ERROR: format must be auto, markdown, or html" >&2
  exit 2
fi

echo "FILE: $input_path"
echo "FORMAT: $format"

if [ "$format" = "markdown" ]; then
  awk '
    function issue(kind, message, line_number) {
      if (line_number > 0) {
        printf "%s line %d: %s\n", kind, line_number, message
      } else {
        printf "%s: %s\n", kind, message
      }
      if (kind == "ERROR") errors++
      else if (kind == "WARN") warnings++
      else notices++
    }

    BEGIN {
      errors = warnings = notices = 0
      h1_count = 0
      prior_level = 0
      in_fence = 0
    }

    {
      line = $0

      if (line ~ /^[[:space:]]*(```|~~~)/) {
        in_fence = !in_fence
        next
      }
      if (in_fence) next

      if (line ~ /(^|[^[:alnum:]_])(TODO|TBD|TK)([^[:alnum:]_]|$)/) {
        issue("WARN", "unfinished editorial marker", FNR)
      }

      if (line ~ /\]\([[:space:]]*\)/) {
        issue("ERROR", "empty Markdown link or image destination", FNR)
      }

      if (line ~ /!\[[[:space:]]*\]\(/) {
        issue("NOTICE", "image has empty alt text; confirm it is decorative", FNR)
      }

      if (match(line, /^#+[[:space:]]/)) {
        level = RLENGTH - 1
        if (level > 6) {
          issue("WARN", "heading uses more than six hash marks", FNR)
          next
        }
        if (level == 1) h1_count++
        if (prior_level > 0 && level > prior_level + 1) {
          issue("WARN", "heading level jumps from " prior_level " to " level, FNR)
        }
        prior_level = level

        heading = substr(line, RLENGTH + 1)
        gsub(/[[:space:]]+#+[[:space:]]*$/, "", heading)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", heading)
        key = tolower(heading)
        if (key == "") {
          issue("WARN", "empty heading", FNR)
        } else if (seen_heading[key]++) {
          issue("WARN", "duplicate heading text: " heading, FNR)
        }
      }
    }

    END {
      if (h1_count == 0) issue("WARN", "no level-one heading found; confirm this is an intentional fragment", 0)
      else if (h1_count > 1) issue("WARN", h1_count " level-one headings found; confirm the page hierarchy", 0)
      if (in_fence) issue("ERROR", "unclosed fenced code block", 0)
      printf "SUMMARY: %d error(s), %d warning(s), %d notice(s). No score is calculated.\n",
             errors, warnings, notices
      if (errors > 0) exit 1
    }
  ' "$awk_input"
  exit $?
fi

awk '
  function issue(kind, message, line_number) {
    if (line_number > 0) {
      printf "%s line %d: %s\n", kind, line_number, message
    } else {
      printf "%s: %s\n", kind, message
    }
    if (kind == "ERROR") errors++
    else if (kind == "WARN") warnings++
    else notices++
  }

  BEGIN {
    errors = warnings = notices = 0
    h1_count = title_count = main_count = 0
    prior_level = 0
  }

  {
    original = $0
    line = tolower(original)

    if (line ~ /(^|[^[:alnum:]_])(todo|tbd|tk)([^[:alnum:]_]|$)/) {
      issue("WARN", "unfinished editorial marker", FNR)
    }

    work = line
    while (match(work, /<title([[:space:]][^>]*)?>/)) {
      title_count++
      work = substr(work, RSTART + RLENGTH)
    }

    work = line
    while (match(work, /<main([[:space:]][^>]*)?>/)) {
      main_count++
      work = substr(work, RSTART + RLENGTH)
    }

    work = line
    while (match(work, /<h[1-6]([[:space:]][^>]*)?>/)) {
      tag = substr(work, RSTART, RLENGTH)
      level = substr(tag, 3, 1) + 0
      if (level == 1) h1_count++
      if (prior_level > 0 && level > prior_level + 1) {
        issue("WARN", "heading level jumps from " prior_level " to " level, FNR)
      }
      prior_level = level
      work = substr(work, RSTART + RLENGTH)
    }

    work = line
    while (match(work, /<img([[:space:]][^>]*)?[[:space:]]*\/?>/)) {
      tag = substr(work, RSTART, RLENGTH)
      if (tag !~ /[[:space:]]alt[[:space:]]*=/) {
        issue("ERROR", "img element has no alt attribute", FNR)
      } else if (tag ~ /[[:space:]]alt[[:space:]]*=[[:space:]]*"[[:space:]]*"/ ||
                 tag ~ /[[:space:]]alt[[:space:]]*=[[:space:]]*'"'"'[[:space:]]*'"'"'/ ||
                 tag ~ /[[:space:]]alt[[:space:]]*=[[:space:]]*\/?>$/) {
        issue("NOTICE", "img has empty alt text; confirm it is decorative", FNR)
      }
      work = substr(work, RSTART + RLENGTH)
    }

    work = line
    while (match(work, /<a[[:space:]][^>]*>/)) {
      tag = substr(work, RSTART, RLENGTH)
      if (tag ~ /[[:space:]]href[[:space:]]*=[[:space:]]*"[[:space:]]*"/ ||
          tag ~ /[[:space:]]href[[:space:]]*=[[:space:]]*'"'"'[[:space:]]*'"'"'/ ||
          tag ~ /[[:space:]]href[[:space:]]*=[[:space:]]*>$/) {
        issue("ERROR", "anchor has an empty href", FNR)
      }
      work = substr(work, RSTART + RLENGTH)
    }

    work = original
    lower_work = tolower(work)
    while (match(lower_work, /[[:space:]]id[[:space:]]*=[[:space:]]*"[^"]+"/)) {
      id_part = substr(work, RSTART, RLENGTH)
      sub(/^[^"]*"/, "", id_part)
      sub(/"$/, "", id_part)
      if (seen_id[id_part]++) {
        issue("ERROR", "duplicate id: " id_part, FNR)
      }
      work = substr(work, RSTART + RLENGTH)
      lower_work = substr(lower_work, RSTART + RLENGTH)
    }

    work = original
    lower_work = tolower(work)
    while (match(lower_work, /[[:space:]]id[[:space:]]*=[[:space:]]*'"'"'[^'"'"']+'"'"'/)) {
      id_part = substr(work, RSTART, RLENGTH)
      sub(/^[^'"'"']*'"'"'/, "", id_part)
      sub(/'"'"'$/, "", id_part)
      if (seen_id[id_part]++) {
        issue("ERROR", "duplicate id: " id_part, FNR)
      }
      work = substr(work, RSTART + RLENGTH)
      lower_work = substr(lower_work, RSTART + RLENGTH)
    }

    work = original
    lower_work = tolower(work)
    while (match(lower_work, /[[:space:]]id[[:space:]]*=[[:space:]]*[^[:space:]"'"'"'=<>`]+/)) {
      id_part = substr(work, RSTART, RLENGTH)
      sub(/^[^=]*=[[:space:]]*/, "", id_part)
      if (seen_id[id_part]++) {
        issue("ERROR", "duplicate id: " id_part, FNR)
      }
      work = substr(work, RSTART + RLENGTH)
      lower_work = substr(lower_work, RSTART + RLENGTH)
    }
  }

  END {
    if (title_count == 0) issue("WARN", "no title element found; confirm this is an intentional fragment", 0)
    else if (title_count > 1) issue("ERROR", title_count " title elements found", 0)
    if (h1_count == 0) issue("WARN", "no h1 found; confirm this is an intentional fragment", 0)
    else if (h1_count > 1) issue("WARN", h1_count " h1 elements found; confirm the page hierarchy", 0)
    if (main_count == 0) issue("NOTICE", "no main element found; confirm the template supplies a main landmark", 0)
    else if (main_count > 1) issue("WARN", main_count " main elements found", 0)
    printf "SUMMARY: %d error(s), %d warning(s), %d notice(s). No score is calculated.\n",
           errors, warnings, notices
    if (errors > 0) exit 1
  }
' "$awk_input"
