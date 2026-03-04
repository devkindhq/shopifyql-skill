---
name: shopifyql-setup
description: Interactive setup wizard for ShopifyQL plugin credentials and preferences. Run this once to configure your Shopify store connection — credentials work across all projects.
---

You are running the ShopifyQL plugin setup wizard. Your job is to check Python, collect credentials, and configure them so the plugin works across any project.

**Security note:** You must NEVER read `.env` or display a full access token back to the user at any point during this wizard.

## Step 0 — Check Python environment

Before anything else, run:

```bash
python3.11 --version 2>/dev/null || echo "NOT_FOUND"
```

**If Python 3.11 is found:** confirm to the user — "Python 3.11 detected. ✓" — and proceed.

**If NOT_FOUND:** tell the user Python 3.11 is required and show the install options:

> **macOS (Homebrew — recommended):**
> ```bash
> brew install python@3.11
> ```
> After install, verify: `python3.11 --version`
>
> **macOS (without Homebrew):**
> Download the installer from [python.org/downloads](https://www.python.org/downloads/) — select version 3.11.x.
>
> **Verify Homebrew is installed first (if using Homebrew):**
> ```bash
> brew --version 2>/dev/null || /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/brew.sh/install/HEAD/install.sh)"
> ```
>
> **Ubuntu / Debian:**
> ```bash
> sudo apt update && sudo apt install -y python3.11 python3.11-venv python3-pip
> ```
>
> **Fedora / RHEL / CentOS:**
> ```bash
> sudo dnf install -y python3.11
> ```
>
> **Other Linux (pyenv — works on any distro):**
> ```bash
> curl https://pyenv.run | bash
> pyenv install 3.11
> pyenv global 3.11
> ```

Then check if the required Python packages are installed:

```bash
python3.11 -c "import shopifyql, dotenv, pandas, certifi" 2>&1 || echo "MISSING_DEPS"
```

**If MISSING_DEPS:** show the install command and run it with user approval:

```bash
pip3.11 install 'shopifyql[all]' pandas python-dotenv certifi
```

Do not proceed to credential collection until Python 3.11 is confirmed working.

---

## Step 1 — Explain how credentials work for this plugin

Before collecting anything, explain:

> This is a Claude Code plugin — credentials are set **once** as OS environment variables and work across every project automatically. You won't need to run this setup again per project.
>
> The plugin checks credentials in this order:
> 1. **OS environment variables** (recommended — set once in `~/.zshrc`, works everywhere)
> 2. **`.env` file in the current project** (local dev fallback only)
>
> Which would you like to use?

Use `AskUserQuestion` with options:
- "OS environment variables (recommended — works across all projects)"
- "Project `.env` file (this project only)"

## Step 2 — Collect credentials

Use `AskUserQuestion` to ask ONE question at a time:

**Question 1 — Store URL:**
Ask: "What is your Shopify store URL?"

- Accept formats: `my-store.myshopify.com`, `https://my-store.myshopify.com`, `my-store`
- Normalise to full domain: strip `https://`, strip trailing slashes, append `.myshopify.com` if no dot present

**Question 2 — Access Token:**
Ask: "Paste your Admin API access token (from your Custom App in Shopify Partners)."

- Warn if it doesn't start with `shpat_`
- Never display the full token back to the user after collection

## Step 3 — Save credentials

**If OS environment variables (recommended):**

Do NOT write any file. Show the user the exact lines to add to their shell profile:

```bash
# Add to ~/.zshrc (macOS) or ~/.bashrc (Linux)
export SHOPIFY_STORE_URL=<store_url>
export SHOPIFY_ACCESS_TOKEN=<token>
```

Then show the one-liner to apply it immediately:

```bash
echo 'export SHOPIFY_STORE_URL=<store_url>' >> ~/.zshrc && \
echo 'export SHOPIFY_ACCESS_TOKEN=<token>' >> ~/.zshrc && \
source ~/.zshrc
```

Explain: "Done — your token never touches any project file. The plugin will pick it up automatically in every project."

---

**If `.env` file:**

Write `.env` in the project root using the `Write` tool:

```
SHOPIFY_STORE_URL=<value>
SHOPIFY_ACCESS_TOKEN=<value>
```

Preserve any other existing lines. Then confirm: "Saved to `.env` (gitignored). Note: this only works in this project — to use across projects, re-run `/shopifyql-setup` and choose the env var option."

## Step 4 — Confirm and next steps

Tell the user:

- "Setup complete. Store: `<store_url>`. Token saved (masked)."
- "To run a query, just ask: 'run this ShopifyQL query: FROM sales SHOW net_sales SINCE ...'"

## Error handling

- If Write fails due to permissions (`.env` option), tell the user to create the file manually with the two lines shown in Step 3.
- If the token doesn't start with `shpat_`, warn but still save — Custom App tokens may vary.
- If `pip3.11` is not found after installing Python 3.11 via Homebrew, tell the user to run `brew link python@3.11` or use the full path: `/opt/homebrew/bin/pip3.11 install ...`
- If the user is on Apple Silicon (M1/M2/M3), Homebrew installs to `/opt/homebrew/` — tell them to add `export PATH="/opt/homebrew/bin:$PATH"` to `~/.zshrc` if `python3.11` is not found after install.
