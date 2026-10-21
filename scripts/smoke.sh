#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${1:-http://127.0.0.1:8080}"
curl --fail --silent --show-error "$BASE_URL/health"
echo
