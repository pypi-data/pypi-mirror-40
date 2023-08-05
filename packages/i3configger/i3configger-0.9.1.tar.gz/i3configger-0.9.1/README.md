[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Build Status](https://travis-ci.org/obestwalter/i3configger.svg?branch=master)](https://travis-ci.org/obestwalter/i3configger)
[![PyPI version](https://badge.fury.io/py/i3configger.svg)](https://pypi.org/project/i3configger/)
[![Documentation](https://img.shields.io/badge/docs-sure!-brightgreen.svg)](http://oliver.bestwalter.de/i3configger)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# i3configger

**Disclaimer:** this is a tool aimed at users who already know how the configuration of [i3](https://i3wm.org) works (as described in the [excellent docs](https://i3wm.org/docs/userguide.html)). `i3configger` is an independent add-on, not directly affiliated with the project and in no way necessary to use i3 productively.

**NOTE** using `i3configger` will replace your existing config files (`config` and optional status bar configs), but it will move them to `<original-name>.bak` if no backup exists yet, so that you can easily revert the damage if you want to go back to your old files.

## Why?

I wanted to be able to switch between different color themes and do things like hide the i3bar with a keyboard shortcut. `i3configger` makes this and other dynamic changes possible without changing i3wm itself.

## Main characteristics

* [same config language as i3](https://i3wm.org/docs/userguide.html#configuring) with these differences:
    * possibility to spread config over several files
    * possibility to assign variables to variables
    * variables in i3status configs are also resolved (set them anywhere in the sources)
* additional configuration of `i3configger` itself and persistence of changes to the i3 configuration is achieved by sprinkling a bit of json on top of the config files.
* command line driven - activities can be bound to keyboard shortcuts directly or as part of a [binding mode](https://i3wm.org/docs/userguide.html#binding_modes)

## How?

In the end i3wm needs a config file it can cope with and it needs to reload or restart, when something changes.

This is realized by adding a build step that can be triggered by calling `i3configger` directly or by running it as a \[daemonized\] watcher process that automatically rebuilds and reloads when source files change or messages are sent.

## What can I do with it?

### Switch between arbitrary "schemes"

You can switch sub configurations (e.g. different color schemes) that conform with a simple naming convention (`config.d/<key>.<value1>.conf`, `config.d/<key>.<value2>.conf`, etc.) by invoking e.g. `i3configger select-next <key>` or `i3configger select <key> <value2>`.

To get an idea what can be done, have a look at the [examples](https://github.com/obestwalter/i3configger/tree/master/examples) and [read the docs](http://oliver.bestwalter.de/i3configger).

### Override any variable

You can change any variable you have defined in the configuration by invoking `i3configger set <variable name> <new value>`. These changes are persisted not in the config itself but in an additional file.

See [i3configger docs](http://oliver.bestwalter.de/i3configger/concept/) for a detailed explanation of the concept and other possible commands.

### Usage example

Here is a snippet from an i3 config that uses a mode to alter itself by sending messages to `i3configger`:

```text
set $i3cBin ~/.virtualenvs/i3/bin/i3configger

bindsym $win+w mode "i3configger"
mode "i3configger" {
    bindsym Right exec "$i3cBin select-next colors --i3-refresh-msg restart"
    bindsym Left exec "$i3cBin select-previous colors --i3-refresh-msg restart"
    bindsym Up exec "$i3cBin shadow bars:targets:laptop:mode dock"
    bindsym Down exec "$i3cBin shadow bars:targets:laptop:mode hide"
    bindsym Return mode "default"
    bindsym Escape mode "default"
}
```

**Explanation of the messages used:**

* `select[...]` integrates different config partials and can therefore make broad changes. In this case for example there are different `colors.<value>.conf` partials that activate different color schemes
* `shadow` adds an overlay that in this case changes the mode of the laptop bar between `hide` and `dock`

## Installation

    $ pip install i3configger

See [docs](http://oliver.bestwalter.de/i3configger/installation) For more details and different ways of installation.

## Some inspiration from the i3 project

... that I would also like to heed for this project:

> * Never break configuration files or existing workflows. Breaking changes require a major version bump (v4 → v5).
> * Keep mental complexity low: once you know i3’s key features, other features should be easy to understand.
> * Only add features which benefit many people, instead of going to great lengths to support rarely used workflows.
> * Only documented behavior is supported. Clear documentation is a requirement for contributions.
