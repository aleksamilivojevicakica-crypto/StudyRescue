# StudyRescue 4.0 — AI study planner (EN / DE / FR)

**Complete runnable hackathon prototype** built with HTML, CSS, JavaScript and Python's standard library. No `npm install`, no Python dependencies, no database server, and **no AI key needed for core planning features**.

## QUICK START — WINDOWS (only an AI key is optional)

1. Install **Python 3.10 or newer** if it is not already installed. On Windows, select **Add Python to PATH** during installation.
2. Extract the complete ZIP archive. **Do not move just `index.html` out of the folder**.
3. Double-click `START_WINDOWS.bat`. A terminal opens and your browser can open at **http://127.0.0.1:8000/**.
4. The site works **without an AI key**: create tasks, schedule work, see overdue warnings and analytics, switch between English, German and French, use a focus timer, save or restore a backup, and export a calendar `.ics` file.
5. To switch on **REAL AI**, open the file named **`.env`** in Notepad. Add a key after the `=` sign on **ONE** of these lines:

```ini
GEMINI_API_KEY=PASTE_YOUR_REAL_GEMINI_KEY_HERE
OPENAI_API_KEY=
```

Or, if using OpenAI instead:

```ini
GEMINI_API_KEY=
OPENAI_API_KEY=PASTE_YOUR_REAL_OPENAI_KEY_HERE
```

Save the file (keep its name **`.env`**, not `.env.txt`), stop the running server with `Ctrl+C`, and double-click `START_WINDOWS.bat` again. It automatically detects which provider has a key. If both are filled, Gemini takes priority. You **do not need to edit HTML, CSS, JavaScript or Python code** to activate AI.

