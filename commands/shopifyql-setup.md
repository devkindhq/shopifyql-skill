---
name: shopifyql-setup
description: Interactive setup wizard for ShopifyQL plugin credentials and preferences. Run this once per project to configure your Shopify store connection.
---

You are running the ShopifyQL plugin setup wizard. Your job is to explain the credential options to the user, collect their preference, then either write `.env` or show them the shell export commands.

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

## Step 1 — Explain credential options

Before collecting anything, explain the two ways credentials can be provided, and ask which they prefer:

> **Option A — `.env` file (easiest):**
> Credentials are written to a `.env` file in the project root. The script reads this file automatically. The file should be gitignored and never committed.
> ⚠️ Note: Claude Code itself is blocked from reading `.env`, so the token stays private.
>
> **Option B — OS environment variables (more secure):**
> You export credentials in your shell before launching Claude Code. The token is never written to disk in this project at all — it only lives in your shell session.
>
> Which would you prefer?

Use `AskUserQuestion` with options "`.env` file" and "OS environment variables".

## Step 2 — Check for existing config (Option A only)

If the user chose Option A, use `Bash` to check whether `.env` exists and has a non-empty `SHOPIFY_STORE_URL`:

```bash
grep -s 'SHOPIFY_STORE_URL' .env | head -1
```

- If a value is found, tell the user: "A store URL is already configured (`<url>`). Would you like to update it, or keep it?" — mask any token, never show it.
- If nothing found, proceed to collect all fields.

## Step 3 — Collect credentials

Use `AskUserQuestion` to ask ONE question at a time:

**Question 1 — Store URL:**
Ask: "What is your Shopify store URL?"
- Accept formats: `my-store.myshopify.com`, `https://my-store.myshopify.com`, `my-store`
- Normalise to full domain: strip `https://`, strip trailing slashes, append `.myshopify.com` if no dot present

**Question 2 — Access Token:**
Ask: "Paste your Admin API access token (from your Custom App in Shopify Partners)."
- Warn if it doesn't start with `shpat_`
- Never display the full token back to the user after collection

## Step 4 — Save credentials

**If Option A (`.env` file):**

Write `.env` in the project root using the `Write` tool with this exact format:

```
SHOPIFY_STORE_URL=<value>
SHOPIFY_ACCESS_TOKEN=<value>
```

Preserve any other existing lines in `.env` that aren't being updated.

Then confirm: "Credentials saved to `.env`. This file is gitignored — do not commit it."

---

**If Option B (OS environment variables):**

Do NOT write any file. Instead, show the user these exact commands to run in their terminal before launching Claude Code:

```bash
export SHOPIFY_STORE_URL=<store_url>
export SHOPIFY_ACCESS_TOKEN=<token>
```

Then explain:

> Add these to your shell profile (`~/.zshrc` or `~/.bashrc`) to make them permanent:
>
> ```bash
> echo 'export SHOPIFY_STORE_URL=<store_url>' >> ~/.zshrc
> echo 'export SHOPIFY_ACCESS_TOKEN=<token>' >> ~/.zshrc
> source ~/.zshrc
> ```
>
> With this approach, your token is never written to disk inside this project. The script picks up environment variables automatically.

## Step 5 — Confirm and next steps

Tell the user:
- "Setup complete. Store: `<store_url>`. Token saved (masked)."
- "To run a query, just ask: 'run this ShopifyQL query: FROM sales SHOW net_sales SINCE ...'"
- "Or use the executor directly: `python3.11 scripts/execute_query.py --query \"...\"`"

## Error handling

- If Write fails due to permissions (Option A), tell the user to create `.env` manually with the two lines shown in Step 4.
- If the token doesn't start with `shpat_`, warn but still save — Custom App tokens may vary.
- If `pip3.11` is not found after installing Python 3.11 via Homebrew, tell the user to run `brew link python@3.11` or use the full path: `/opt/homebrew/bin/pip3.11 install ...`
- If the user is on Apple Silicon (M1/M2/M3) and Homebrew installs to `/opt/homebrew/` instead of `/usr/local/`, `python3.11` may not be on PATH automatically — tell them to add `export PATH="/opt/homebrew/bin:$PATH"` to their `~/.zshrc`.
