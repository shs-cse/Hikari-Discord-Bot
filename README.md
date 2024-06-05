# Discord Bot (Hikari + Docker)
This code is meant for maintaining official discord servers of CSE250, CSE251, CSE350, CSE460, and CSE428 at [Brac University, Dhaka, Bangladesh](https://www.bracu.ac.bd/).

# Instructions for Bot Setup
- The very first time...
    - ubuntu 24.04 (lts)
    - `sudo apt install python3-full`
    - `git clone https://github.com/shs-cse/hikari-discord-bot.git . && git update-index --skip-worktree info.jsonc`
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
    - `pip install xlrd pandas pygsheets`
    - `pip install -U hikari[speedups]`
    - `pip install hikari-crescent`
    - `pip install -U hikari-miru`
    - `python -dO main.py`
- Rerun the bot for a new semester...
- Dev Notes

# Dev Notes
## How to update [`info.jsonc`](./info.jsonc) file
- Don't track changes in the file:
    ```bash
    git update-index --skip-worktree info.jsonc
    ```
- Track changes in the file again:
    ```bash
    git update-index --no-skip-worktree info.jsonc
    ```
