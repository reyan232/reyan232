---
name: agent-reach-install
description: >
  Install, repair, or upgrade Agent Reach — the toolkit that gives an agent
  read access to Twitter/X, Reddit, XiaoHongShu, Bilibili, YouTube, GitHub,
  Facebook, Instagram, LinkedIn, V2EX, Xueqiu, Xiaoyuzhou podcasts, RSS and
  arbitrary web pages. Use this whenever the user asks to install / set up /
  reinstall / update Agent Reach, pastes the install.md or update.md URL from
  the Panniantong/agent-reach repo, says "帮我安装 Agent Reach", asks which
  channels they can unlock, or reports that agent-reach channels show as
  broken, unavailable, ❌ or ⚠️ in `agent-reach doctor`. Also use it when a
  user wants their agent to "be able to read Reddit/Twitter/小红书" and no
  such tooling exists yet — that is an Agent Reach install even if they never
  name it. NOT for fetching content once Agent Reach is working: the separate
  `agent-reach` skill does the actual searching and reading.
---

# Installing Agent Reach

Agent Reach is a selector, installer, health checker and router — never a
wrapper. After installation you call the upstream tools directly (`twitter`,
`rdt`, `bili`, `opencli`, `yt-dlp`, `gh`, `mcporter`). Knowing this shapes the
whole job: you are not installing one program, you are provisioning a fleet of
CLIs and then proving which ones can actually reach the internet.

The canonical upstream instructions live at
`https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md`.
Fetch them when you need exact current flags; this skill covers the workflow
and the failure modes that document assumes away.

## The failure this skill exists to prevent

The install almost always "succeeds". Packages resolve, `doctor` prints a
channel count, everyone feels good — and then the tool cannot fetch a single
page because the host's egress is restricted, or because the one channel the
user actually wanted needs a desktop Chrome that isn't there.

So: **establish what this machine can reach before you install anything, and
report capability rather than installation status at the end.** A user who
hears "3/15 channels active" believes they have three working channels. If
those three cannot resolve their hosts, you have misled them.

## Step 0 — Preflight

```bash
bash scripts/preflight.sh
```

It reports the Python install path available, whether this is a desktop or a
headless/sandboxed host, and — most importantly — probes the actual sites
Agent Reach reads, separating the *install lane* (pypi, codeload) from the
*content lane* (reddit, x.com, r.jina.ai, …).

Act on the verdict before touching the system:

- **Content lane mostly blocked** → say so now, plainly, and ask whether to
  continue. A gated CI container, a corporate proxy or a locked-down cloud
  sandbox will install Agent Reach perfectly and read nothing. The honest
  framing is "I can install it, but it won't be able to fetch anything here —
  do you want it anyway, or should I give you the steps for your laptop?"
- **Headless host** → OpenCLI is unavailable, and with it Facebook, Instagram,
  and the preferred backends for Reddit and XiaoHongShu. Do not offer those as
  if they were on the table.
- **Ephemeral container** → whatever you install disappears with the session.
  Mention it, because an install that evaporates is worth knowing about in
  advance, not after.

## Step 1 — Install the package

Try these in order; each fallback exists for a failure the previous one hits.

```bash
# 1. Preferred
pipx install https://github.com/Panniantong/agent-reach/archive/main.zip

# 2. No pipx, or PEP 668 externally-managed interpreter (Homebrew/Debian)
python3 -m venv ~/.agent-reach-venv
~/.agent-reach-venv/bin/pip install https://github.com/Panniantong/agent-reach/archive/main.zip

# 3. The archive URL 403s (proxy allowlists GitHub per-repo)
git clone --depth 1 https://github.com/Panniantong/agent-reach /tmp/agent-reach
~/.agent-reach-venv/bin/pip install /tmp/agent-reach
```

Fallback 3 is common in agent sandboxes: `git` traffic is proxied and allowed
while raw archive downloads are refused. A 403 on the `.zip` while `git clone`
of the same repo works is that signature, not a broken mirror. In a Claude Code
remote session, `add_repo` grants the clone. Clone to `/tmp` or `~`, **never
into the user's working directory** — polluting their project is a real cost.

If you used a venv, put the entry point on PATH so later steps and the user's
future shells find it:

```bash
ln -sf ~/.agent-reach-venv/bin/agent-reach /usr/local/bin/agent-reach   # or ~/.local/bin
```

### Windows

`python3` may be a Microsoft Store alias rather than a real interpreter — if
`where python3` points into `WindowsApps`, use the launcher `py -3` instead:

```powershell
py -3 -m venv $env:USERPROFILE\.agent-reach-venv
$env:USERPROFILE\.agent-reach-venv\Scripts\python.exe -m pip install https://github.com/Panniantong/agent-reach/archive/main.zip
```

