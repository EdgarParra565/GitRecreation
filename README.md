# GitRecreation

GitRecreation is a small Python implementation of Git-style version control.
The command line tool is named `ugit` and stores repository data in a local
`.ugit/` directory.

This project is mainly for learning how Git works internally. It implements
objects, refs, branches, commits, tags, checkout, diffs, merges, a staging
index, and simple local-path fetch/push operations.

## Requirements

- Python 3
- `setuptools`
- Unix `diff` and `diff3` commands for diff and merge output
- Graphviz `dot` if you want to use the `ugit k` commit graph command

If `setuptools` is missing, install it with:

```bash
python3 -m pip install --user setuptools
```

## Installation

From the project root:

```bash
python3 setup.py develop --user
```

Or use pip's editable install mode:

```bash
python3 -m pip install --user -e .
```

If the `ugit` command is not found after installation, add your user Python
bin directory to `PATH`. On macOS with Python 3.14, that may be:

```bash
export PATH="$HOME/Library/Python/3.14/bin:$PATH"
```

## Basic Usage

Create a repository:

```bash
ugit init
```

Stage files:

```bash
ugit add README.md
ugit add ugit
```

Create a commit:

```bash
ugit commit -m "Initial commit"
```

View history:

```bash
ugit log
```

Show the current status:

```bash
ugit status
```

View unstaged changes:

```bash
ugit diff
```

View staged changes:

```bash
ugit diff --cached
```

## Commands

| Command | Description |
| --- | --- |
| `ugit init` | Create a `.ugit/` repository in the current directory. |
| `ugit add <files...>` | Add files or directories to the staging index. |
| `ugit commit -m <message>` | Create a commit from the current index. |
| `ugit status` | Show the current branch, merge state, staged changes, and unstaged changes. |
| `ugit log [commit]` | Print commit history starting at a commit, branch, tag, or `@`. |
| `ugit show [commit]` | Print a commit and its diff against its first parent. |
| `ugit diff [commit]` | Compare the index or working tree against another tree. |
| `ugit diff --cached [commit]` | Compare the index against a commit. |
| `ugit checkout <commit-or-branch>` | Check out a commit or branch into the working tree. |
| `ugit reset <commit>` | Move `HEAD` to another commit. |
| `ugit branch [name] [start_point]` | List branches or create a branch. |
| `ugit tag <name> [commit]` | Create a tag pointing to a commit. |
| `ugit merge <commit>` | Merge another commit into the current `HEAD`. |
| `ugit merge_base <commit1> <commit2>` | Print the common ancestor for two commits. |
| `ugit fetch <path>` | Fetch objects and branch refs from another local `ugit` repository. |
| `ugit push <path> <branch>` | Push a local branch to another local `ugit` repository. |
| `ugit hash-object <file>` | Store a file as a blob object and print its object ID. |
| `ugit cat-file <object>` | Print a raw object. |
| `ugit write-tree` | Write the current index as a tree object. |
| `ugit read-tree <tree>` | Read a tree into the index. |
| `ugit k` | Render the commit graph with Graphviz. |

`@` is used as a shortcut for `HEAD`.

## How It Works

`ugit` stores data inside `.ugit/`:

- `.ugit/objects/` contains content-addressed objects.
- `.ugit/HEAD` points to the current commit or branch ref.
- `.ugit/refs/heads/` stores branch refs.
- `.ugit/refs/tags/` stores tag refs.
- `.ugit/index` stores the staging area as JSON.
- `.ugit/MERGE_HEAD` is used while a merge is in progress.

Objects are written with a simple header:

```text
<type>\0<content>
```

The object ID is the SHA-1 hash of that stored object.

## Example Workflow

```bash
ugit init
ugit add README.md ugit
ugit commit -m "Create first commit"

ugit branch feature
ugit checkout feature

echo "notes" > notes.txt
ugit add notes.txt
ugit commit -m "Add notes"

ugit checkout master
ugit merge feature
ugit status
```

## Local Remote Workflow

Remote support currently works with another local `ugit` repository path:

```bash
ugit fetch ../other-repo
ugit push ../other-repo master
```

Fetched branch refs are stored under `.ugit/refs/remote/`.

## Project Layout

```text
ugit/
  base.py      Core repository operations.
  cli.py       Command-line parser and command handlers.
  data.py      Object storage, refs, and index helpers.
  diff.py      Tree diffing and three-way merge helpers.
  remote.py    Local-path fetch and push support.
setup.py       Package metadata and console script entry point.
```
