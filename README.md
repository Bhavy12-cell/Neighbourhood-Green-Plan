# 🌳 Neighbourhood Green Plan

A small web app that turns "someone should clean up our street and plant some trees" into an actual plan. Enter your area, number of volunteers, date and type of space, and get a complete cleanup and tree-planting plan in seconds, powered by the open-weight **Gemma** model.

Built for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05).

## What it does

Given your inputs, the app generates five sections, each in its own tab:

| Tab | What you get |
|-----|--------------|
| 🌳 Trees | 4-5 native trees/plants suited to the season and area, and why |
| 📋 Plan | A step-by-step cleanup and planting schedule with timings |
| 👥 Roles | How to split the work among your volunteers |
| 🧰 Supplies | A checklist of what to bring |
| 💬 WhatsApp | A short, friendly invite message you can copy into your neighbourhood group |

You can also download the full plan as a Markdown file.

**The idea:** the screen should be the shortest part of the experience. Generate the plan, send one message, then put the phone down and go outside.

## Tech stack

- **Model:** Gemma (`gemma-4-26b-a4b-it`), Google's open-weight model, called through Google AI Studio
- **UI:** [Streamlit](https://streamlit.io) with custom CSS
- **SDK:** [`google-genai`](https://pypi.org/project/google-genai/)
- **Language:** Python 3

## How it works

1. The form inputs are combined into one prompt.
2. The prompt asks Gemma to reply in simple, friendly English and to split the answer into five sections, each starting with a marker such as `[[TREES]]` or `[[PLAN]]`.
3. A small parser splits the response on those markers and shows each section in a tab.
4. If the model skips the markers, the app falls back to showing the full response instead of breaking.

## Getting started

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install dependencies

```bash
pip install streamlit google-genai
```

### 3. Get an API key

1. Go to [aistudio.google.com](https://aistudio.google.com) and sign in.
2. Click **Get API key** and then **Create API key**.

### 4. Add your key and model

Open `app.py` and edit the two lines at the top:

```python
API_KEY = "your-api-key-here"
MODEL = "models/gemma-4-26b-a4b-it"
```

To see which Gemma models your key can use, run:

```python
from google import genai

client = genai.Client(api_key="YOUR_KEY")
for m in client.models.list():
    if "gemma" in m.name.lower():
        print(m.name)
```

### 5. Run the app

```bash
streamlit run app.py
```

It opens at `http://localhost:8501`.

## ⚠️ Keep your API key private

Never commit a real API key to GitHub. Before pushing, make sure the line in `app.py` reads:

```python
API_KEY = ""
```

If a key is ever exposed by mistake, delete it in Google AI Studio and create a new one.

## Limitations

- **Not offline.** This version calls Gemma through the hosted Google AI Studio API, so it needs an internet connection.
- **Verify the trees.** Species suggestions come from the model. Please check them with a local nursery or forest department before planting.
- **Marker format.** Gemma occasionally ignores the section markers. The app then shows the plain response, and clicking **Create plan** again usually fixes it.

## Why open weights?

- **No lock-in:** the model name is a single line, so swapping models is trivial.
- **A path to running locally:** the same prompt and logic could run on a laptop through a local runtime, keeping everything on the user's own machine.
- **Room to adapt:** open weights make it possible to fine-tune on local knowledge such as regional trees, languages or municipal rules.

## Ideas for next steps

- Run Gemma locally for fully offline use
- Add Hindi and other regional languages
- Add a photo upload to assess a site before planning
- Add a map of the neighbourhood

## License

MIT, or choose the license you prefer.
