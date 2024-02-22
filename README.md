# Discord Bot (Hikari + Docker)
This code is meant for maintaining official discord servers of CSE250, CSE251, CSE350, CSE460, and CSE428 at [Brac University, Dhaka, Bangladesh](https://www.bracu.ac.bd/).

# Instructions for Bot Setup
- The very first time...
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