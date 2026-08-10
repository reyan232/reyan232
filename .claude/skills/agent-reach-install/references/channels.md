# Channel reference

Per-channel backends, credentials and constraints. Read the section for the
channels the user actually chose — there is no reason to load all of it.

- [Cookie handling](#cookie-handling-read-first) — read first, applies to most
- [Zero-config channels](#zero-config-channels)
- [OpenCLI](#opencli-desktop-only) · [Twitter/X](#twitterx) · [Reddit](#reddit)
- [XiaoHongShu](#xiaohongshu-小红书) · [Facebook / Instagram](#facebook--instagram)
- [Bilibili](#bilibili) · [Xueqiu](#xueqiu-雪球) · [Xiaoyuzhou](#xiaoyuzhou-小宇宙-podcasts)
- [LinkedIn](#linkedin) · [Proxies](#proxies) · [Upstream tools](#upstream-tool-cheatsheet)

## Cookie handling (read first)

Most authenticated channels use browser cookies. The reliable path is
Cookie-Editor, because it makes the user the one who decides what gets shared:

1. User logs into the platform in their own browser.
2. Install [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm).
3. Click the extension → Export → Header String.
4. Paste into the relevant `agent-reach configure …` hidden prompt.

**Recommend a dedicated/secondary account.** Platforms restrict or ban accounts
for non-browser API traffic, and a cookie is full account access — a throwaway
bounds both risks.

Do not scrape cookies the user didn't hand over, and do not echo a captured
value back into the conversation.

## Zero-config channels

Active after `--system` with no credentials: **Web** (Jina Reader), **YouTube**
(yt-dlp), **GitHub** (gh), **RSS** (feedparser), **Exa search** (mcporter),
**V2EX**, **Bilibili basic**. If these fail, suspect egress, not configuration.

## OpenCLI (desktop only)

One install backing Reddit, Facebook, Instagram, Bilibili subtitles, a Twitter
fallback and the XiaoHongShu desktop backend, by reusing the user's Chrome
session — no passwords stored, no API approval queues.

```bash
agent-reach install --env=auto --system --channels=opencli
```

Then a manual step Chrome's security model makes non-delegable:

1. Open <https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk>
2. Add to Chrome.
3. Verify: `opencli doctor` → `Extension: connected`.

The installer **skips OpenCLI on headless hosts**. That is correct behaviour,
not an error — but it silently removes Facebook and Instagram entirely, so tell
the user rather than letting them discover it in `doctor`.

`AUTH_REQUIRED` means no live session for that site: have the user log in in
Chrome. Do not log in for them.

## Twitter/X

```bash
agent-reach configure twitter-cookies   # hidden prompt; stores auth_token + ct0
```

This stores values for `doctor`'s config check. It does **not** modify your
shell, so calling the CLI directly needs them exported in that process:

```bash
export TWITTER_AUTH_TOKEN="..." TWITTER_CT0="..."
twitter search "query" -n 10
```

Binary is `twitter`. Fallback backend: OpenCLI.

## Reddit

Login is mandatory — anonymous endpoints are closed and the official API needs
manual approval. Desktop users should prefer OpenCLI. Otherwise `rdt-cli`:

```bash
rdt login    # extracts browser cookies where a browser exists
```

Headless: write `reddit_session` into `~/.config/rdt-cli/credential.json` by
hand, following the exact shape `agent-reach doctor` prints.

Binary is `rdt`, not `rdt-cli`. Server IPs are frequently rate-limited or
blocked outright; a residential proxy may be required.

## XiaoHongShu (小红书)

Backend depends on environment:

- **Desktop** — OpenCLI, using a Chrome session the user already has.
- **Server** — `xiaohongshu-mcp`: download the release binary into
  `~/.agent-reach/tools/`, run it (first start pulls ~150MB of headless
  browser), import cookies via Cookie-Editor, then
  `mcporter config add xiaohongshu http://localhost:18060/mcp --scope home`.
  Pass `--timeout 120000` on calls.
- **Legacy** — existing `xhs-cli` installs still work; upstream stopped
  updating in 2026-03, so don't install it fresh.

Explicit cookie import: `agent-reach configure xhs-cookies` (ignores non
`xiaohongshu.com` cookies, and does not inject anything into OpenCLI/Chrome).

Never automate a XiaoHongShu login. If there's no existing session, use the
Cookie-Editor route.

## Facebook / Instagram

OpenCLI only — desktop, reusing Chrome login. Not supported headless.

```bash
opencli facebook search "query" -f yaml
opencli facebook profile zuck -f yaml
opencli instagram user nasa -f yaml
```

Scope limits worth setting expectations on: Facebook Groups covers the group
list and recent activity the logged-in user can see, not arbitrary group posts
and comments. Instagram `search` finds *users*, not posts by keyword. On 429s
or login errors, have the user re-login in Chrome and slow the request rate.

## Bilibili

Basic search works with no login via `bili`. Subtitles route through OpenCLI,
so they need a desktop.

```bash
bili search "query" --type video
opencli bilibili subtitle BVxxxx
```

## Xueqiu (雪球)

Stock quotes and community posts; needs a logged-in cookie.

```bash
agent-reach configure --from-browser chrome --platform xueqiu
```

Reads only the minimum cookies for Xueqiu — it does not sweep other platforms.

## Xiaoyuzhou (小宇宙) podcasts

Transcription ships with Agent Reach; only a free Groq key is needed.

```bash
agent-reach configure groq-key
bash ~/.agent-reach/tools/xiaoyuzhou/transcribe.sh <episode-url>
```

Key from <https://console.groq.com> → API Keys (starts `gsk_`, no card needed).
Free tier is roughly 2 hours of audio per hour, recovering after ~15 minutes.
Whisper large-v3 quality, but no speaker diarization; split anything over two
hours.

## LinkedIn

Basic pages are readable through Jina Reader already. Full profile and job
search needs `mcp-server-linkedin` (requires `uv`/`uvx`):

```bash
mcporter config add linkedin --command uvx --arg mcp-server-linkedin@latest \
  --env UV_HTTP_TIMEOUT=300 --scope home
uvx mcp-server-linkedin@latest --login    # needs a visible browser
```

Session persists in `~/.linkedin-mcp/profile/`. Headless hosts need the login
run under something like VNC.

## Proxies

`twitter-cli` and `rdt-cli` honour standard proxy variables. Store the address
once via a hidden prompt, then export it for the calling process:

```bash
agent-reach configure proxy
export HTTP_PROXY="..." HTTPS_PROXY="..."
```

Needed for mainland-China networks, and often for server IPs that platforms
risk-score. Configuring a proxy is not a switch that unlocks a channel — it
only helps when the block is geographic or IP-reputation based. It will not
help against an allowlisting egress proxy, and you should never disable TLS
verification to get around one.

## Upstream tool cheatsheet

| Platform | Tool | Example |
|---|---|---|
| Twitter/X | `twitter` (alt `opencli`) | `twitter search "query" -n 10` |
| YouTube | `yt-dlp` | `yt-dlp --dump-json URL` |
| Bilibili | `bili` / `opencli` | `bili search "query" --type video` |
| Reddit | `opencli` (alt `rdt`) | `opencli reddit search "q" -f yaml` |
| Facebook / Instagram | `opencli` | `opencli instagram user nasa -f yaml` |
| GitHub | `gh` | `gh search repos "query"` |
| Web | `curl` + Jina | `curl -s "https://r.jina.ai/URL"` |
| Exa search | `mcporter` | `mcporter call exa.web_search_exa query="..."` |
| XiaoHongShu | `opencli` / `mcporter` | `opencli xiaohongshu search "q" -f yaml` |
| Xiaoyuzhou | `transcribe.sh` | `bash ~/.agent-reach/tools/xiaoyuzhou/transcribe.sh URL` |
| LinkedIn | `mcporter` | `mcporter call linkedin.get_person_profile …` |
| RSS | `feedparser` | `python3 -c "import feedparser; ..."` |

For multi-backend platforms, `agent-reach doctor --json` → `active_backend` is
the authority on what is actually serving a channel right now.
