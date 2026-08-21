#!/usr/bin/env bash

set -u

usage() {
  echo "Usage: scan-copy-patterns.sh FILE [FILE ...]" >&2
  echo "Reports line-oriented editorial prompts; it does not infer authorship." >&2
}

if [ "$#" -eq 0 ]; then
  usage
  exit 2
fi

overall_status=0

for input_path in "$@"; do
  if [ ! -f "$input_path" ] || [ ! -r "$input_path" ]; then
    echo "ERROR: cannot read file: $input_path" >&2
    overall_status=2
    continue
  fi

  case "$input_path" in
    */*) awk_input="$input_path" ;;
    *) awk_input="./$input_path" ;;
  esac

  awk '
    function clean(value) {
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
      return value
    }

    function report(category, sample) {
      printf "%s:%d: %s: %s\n", FILENAME, FNR, category, clean(sample)
      findings++
    }

    function starts_paragraph(value, lower, words, count, lead) {
      if (!after_blank || value ~ /^[[:space:]]*$/ || value ~ /^[[:space:]]*#/ ||
          value ~ /^[[:space:]]*([-*+]|[0-9]+[.)])[[:space:]]/) {
        return
      }
      lower = tolower(clean(value))
      gsub(/[^[:alnum:][:space:]-]/, "", lower)
      count = split(lower, words, /[[:space:]]+/)
      if (count < 2) {
        return
      }
      lead = words[1] " " words[2]
      if (lead == prior_lead) {
        report("repeated paragraph opening", lead)
      }
      prior_lead = lead
    }

    BEGIN {
      findings = 0
      in_fence = 0
      after_blank = 1
      prior_lead = ""
    }

    {
      line = $0

      if (line ~ /^[[:space:]]*(```|~~~)/) {
        in_fence = !in_fence
        next
      }

      if (in_fence) {
        next
      }

      if (line ~ /^[[:space:]]*$/) {
        after_blank = 1
        next
      }

      lower = tolower(line)
      starts_paragraph(line)

      if (lower ~ /in today.s ([[:alnum:]-]+[[:space:]]+)*(world|landscape|environment)/ ||
          index(lower, "when it comes to") > 0 ||
          index(lower, "without further ado") > 0) {
        report("stock opening or transition", line)
      }

      if (index(lower, "it is important to note") > 0 ||
          lower ~ /it.s important to note/ ||
          index(lower, "it is worth noting") > 0 ||
          lower ~ /it.s worth noting/ ||
          index(lower, "needless to say") > 0 ||
          index(lower, "it goes without saying") > 0) {
        report("removable meta-commentary", line)
      }

      if (index(lower, "delve into") > 0 ||
          index(lower, "ever-evolving landscape") > 0 ||
          index(lower, "navigate the complexities") > 0 ||
          index(lower, "unlock the power") > 0 ||
          index(lower, "unlock the potential") > 0 ||
          index(lower, "game-changer") > 0) {
        report("inflated or generic phrasing", line)
      }

      if (index(lower, "in conclusion") > 0 ||
          index(lower, "in summary") > 0 ||
          index(lower, "to sum up") > 0) {
        report("stock conclusion", line)
      }

      if (lower ~ /whether you.re (a|an|the)/ || lower ~ /whether you are (a|an|the)/) {
        report("broad audience sweep", line)
      }

      if (index(lower, "not only") > 0 && index(lower, "but also") > 0) {
        report("paired rhetorical construction", line)
      }

      punctuation = line
      exclamations = gsub(/!/, "", punctuation)
      if (exclamations >= 2) {
        report("dense exclamation punctuation", line)
      }

      after_blank = 0
    }

    END {
      printf "%s: %d review prompt(s). Review in context; matches do not identify how text was written.\n",
             FILENAME, findings
      if (findings > 0) {
        exit 1
      }
    }
  ' "$awk_input"

  scan_status=$?
  if [ "$scan_status" -eq 1 ] && [ "$overall_status" -eq 0 ]; then
    overall_status=1
  elif [ "$scan_status" -gt 1 ]; then
    overall_status=2
  fi
done

exit "$overall_status"
