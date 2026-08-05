# Code samples for IIIF-CS

Python samples accompanying the API documentation pages. Each `p{NN}_{topic}/`
directory matches a documentation page (numbered by sidebar order); the shared
helpers live in `iiif_cs.py` and `settings.py` in this directory.

## One-time setup

1. Create and activate a virtual environment in this directory, and install the
   dependencies:

   ```
   cd dlcs-docs-client
   python -m venv .venv
   .venv\Scripts\activate        # (Windows; on macOS/Linux: source .venv/bin/activate)
   pip install requests python-dotenv
   ```

2. Create a `.env` file **in this directory** with your settings, using the example
   in [example.env](example.env).

## Running a sample

Always run from **this directory** (`dlcs-docs-client`), using Python's *module*
form — dots, no `.py`, no leading `.\`:

```
python -m p04_entrypoint.entrypoint
python -m p06_space.create_space
python -m p08_queue.get_batches
```

Tab completion works if you type the path first and then fix it up, but the argument
really is a module name: `p04_entrypoint.entrypoint`, not a file path.

### Why the other obvious invocations fail

| Attempt | Why it fails |
|:---|:---|
| `cd p04_entrypoint` then `python entrypoint.py` | When you run a *script file*, Python puts the **script's own directory** on the import path — not your shell's current directory. `iiif_cs.py` lives one level up, so `ModuleNotFoundError: No module named 'iiif_cs'`. |
| `python p04_entrypoint\entrypoint.py` from here | Same rule: the path entry is `p04_entrypoint\`, not this directory. Same error. |
| `python -m .\p04_entrypoint\entrypoint.py` | `-m` takes a **module name**, not a file path — hence "Relative module names not supported". |
| `python -m entrypoint` from inside `p04_entrypoint` | Would find the module, but `iiif_cs` is still not on the path (and the `.env` wouldn't load — see below). |

`python -m package.module` works because `-m` puts the **current working
directory** first on the import path — so `iiif_cs`, `settings`, and cross-sample
imports (e.g. `p09_batch` importing from `p08_queue`) all resolve.

Two more reasons the working directory must be this one:

- `settings.py` calls `load_dotenv()`, which looks for `.env` relative to the
  current working directory.
- Some samples import helpers from sibling sample packages by their
  `p{NN}_…` name.

## What the samples are (and aren't)

Deliberately simple, synchronous, no error handling — they exist to show the HTTP
operations as clearly as possible, not to be a client library. Most demonstrate a
flow top-to-bottom under `if __name__ == '__main__':` and print each request and
response as they go. They run against the API named in your `.env`
(`IIIF_CS_API_HOST`) and most create/modify real resources in the documentation
space (`settings.docs_space_id`) — point them at a test/staging customer, not
production content you care about.
