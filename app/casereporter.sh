#!/usr/bin/env bash
# casereporter: CLI-Wrapper für CaseReporter API

API_URL="http://localhost:8000"

usage() {
  echo "Usage: $(basename "$0") -g <CASE_ID> | -f <CASE_ID>"
  echo
  echo "Options:"
  echo "  -g <CASE_ID>   Generiert das PDF-Gutachten für den Fall CASE_ID"
  echo "  -f <CASE_ID>   Liefert nur das KI-Fazit für Fall CASE_ID"
  echo "  -h             Zeigt dieses Hilfe-Menü"
  exit 1
}

# Prüfen, ob getopt verfügbar ist
if ! command -v getopt >/dev/null 2>&1; then
  echo "getopt not found, please install util-linux or an equivalent package." >&2
  exit 1
fi

# Optionen parsen
PARSED=$(getopt -o g:f:h --long generate:,fazit:,help -- "$@")
if [[ $? -ne 0 ]]; then usage; fi

eval set -- "$PARSED"

ACTION=""
CASE_ID=""

while true; do
  case "$1" in
    -g|--generate)
      ACTION="generate"
      CASE_ID="$2"
      shift 2
      ;;
    -f|--fazit)
      ACTION="fazit"
      CASE_ID="$2"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    --)
      shift
      break
      ;;
    *)
      usage
      ;;
  esac
done

if [[ -z "$ACTION" || -z "$CASE_ID" ]]; then
  usage
fi

case "$ACTION" in
  generate)
    echo "Generiere Gutachten für Fall: $CASE_ID"
    curl -s -X GET "$API_URL/reports/$CASE_ID" --output "gutachten_${CASE_ID}.pdf"
    echo "PDF gespeichert als gutachten_${CASE_ID}.pdf"
    ;;
  fazit)
    echo "Hole KI-Fazit für Fall: $CASE_ID"
    curl -s -X POST "$API_URL/reports/$CASE_ID/fazit"
    echo
    ;;
esac