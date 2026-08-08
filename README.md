# Rose — Amazon DSP Program Manager Mock Interview Coach

An in-browser AI interview coach who plays your Amazon hiring-manager, listens to your
spoken answers, and scores them against the Leadership-Principles bar. Everything runs
**locally in your browser** — recordings, transcripts, and scores never leave your device.

> **Your live URL (once deployed):** `https://scaruana33-code.github.io/mock-interview/`

---

## 🚀 Fastest way to go live at your exact URL (auto-deploy, ~5 min)

This package includes a GitHub Actions workflow that **auto-publishes to your Pages URL**
every time you push. Steps:

1. Sign in to GitHub as **scaruana33-code** and create a new **public** repository named
   exactly **`mock-interview`** (the repo name is what makes the URL end in `/mock-interview/`).
2. Click **Add file → Upload files** and drag in **everything from this folder**, keeping the
   structure — including the hidden `.nojekyll` file and the `.github/workflows/deploy.yml`
   folder/file. Commit to the **main** branch.
3. Go to **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
4. The workflow runs automatically. In ~1–2 minutes Rose is live at:
   **`https://scaruana33-code.github.io/mock-interview/`**
5. Open it, click **Allow** on the microphone prompt, and start recording. 🎙️

> Prefer no Actions? You can instead pick **Deploy from a branch → main → / (root)** in
> Settings → Pages. The included `.nojekyll` makes that work too. Either path lands on the
> same URL.

---

## 🌹 What Rose does

1. **She listens.** Hit **Record** and Rose transcribes your answer live using your browser's
   speech-to-text (you'll watch the words appear).
2. **She scores you 0–5** on the five things an Amazon bar-raiser grades:
   - **STAR structure** — Situation, Task, Action, Result?
   - **Ownership ("I")** — she counts your *I*-vs-*we* ratio
   - **Data / metrics** — did numbers drive the story?
   - **Quantified result** — a %, $, time-saved, or SLA figure?
   - **Maps to the principle** — did you hit that Leadership Principle + the DSP payroll context?
3. **She delivers a verdict** — overall score, a **Strong Hire / Hire / Lean No / No Hire**
   debrief call, specific strengths & fixes, a pacing note (were you in the 2–4 min zone?),
   a filler-word count, and the **follow-up probe** she'd ask next.

Best experience is **Chrome or Edge**. In any browser you can also paste/edit a transcript
and Rose will score that.

---

## Using it as a "direct action" (one-click launch)

Once it's live at your URL, you can reach Rose instantly in whatever way suits you:

- **Browser bookmark / New-tab shortcut:** bookmark `https://scaruana33-code.github.io/mock-interview/`
  and pin it to your bookmarks bar — one click to practice.
- **Phone home-screen icon:** open the URL on your phone → **Share → Add to Home Screen**.
  It launches like an app (great for practicing out loud on the go).
- **Microsoft Teams tab:** in a Team/chat, **+ → Website** tab → paste your URL.
- **SharePoint page:** edit a page → **Embed** web part → paste:
  ```html
  <iframe src="https://scaruana33-code.github.io/mock-interview/"
          width="100%" height="1000" allow="microphone" style="border:0"></iframe>
  ```
  The `allow="microphone"` attribute is required, or recording is blocked in the frame.

---

## Files in this package

| File | Purpose |
|------|---------|
| `index.html` | The entire app, including Rose. |
| `.github/workflows/deploy.yml` | Auto-deploys to your GitHub Pages URL on every push. |
| `staticwebapp.config.json` | Config if you host on **Azure Static Web Apps** (mic permission + routing). |
| `netlify.toml` | Config if you drag-and-drop to **Netlify** (mic permission). |
| `.nojekyll` | Lets **GitHub Pages** serve files as-is. |
| `README.md` | This file. |

## Test locally first (optional)

```bash
python -m http.server 8000    # then open http://localhost:8000
```
`localhost` is a secure origin, so the mic and Rose's speech-to-text work.

## Privacy

All audio, transcripts, and Rose's scores live only in your browser's localStorage on the
device you use. Nothing is uploaded. **Reset** in the app (or clearing browser data) erases it.
