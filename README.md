# Seiler Asterces — landing page

*Where there is a Will there is a Way.*

A single-page, fractal landing page for the [Seiler Asterces](https://www.youtube.com/@secretsarelies9681) YouTube channel — the visual and audio laboratory of Secrets Are Lies.

Live: `https://vcpmark.github.io/seiler-asterces/`

## What it does

- **The fractal** is a Julia set rendered live in a WebGL shader. Its parameter walks the edge of the Mandelbrot set's main cardioid, so the shape is always connected and intricate, never dust. Exterior glow comes from a distance estimate; the interior is shaded by an orbit trap, which gives the slow-moving "veins."
- **On a phone**, tilting the device shifts the fractal, the parallax of the video ring, and the epigraph. Motion is measured as deltas from a slowly re-centring baseline, so it responds to movement, not to how you happen to be holding the phone. iOS asks permission via the "Turn on motion" button; Android just works.
- **On a desktop**, the mouse does what tilt does. Scroll wheel, arrow keys, or drag rotate the ring of videos. Browsing the ring also nudges the fractal.
- **Videos** sit on an orbit. The front one is the stage; click or tap it to play inline (youtube-nocookie embed). Others are thumbnails and dots receding into the scene.
- **The video list updates itself.** A GitHub Action pulls the channel's public RSS feed every six hours (and on every push) and writes `videos.json`. No API key. Until the first sync runs, the page shows a single "Latest uploads" tile that plays the channel's uploads playlist.
- Render resolution adapts to the device's frame rate, `prefers-reduced-motion` freezes the drift, and there's a gradient fallback if WebGL is unavailable.

## Deploy

With the [GitHub CLI](https://cli.github.com) installed and signed in:

```bash
./setup.sh
```

That creates a public repo named `seiler-asterces` under your account, pushes, turns on GitHub Pages from the `main` branch, and kicks off the first video sync. Set `REPO=something ./setup.sh` to use a different name.

### Manual steps (no `gh`)

1. Create an empty public repo on github.com.
2. In this folder: replace `vcpmark` in `index.html` with your GitHub username (it's only used for the share image URL), then
   ```bash
   git init -b main && git add -A && git commit -m "Seiler Asterces"
   git remote add origin https://github.com/YOUR-USER/seiler-asterces.git
   git push -u origin main
   ```
3. Repo → Settings → Pages → Source: *Deploy from a branch* → `main` / `/ (root)` → Save.
4. Repo → Actions → *Sync videos from YouTube* → Run workflow (or wait for the next scheduled run).

## Files

| Path | Purpose |
| --- | --- |
| `index.html` | The whole page: styles, shader, interaction. No build step. |
| `videos.json` | Written by the Action; the page reads it. |
| `scripts/sync_videos.py` | Fetches the RSS feed and writes `videos.json`. Python stdlib only. |
| `.github/workflows/sync-videos.yml` | Schedule + commit-if-changed. |
| `og.png`, `icon.png` | Share image and favicon, rendered from the same fractal. |
| `setup.sh` | One-shot deploy. |

## Run locally

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000`. Device motion needs HTTPS or localhost, so this works on the laptop; to test tilt on a phone, use the live GitHub Pages URL.

## Tweaks

- Epigraph text: the `<p class="epigraph">` in `index.html`.
- Channel: `CHANNEL_ID` / `HANDLE` in `scripts/sync_videos.py`, and `UPLOADS_PLAYLIST` plus the two channel links in `index.html` (`UU` + the channel ID after `UC`).
- Palette: the `pal()` function in the fragment shader, plus the CSS variables at the top of the stylesheet.
- Sync frequency: the `cron` line in the workflow.
