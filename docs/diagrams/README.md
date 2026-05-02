# Architecture diagrams (Excalidraw)

## See the diagram in the browser (zoom, pan) — option 3

The GitHub README only shows a **static** image. To get the **Excalidraw** experience (zoom, pan, edit):

1. **Share link (easiest for viewers)**  
   Open the **interactive** diagram using the one-click link in the **“Excalidraw in the browser”** section of [`../architecture.md`](../architecture.md) (same as working in the app, with zoom and pan on [excalidraw.com](https://excalidraw.com)).  
   For the best view of our diagrams, turn on **dark mode** in Excalidraw (toolbar sun/moon icon, or **Menu** → theme).

2. **Source file in this folder (for version control)**  
   - Export your drawing as **`.excalidraw`** from Excalidraw and commit it under `docs/diagrams/` (e.g. `architecture.excalidraw`).  
   - Viewers can: download the file from GitHub → open [excalidraw.com](https://excalidraw.com) → **☰ → Open** and choose the file.  
   - After the file is on the default branch, the **raw** URL is:  
     `https://raw.githubusercontent.com/<user>/<repo>/<branch>/docs/diagrams/<file>.excalidraw`  
     (use **Raw** on GitHub to copy or open in a new tab, then import into Excalidraw if the app offers “import from link”.)

3. **Optional: PNG / SVG in `docs/images/`**  
   For a quick preview in the README, export PNG or SVG, but for **zoom** prefer the **share link** or the **`.excalidraw` file** as above.

---

## File naming (suggested)

- `architecture.excalidraw` — main system / technical MVP architecture (keep in sync with `docs/architecture.md` text).

When you change the drawing, re-export the share link in `docs/architecture.md` if the shared scene URL changed.