## Step 2 — Check, then install system dependencies

`agent-reach install` is read-only by default. Run it that way first and show
the user what it found:

```bash
agent-reach install --env=auto              # check only, changes nothing
agent-reach install --env=auto --dry-run    # preview what --system would do
```

`--system` installs the core external tooling (gh CLI, Node bits, mcporter +
Exa search, yt-dlp config) and may use the system package manager. **Get
explicit approval before running it** — it is the step that touches the host:

```bash
agent-reach install --env=auto --system
```

Never reach for `sudo` on your own initiative. If something needs elevation,
name what needs it and let the user decide.

## Step 3 — Let the user choose channels

Present the optional channels and let them pick, filtered by what Step 0
proved possible. Offering XiaoHongShu-via-OpenCLI on a headless box wastes
everyone's time.

```bash
agent-reach install --env=auto --system --channels=opencli,twitter,reddit
```

Valid names: `opencli`, `twitter`, `xiaoyuzhou`, `xueqiu`, `xiaohongshu`,
`reddit`, `facebook`, `instagram`, `bilibili`, `linkedin`, `all`.

OpenCLI is the highest-leverage single pick on a desktop — one install backs
Reddit, Facebook, Instagram, Bilibili subtitles, a Twitter fallback and the
XiaoHongShu desktop backend, all reusing the user's existing Chrome session.
It requires a Chrome extension the user must add by hand; the installer cannot
do it for them.

Read `references/channels.md` for per-channel credential setup, the cookie
security guidance, and the desktop-vs-server backend split.

## Step 4 — Diagnose honestly

```bash
agent-reach doctor          # human readable
agent-reach doctor --json   # active_backend per channel; use for real answers
```

Read `doctor` output critically rather than relaying it:

- The **N/15 count means binaries are present and configured**, not that
  anything was fetched. Never present it as proven capability.
- `⚠️`/`warn` usually means *installed but unauthenticated* — a cookie or key
  is missing. That is a Step 5 item, not a failure.
- Some warnings are deliberate: doctor won't run `gh auth status` (it writes a
  device-id) and won't start remote MCP services, so it declines to claim those
  are live. Don't "fix" a channel that is merely unverified.
- **Binary names differ from channel names.** Reddit installs as `rdt`, Twitter
  as `twitter`. Checking `which rdt-cli` fails on a perfectly good install and
  sends you chasing nothing. With a `uv`-based install they land in
  `~/.local/bin`; confirm that directory is on PATH.

Where a channel is genuinely broken, fix it within the boundaries below. Where
it's blocked by the network, say that rather than retrying.

## Step 5 — Credentials

Only ask for what the chosen channels actually need — see
`references/channels.md` for exact commands. Values go in via hidden prompts
(`agent-reach configure …`), which keeps secrets out of shell history and the
transcript. Never paste a token or cookie back to the user.

Recommend a **secondary account** for any cookie-authenticated platform. Cookie
auth carries two real risks: platforms ban accounts for non-browser API access,
and a leaked cookie grants full account access. A throwaway account bounds the
damage on both.

Storing a Twitter cookie does not export it — running `twitter` directly still
needs `TWITTER_AUTH_TOKEN` and `TWITTER_CT0` in that process's environment.

## Step 6 — Report

Close with what the user can *do*, separating three states so the summary is
actionable:

1. **Working** — verified, with the command they'd use.
2. **Needs credentials** — exactly which one, and how to supply it.
3. **Unavailable here** — with the reason (no desktop, blocked egress,
   ephemeral host), not left as an unexplained ❌.

If the host is ephemeral or gated, repeat it here even if you said it in
Step 0 — it is the single most important caveat and it belongs next to the
final result. If the install can't do what the user wanted, offer the
alternative: the same steps on their own machine.

Optionally set up `agent-reach watch` on a daily schedule for ongoing health
and update checks — offer it, don't assume it.

## Boundaries

These come from upstream and are worth respecting because violating them
breaks user trust in ways that are hard to walk back:

- No `sudo` without explicit approval.
- Keep files in `~/.agent-reach/` (config, tokens), `~/.agent-reach/tools/`
  (upstream repos), `/tmp` (scratch). Never in the user's workspace.
- Install only what this workflow and upstream's guide call for.
- Never disable firewalls, TLS verification, or proxy settings to force a
  channel to work. A blocked host is a fact to report, not an obstacle to
  route around.
- Never log in on the user's behalf or scrape browser cookies they didn't
  explicitly export. XiaoHongShu in particular: OpenCLI may reuse a Chrome
  session the user already controls, but nothing here should be creating one.
