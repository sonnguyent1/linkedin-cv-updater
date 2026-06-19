# LinkedIn CV Updater FastMCP Server

This FastMCP server integrates with your AI Agent to automate the process of updating your LinkedIn profile's Experience and About sections. It reads your local project code, extracts key metrics and tech stack highlights, and pushes beautifully formatted, action-oriented bullet points directly to your LinkedIn profile.

## 🚀 Architecture (CDP Automation)

Unlike standard APIs that are heavily rate-limited or blocked by LinkedIn CAPTCHAs, this tool uses **Playwright + Chrome DevTools Protocol (CDP)**. It connects to your *actual, running Chrome browser* to perform UI automation. 

This means:
- No passwords or cookie extraction required!
- Zero CAPTCHA blocks!
- Fully secure, running on your local machine.

## 🛠️ Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended)
- Google Chrome installed (macOS)

## 📦 Installation

Since this project is packaged and distributed via GitHub Actions, the fastest way to install it is using the pre-compiled release binaries (wheel files) from the Releases page.

**Install the latest pre-compiled release (v0.2.2):**
```bash
uv tool install https://github.com/sonnguyent1/linkedin-cv-updater/releases/download/v0.2.2/linkedin_cv_updater_mcp-0.2.2-py3-none-any.whl
```
*or using pipx:*
```bash
pipx install https://github.com/sonnguyent1/linkedin-cv-updater/releases/download/v0.2.2/linkedin_cv_updater_mcp-0.2.2-py3-none-any.whl
```

**Alternatively, install directly from the repository source:**
```bash
uv tool install git+https://github.com/sonnguyent1/linkedin-cv-updater.git
```

This will give you a global `linkedin-cv-updater` command.

## 🏃‍♂️ Usage Guide

Because this MCP server drives your live browser, you must start Chrome with a specific debugging port open *before* your Agent calls the tools.

### Step 1: Launch Chrome with CDP
We have provided a helper script for macOS. **Make sure Chrome is completely quit first (Cmd+Q)**, then run:

```bash
curl -sL https://raw.githubusercontent.com/sonnguyent1/linkedin-cv-updater/main/scripts/start_chrome.sh | bash
```

*(This launches Chrome with `--remote-debugging-port=9222` and mounts a dedicated DevTools profile.)*

### Step 2: Log into LinkedIn
In the newly opened Chrome window, navigate to LinkedIn and ensure you are logged in. **Leave this window open.**

### Step 3: Configure your IDE
Add the server to your IDE's MCP Configuration file (`mcp_config.json`):

```json
{
  "mcpServers": {
    "linkedin-cv-updater": {
      "command": "linkedin-cv-updater",
      "args": [],
      "env": {
        "LINKEDIN_PROFILE_ID": "your-profile-id"
      }
    }
  }
}
```

### Step 4: Trigger Your IDE Agent
Once configured and restarted, paste this simple, natural language prompt into your IDE agent to trigger the entire end-to-end flow autonomously:

> *"Act as my career manager. Extract my technical achievements and the company name from this repository, fetch my current LinkedIn bio, and push formatted updates to both my LinkedIn Experience and About sections. Finally, export my profile as a PDF CV."*

Or even simpler:
> *"Extract my project highlights, update my LinkedIn experience and bio, and save my profile as a PDF."*

Because FastMCP tools are self-describing, your Agent will automatically discover and string together all the necessary prompts and tools to complete the task. Sit back and watch the browser automate the updates!

### 💅 Bonus: The CV Beautification Pipeline
Want to turn your raw LinkedIn profile into a stunning, professionally styled physical PDF? We built a dedicated pipeline for that! Just tell your agent:

> *"Export my LinkedIn profile, rewrite my achievements to make them sound professional and impactful, and generate a beautiful physical PDF CV for me."*

The Agent will seamlessly download your profile, rewrite your achievements for maximum impact, apply premium typography, and render it into a pixel-perfect `beautified_cv.pdf` file!

## 🧠 Features & Prompts

This server exposes several Tools and Prompts:
- **Tools**: `update_linkedin_experience`, `update_linkedin_about`, `export_linkedin_pdf`, `generate_beautiful_cv`
- **Prompts**: `extract_project_highlights`, `format_linkedin_content`, `extract_company_name`, `beautify_cv`

Your Agent is instructed to use the prompts to extract your technical achievements from your local codebase *before* utilizing the tools to type them into LinkedIn.

## 📝 Logs
To ensure FastMCP's JSON-RPC protocol remains uncorrupted, all execution logs are safely written to `~/.linkedin-cv-updater/logs/server.log`.
