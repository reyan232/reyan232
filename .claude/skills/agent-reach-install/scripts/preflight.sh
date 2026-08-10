#!/usr/bin/env bash
# Agent Reach preflight: report the environment before installing anything.
#
# Answers three questions that change the whole install plan:
#   1. Which Python install path is available (pipx / uv / venv fallback)?
#   2. Is this a desktop with Chrome, a headless server, or a gated sandbox?
#   3. Can this host actually reach the sites Agent Reach exists to read?
#
# Read-only. Installs nothing, writes nothing outside /tmp.

set -uo pipefail

hr() { printf '%s\n' "----------------------------------------"; }
have() { command -v "$1" >/dev/null 2>&1; }

echo "Agent Reach preflight"
hr

# --- 1. Python / installer tooling -------------------------------------------
echo "[tooling]"
for t in python3 pipx uv pip3 node npm git curl; do
  if have "$t"; then
    printf '  ok      %-8s %s\n' "$t" "$(command -v "$t")"
  else
    printf '  missing %-8s\n' "$t"
  fi
done

if have python3; then
  echo "  python  $(python3 --version 2>&1)"
  # PEP 668 marks an interpreter as externally managed; plain `pip install`
  # into it will refuse, which is the most common install failure.
  if python3 -c 'import sysconfig,os,sys; sys.exit(0 if os.path.exists(os.path.join(sysconfig.get_path("stdlib"),"EXTERNALLY-MANAGED")) else 1)' 2>/dev/null; then
    echo "  note    interpreter is PEP 668 externally-managed -> use pipx or a venv"
  fi
fi

if have agent-reach; then
  echo "  note    agent-reach already installed: $(agent-reach --version 2>&1 | head -1)"
fi

hr

# --- 2. Desktop vs headless ---------------------------------------------------
echo "[environment]"
KIND="headless server"
if [ "$(uname -s)" = "Darwin" ]; then
  if [ -d "/Applications/Google Chrome.app" ]; then KIND="desktop (macOS + Chrome)"; else KIND="macOS, no Chrome found"; fi
elif [ -n "${WSL_DISTRO_NAME:-}" ]; then
  KIND="WSL (treat as headless unless Chrome is reachable)"
elif [ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]; then
  KIND="desktop (Linux with display)"
fi
echo "  kind    $KIND"
for b in google-chrome google-chrome-stable chromium chromium-browser; do
  have "$b" && { echo "  chrome  $(command -v $b)"; break; }
done
[ -f /.dockerenv ] && echo "  note    container detected (/.dockerenv)"
if [ -n "${HTTPS_PROXY:-}${https_proxy:-}" ]; then
  echo "  proxy   HTTPS_PROXY is set -> egress is mediated, expect host allowlisting"
fi
echo "  hint    OpenCLI needs a desktop + Chrome extension. On a headless host the"
echo "          installer skips it, which also drops Facebook/Instagram and the"
echo "          preferred Reddit and XiaoHongShu backends."

hr

# --- 3. Egress ----------------------------------------------------------------
# The point of Agent Reach is reading these sites. A host that installs
# cleanly but cannot reach them yields a green doctor and zero capability,
# so probe before promising anything.
echo "[egress]"
# A proxy that refuses a CONNECT tunnel yields 000; one that answers with
# 403/407 is allowlisting rather than dropping traffic. Both mean "you cannot
# read this site", but the second tells the user a policy is in play.
probe() { # label host
  local code
  code=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 12 "$2" 2>/dev/null)
  case "$code" in
    000|"")  printf '  BLOCKED %-15s %s\n' "$1" "$2"; return 1 ;;
    403|407) printf '  GATED   %-15s %s (%s)\n' "$1" "$2" "$code"; return 1 ;;
    *)       printf '  ok      %-15s %s (%s)\n' "$1" "$2" "$code"; return 0 ;;
  esac
}

echo "  -- install lane (needed to install at all)"
INSTALL_BAD=0
probe "pypi"     "https://pypi.org/simple/"                     || INSTALL_BAD=$((INSTALL_BAD+1))
probe "codeload" "https://codeload.github.com/pypa/pipx/zip/refs/heads/main" || INSTALL_BAD=$((INSTALL_BAD+1))

echo "  -- content lane (what Agent Reach exists to read)"
CONTENT_BAD=0; CONTENT_ALL=0
for pair in \
  "web|https://r.jina.ai/https://example.com" \
  "github-api|https://api.github.com" \
  "youtube|https://www.youtube.com" \
  "reddit|https://www.reddit.com" \
  "twitter|https://x.com" \
  "bilibili|https://www.bilibili.com"; do
  CONTENT_ALL=$((CONTENT_ALL+1))
  probe "${pair%%|*}" "${pair#*|}" || CONTENT_BAD=$((CONTENT_BAD+1))
done

hr
echo "[verdict]"
[ "$INSTALL_BAD" -gt 0 ] && {
  echo "  Install lane is restricted. pip may fail on the GitHub archive URL;"
  echo "  fall back to: git clone the repo, then pip install from the local path."
}
if [ "$CONTENT_BAD" -eq 0 ]; then
  echo "  Egress open ($CONTENT_ALL/$CONTENT_ALL content hosts). Proceed normally."
elif [ "$CONTENT_BAD" -ge $((CONTENT_ALL - 1)) ]; then
  echo "  $CONTENT_BAD/$CONTENT_ALL content hosts unreachable: a gated network, not a"
  echo "  broken install. Say so BEFORE installing. Agent Reach will install"
  echo "  cleanly and doctor will count channels as present, but nothing here"
  echo "  can actually be fetched."
else
  echo "  Partial egress ($CONTENT_BAD/$CONTENT_ALL blocked). Install, then offer only"
  echo "  the channels whose hosts answered above."
fi
