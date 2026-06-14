#!/bin/bash

echo "================================================="
echo "   LinkedIn CV Updater - Chrome CDP Launcher     "
echo "================================================="
echo "Launching Google Chrome with Remote Debugging enabled on Port 9222..."
echo ""
echo "Important: "
echo "1. If Chrome is already open normally, you MUST close it completely first."
echo "   (Right click Chrome in Dock -> Quit, or Cmd+Q)"
echo "2. Once launched, sign into LinkedIn and leave the window open."
echo "3. The MCP server will automatically connect to this instance."
echo "================================================="

# Start Chrome with remote debugging on port 9222
# Using a dedicated user data dir to satisfy Chrome's security requirements for CDP
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --no-first-run \
  --no-default-browser-check \
  --user-data-dir="$HOME/Chrome_Dev_Profile"