**Where to get a key:** [Google AI Studio](https://aistudio.google.com/apikey) for Gemini, or [OpenAI Platform](https://platform.openai.com/api-keys) for OpenAI. A ChatGPT subscription is **not** an API key and does not automatically include API credits. Some models, providers, geographic regions, and accounts may have costs, quotas, or access restrictions.

### macOS / Linux

Run `./START_MAC_LINUX.sh` inside the extracted folder (or `python3 server.py`). Visit **http://127.0.0.1:8000/**. For API setup, use the same `.env` steps as Windows.

### If the site opens but AI does not

* Under **Preferences**, check **AI connection**. If it shows a configured provider, click **Test live AI connection** to make a small real API request (this may consume tokens/cost). A configured key alone does not guarantee the provider is reachable.
* Verify the key was entered into `.env`, not `.env.example`, and that you **restarted** the server.
* An expired/invalid key, missing credits, unavailable model or network outage will make connected AI unavailable. The rest of the site continues working.
* If the server says that port 8000 is in use, close the other terminal running it. Alternatively change `PORT=8001` in `.env` and visit `http://127.0.0.1:8001`.
* Opening `index.html` directly via `file:///` will show most offline functionality, but it **cannot reach the AI backend**. Use the server launchers.
* `.env` may be hidden in file explorers. In Notepad, use **File → Open → All files**. Do not rename it inadvertently.

## Main site features

There are **six independent pages in each of three languages**, for a total of **18 localized HTML pages**:

| Section | Features |
|---|---|
| **Overview** | Task summary, priority list, upcoming sessions, overload alert |
| **Assignments** | Create, edit, delete, mark complete, filter and search; quick add from natural language; AI photo-to-task extraction |
| **My schedule** | Deadline-aware dynamic 21-day plan; 7-day calendar view; 50-minute max work blocks; deadline-conflict warnings and focus timer |
| **AI Study Coach** | Offline workload analysis; real AI analysis (with key); study-step breakdown; **new conversation interface with task context** |
| **Insights** | Completion rate, pending time by subject, next week's workload |
| **Preferences** | Weekly available minutes, start time, example data, JSON backup and restore, `.ics` calendar export, privacy & AI status |

Changing EN / DE / FR retains **the same assignments** when pages share a site origin. Translations apply to navigation, task forms, warnings, labels and AI response instructions. AI responses are requested in the selected site language. Task names you entered yourself are not automatically translated.

### About the scheduling algorithm

The local planner sorts by **earliest deadline first**, with importance and difficulty as tie-breakers, and allocates estimated durations into blocks of at most 50 minutes across your available daily minutes. It excludes elapsed time today, identifies overdue tasks, and warns when known work cannot fit before deadlines. It looks ahead **21 days** and explicitly labels later deadlines as outside its horizon. It is an explainable deterministic algorithm, **not** a self-trained neural network. Changes to tasks and availability recompute the plan. It does not automatically know your school hours or real-life events; those must be reflected in Preferences.

### About connected AI

The Python backend calls an existing hosted model (OpenAI or Gemini) to:
* Explain workload and priorities, taking planner warnings into account.
* Propose achievable steps to start an assignment.
* Interpret descriptions typed in ordinary language, showing a proposed task for review.
* Extract one proposed assignment from a JPEG, PNG or WebP photo (max. 3 MB, requires AI with vision support).
* Answer a study planning question in the **Chat to AI Coach**, supplied with the student's unfinished tasks.

A model response may be wrong. **Always verify extracted due dates and assignment details before accepting them.** Text and images sent for AI features are transmitted to the chosen model provider; core offline features do not require sending homework to an external service.

## Privacy and security

* Assignments are saved locally with **localStorage** in that browser. There are **no accounts, remote user database, or cross-device sync**. Make a JSON backup before clearing site data or changing browsers.
* `.env` is ignored by Git and is *not served* by `server.py`. The API key stays on the server, not the webpage.
* **Never put `.env` or API keys in GitHub, public website assets, screenshots, emails or chat.** If publishing, first remove `.env` from all uploaded files and configure the key as a private server environment variable.
* This server is **local only** (`127.0.0.1`) by default. Its API endpoints have no user authentication; do **not** expose it publicly with a paid key without adding authentication, robust rate limits, abuse prevention and proper hosting controls. Publishing only the static site is safe but connected AI then will not work.
* The app is intended as an educational **hackathon prototype**, not a production service or a school-approved grade tool.

## File layout

```
StudyRescue_4/
  .env                      <-- PASTE KEY HERE, PRIVATE (do not upload!)
  .env.example              <-- Blank template for GitHub
  .gitignore
  START_WINDOWS.bat         <-- Double-click on Windows
  START_MAC_LINUX.sh
  server.py                 <-- Backend and model connections
  index.html                <-- Redirect to English overview
  assets/
    app.js                  <-- All application features
    translations.js         <-- EN / DE / FR dictionaries
    styles.css              <-- Responsive styles
    favicon.svg
  en/ de/ fr/               <-- 6 real HTML pages per language
  tests/                    <-- Test scripts; not needed to run app
  README.md
```

## Hackathon demo / submission

A compact 3–4 minute video should show: (1) assignments, (2) a realistic schedule, (3) an overloaded day and honest warning, (4) AI coaching/chat if you have configured a key, (5) EN / DE / FR switching, and (6) insights. Mention clearly whether the recorded demo uses the **actual AI** or only offline guidance. **GitHub code must exclude `.env`**. For Devpost, include screenshots, a description of the student problem, solution, technologies, limitations and a link to the functioning site if deployed.

Static hosting (e.g. GitHub Pages) can run all **offline** features, but cannot execute `server.py`. To offer connected AI online, host this server on a separate trusted backend platform with private environment variables and adapt the site's API calls for that deployment. The current ZIP is ready to run locally, but **not automatically published to the internet**.

## Testing

The project uses standard-library Python and plain JS. Quick checks:

```bash
python -m unittest discover -s tests -p 'test_server.py' -v
node tests/test_logic.cjs
```

Browser smoke tests (optional) use Playwright + Chromium, which are **only required for testing**, not for the site to run.

## Sources for supported API formats

* [OpenAI Chat Completions](https://platform.openai.com/docs/api-reference/chat) — text and image inputs for compatible models.
* [Gemini generateContent API](https://ai.google.dev/api/generate-content) — text, inline image input and JSON output mode for supported models.

Original educational project. You can customize and publish the code without credentials.
