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

Since this project is packaged and distributed, you can install it globally on your system using `uv` or `pipx`:

```bash
uv tool install git+https://github.com/sonnguyent1/linkedin-cv-updater.git
```
*or*
```bash
pipx install git+https://github.com/sonnguyent1/linkedin-cv-updater.git
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

Once you restart your IDE, the server will launch seamlessly in the background and its tools will be available to your Agent!

## 🧠 Features & Prompts

This server exposes several Tools and Prompts:
- **Tools**: `update_linkedin_experience`, `update_linkedin_about`
- **Prompts**: `extract_project_highlights`, `format_linkedin_content`

Your Agent is instructed to use the prompts to extract your technical achievements from your local codebase *before* utilizing the tools to type them into LinkedIn.

## 📝 Logs
To ensure FastMCP's JSON-RPC protocol remains uncorrupted, all execution logs are safely written to `~/.linkedin-cv-updater/logs/server.log`.
