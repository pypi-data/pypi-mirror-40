# wowlint
## Linter for Words of Worship resource files

[![Build Status](https://travis-ci.org/jamesremuscat/wowlint.svg?branch=master)](https://travis-ci.org/jamesremuscat/wowlint)
[![Coverage Status](https://coveralls.io/repos/github/jamesremuscat/wowlint/badge.svg?branch=master)](https://coveralls.io/github/jamesremuscat/wowlint?branch=master)

[Words of Worship](http://www.wordsofworship.com) is a popular tool for
projecting song lyrics, liturgy and other textual media in churches and houses
of worship.

`wowlint` aims to provide a mechanism to assure quality and consistency of
the song and liturgy resource files, by automatically verifying things like:

 - Lines start with a capital letter
 - Copyright and author information is provided
 - Lines do not have trailing punctuation

The validation criteria are unashamedly based on the house style of
[St Aldates Church](https://github.com/staldates).

## Basic usage

```shell
$ wowlint [ options ] /path/to/some/wow/files/*.wow-song
```
For help with options, run:

```shell
$ wowlint --help
```

### Runtime options

* **-e**, **--errors-only**: Just show errors, don't run lints that give warnings.
* **-l**, **--list**: Just list files that fail validation, not the details. Implies `-S`.
* **-S**, **--no-summary**: Don't show a summary (number of files, errors, etc) at the end of the output.

## Configuration

Per-lint configuration is possible by creating a `wowlintrc.yml` file in the
directory from which you run `wowlint`. This should be a YAML file with lint
names as keys and per-lint configuration as values.

All lints accept the `exclude` key, which should be a list of filenames to be
excluded from that lint. For example, to exclude the `test.wsg` file from the
`NoAuthorProvided` lint, your `wowlintrc.yml` should contain:

```yaml
NoAuthorProvided:
  exclude:
    - "test.wsg"
```

### Per-lint configuration options

#### LineTooLong
Words of Worship has trouble displaying very long lines of text if, when
the line is wrapped, it occupies more lines than are visible on the screen.
A "safe" line length therefore depends on your display settings.

* **max_length**: Maximum line length. Defaults to 200.

#### SpellCheck
* **lang**: Language to use for spell-checking. Must refer to an available
  dictionary on your system (e.g. on Linux, a dictionary that can be used by
  `aspell` via `enchant`). Defaults to `en_GB`.

## Advanced usage

It's possible to use `wowlint` as a WoW-to-text converter by dumping the
internal representation of a WoW file to stdout, by running:

```shell
$ python -m wowlint.wowfile [filename]
```
Note that this currently only works with song and liturgy resource files.

### git diff

It's therefore possible to configure `git` to display a diff of the binary WoW
file format!

You'll need to add the following to `.gitattributes`:

```
*.wsg diff=wow
*.wow-song diff=wow
```

Then you can configure `git` with the following:

```shell
$ git config --local diff.wow.textconv "python -m wowlint.wowfile"
```

Note that due to security implications, the latter must be run for each clone
of your song files repository; you can't commit it, as you can with
`.gitattributes`.

## Limitations

Currently this project is very young, and:
 - Only song files (`.wsg` and `.wow-song`) and liturgy files (`.wlt` and
   `.wow-liturgy`) are supported
 - There's no way to specify custom validation or disable entire rules
 - Automating the running of `wowlint` is left as an exercise for the user

# Contributions

Contributions welcome: please fork the project and submit a pull request.
