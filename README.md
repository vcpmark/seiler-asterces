# Seiler Asterces

*Where there is a Will there is a Way.*

The landing page for the [Seiler Asterces](https://www.youtube.com/@secretsarelies9681) YouTube channel — the visual and audio laboratory of Secrets Are Lies. Deep frequencies, generative ecosystems, dark-mode aesthetics. Best experienced with studio monitors.

**Live:** https://vcpmark.github.io/seiler-asterces/

## What it does

- **The fractal** is a Julia set rendered live in a WebGL shader. Its parameter walks the edge of the Mandelbrot set's main cardioid, so the shape is always connected and intricate, never dust. Exterior glow comes from a distance estimate; the interior is shaded by an orbit trap, which gives the slow-moving "veins."
- **On a phone**, tilting the device shifts the fractal, the parallax of the video ring, and the epigraph. Motion is measured as deltas from a slowly re-centring baseline, so it responds to movement, not to how you happen to be holding the phone. iOS asks permission via the "Turn on motion" button; Android just works.
- **On a desktop**, the mouse does what tilt does. Scroll wheel, arrow keys, or drag rotate the ring of videos. Browsing the ring also nudges the fractal.
- **Videos** sit on an orbit. The front one is the stage; click or tap it to play inline (youtube-nocookie embed). Others are thumbnails and dots receding into the scene.
- **The video list updates itself.** A GitHub Action pulls the channel's public RSS feed every six hours and rewrites `videos.json` when something changed. No API key. If the list is ever empty, the page shows a single "Latest uploads" tile that plays the channel's uploads playlist.
- Render resolution adapts to the device's frame rate, `prefers-reduced-motion` freezes the drift, and there's a gradient fallback if WebGL is unavailable.

## Files

| Path | Purpose |
| --- | --- |
| `index.html` | The whole page: styles, shader, interaction. No build step. |
| `videos.json` | Written by the Action; the page reads it. |
| `scripts/sync_videos.py` | Fetches the RSS feed and writes `videos.json`. Python stdlib only. |
| `.github/workflows/sync-videos.yml` | Schedule + commit-if-changed. |
| `og.png`, `icon.png` | Share image and favicon, rendered from the same fractal. |

## Tweaks

- Epigraph text: the `<p class="epigraph">` in `index.html`.
- Channel: `CHANNEL_ID` / `HANDLE` in `scripts/sync_videos.py`, and `UPLOADS_PLAYLIST` plus the two channel links in `index.html` (`UU` + the channel ID after `UC`).
- Palette: the `pal()` function in the fragment shader, plus the CSS variables at the top of the stylesheet.
- Sync frequency: the `cron` line in the workflow.
