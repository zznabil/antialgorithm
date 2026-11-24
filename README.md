<p align="center">
  <img src=".claude-plugin/icon.png" width="140" height="140" alt="Orange bell curve with one point far out on its tail">
</p>

# antialgorithm

<p align="center">
  <a href="https://github.com/mankidev/antialgorithm/releases"><img src="https://img.shields.io/github/v/release/mankidev/antialgorithm?color=F07A1E&labelColor=171717" alt="Latest release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/mankidev/antialgorithm?color=F07A1E&labelColor=171717" alt="MIT license"></a>
  <a href="https://github.com/mankidev/antialgorithm/stargazers"><img src="https://img.shields.io/github/stars/mankidev/antialgorithm?color=F07A1E&labelColor=171717" alt="GitHub stars"></a>
</p>

<p align="center"><sub>English | <a href="docs/README_TR.md">Türkçe</a> | <a href="docs/README_ZH.md">简体中文</a> | <a href="docs/README_JA.md">日本語</a> | <a href="docs/README_KO.md">한국어</a> | <a href="docs/README_ES.md">Español</a> | <a href="docs/README_PT.md">Português</a> | <a href="docs/README_DE.md">Deutsch</a> | <a href="docs/README_FR.md">Français</a> | <a href="docs/README_RU.md">Русский</a></sub></p>

![Six posters without the skill on top, six with it below](images/showcase.png)

Agent skill for creative work: names, story, game ideas, posters, UI. It makes the model name its first, most average pick, then move away from it for a reason taken from the project.

Both rows came from the same prompt: `Design a poster for a music festival as a 400x600 SVG. Save the final SVG as final.svg in the current folder.` The top row is one batch of six runs without the skill, none left out. The bottom row is picked from about a dozen runs made while the skill was still being written.

![Chart of how often a choice gets picked: a tall peak around the average marked as the safe zone, flat on both sides](images/graph.png)

## Install

The [skills](https://github.com/vercel-labs/skills) CLI puts it where your agent reads skills, for Codex, Cursor, OpenCode, Claude Code and others:

```
npx skills add mankidev/antialgorithm
```

Or clone it into your agent's skills folder:

```
git clone https://github.com/mankidev/antialgorithm <skills folder>/antialgorithm
```

In Claude Code it also installs as a plugin (on versions before 2.1.275, run `/plugin marketplace add mankidev/antialgorithm` first):

```
/plugin install antialgorithm --marketplace mankidev/antialgorithm
```

`antialgorithm` is one static binary with no runtime. Get it from the [releases](https://github.com/mankidev/antialgorithm/releases), or build it with `cargo install --path cli`. Put it on your `PATH`. Every command takes `--help`. Exit codes: 0 ok, 1 `check` found problems, 2 bad input.

## Commands

`antialgorithm seed visual|text|idea` rolls a starting point when the request is thin. A visual seed gives a making method, colors, layout, type, a verb and a scale for the idea, a setting, a region and, half the time, an object. A text seed gives a voice, a way in and a register. An idea seed gives a verb, a constraint, a scale and a pressure. It draws from system randomness, so two people sending the same prompt start in different places. It also saves each seed to `~/.local/state/antialgorithm/history.jsonl` (under `$XDG_STATE_HOME` when that is set, or at `$ANTIALGORITHM_HISTORY`) and skips values from the last few, so your own seeds don't repeat from one session to the next. `--keep "axis=value"` holds an axis fixed, `--only axis` rolls one axis again, `--no-log` skips saving, `--json` prints JSON.

`antialgorithm moves` keeps a short log of the main move behind each off-default answer, such as "neon tube wall, almost no type". The model reads it before showing new work, so it doesn't reuse a move that worked last time just because it worked. `moves add "text"` saves one.

`antialgorithm rough in.svg out.svg` shakes the straight lines, shapes and letters of an SVG, and breaks the even spacing of repeated marks, so a hand-made look drawn in code stops looking plotted. It is only for hand-made methods such as print, paint, stamps and ink; screen, camera and render looks keep their own marks. `--seed N` makes the result repeat.

`antialgorithm check file.svg` renders an SVG at full size and at icon size and lists text that runs off an edge, sits under a shape, has low contrast or is too small. The size limit fits posters; for an app screen use `--min-text 0.6`. `--json` prints JSON.

`antialgorithm skill [visuals]` prints the skill text built into the binary.

Visual rules live in `visuals.md`, which the model reads only for visual work, so a name or a slogan doesn't load them.

## License

MIT

## Star History

<a href="https://star-history.com/#mankidev/antialgorithm&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=mankidev/antialgorithm&type=Date&theme=dark">
    <img src="https://api.star-history.com/svg?repos=mankidev/antialgorithm&type=Date" alt="Star history chart for mankidev/antialgorithm">
  </picture>
</a>
