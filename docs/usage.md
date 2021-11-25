# Usage

AuroraLog ships as a minimal CLI that leans on plain text and monthly files. The script reads from STDIN when content is omitted so the workflow can be chained into editors or snippets.

```
$ auroralog --tags "mood, focus" --prompt-mood calm --content "Scribbled today's reflections."
Saved entry to .auroralog/journals/2021-10.md
```

Use `--review` to print the current month's entries without creating a new block. The module directories can be installed in development with `pip install -e src` so that the CLI finds the `auroralog` package cleanly.
