
# Blackboard Unsucked

_crummy name for a fix of crummy software_

If you are a student or faculty at ODU I'm sure you're no stranger
to wasting 2-3 hours a day trying to find or post assignments via BlackBoard.

I am concerned with the student's view, but I hope this experiment can
prove useful for professors as well. The goal is to wrap around existing
BlackBoard infrastructure and provide a CLI API to access all the important functions
which usually are trapped behind 4-5 links and a total 20-30 second browser load time.

# Specific Goals

 - [x] Login to BB
 - [x] List classes for the current semester only (hide irrelevant ones)
 - [x] List all announcements
 - [x] List assignments for a given class
  - This will have to be sort of intelligent as professors put assignments in different places
 - [ ] Submit files for assignments
 - [ ] View/Post to discussion boards
 - [ ] Caching and Daemon operation, to prevent having to hit the network for most data access


# Dependencies

Python3 `requests`, and `BeautifulSoup`, both of which can be 
installed via `pip3`

# Usage

The fastest setup is to save a `.har` file of a recent Blackboard session someplace,
then run

```bash
# Install the package
pip3 install --user bb_unsucked
# Read authentication details from .har
python3 -m bb_unsucked build-cache downloads/my-session.har
# use the __main__.py program to list all of your classes
python3 -m bb_unsucked ls
```

## in a script

the file `demo_usage_in_script.py` has more examples, but the hello world is:

```python
import bb_unsucked

bb = bb_unsucked.BBUnsucked()

for my_class in bb.classes():
  print(f"I am in {my_class.course_id}")

```

## authentication

To perform the authentication step the most reliable method is to
save a `.har` file of a recent blackboard session. `bb_unsucked` is
capable of parsing authentication session cookies out of the file `recent_request.har`.

![how to save a .har from a browser](howto-save-har.jpg "Saving .HAR")


## Config

`bb-unsucked` reads from config directives first from `/etc/bb-unsucked/config.ini`
and then from `$HOME/.bb-unsucked/config.ini`. Neither file need to be present,
but should you want to override a parameter the default config contents would be

```
[DEFAULT]
base_domain = https://www.blackboard.odu.edu
cookies_file = /j/.bb-unsucked/cookies.bin
agressive_caching = False
courses_cache_file = /j/.bb-unsucked/courses-cache.bin
courses_max_cache_s = 604800
announcements_cache_file = /j/.bb-unsucked/announcements-cache.bin
announcements_max_cache_s = 21600

```

As you can see, the `base_domain` defaults to ODU's blackboard instance,
but this can be changed to point to any blackboard instance.

My config lists various cache files as being under `/j/` (my home dir)
because when using defaults `bb-unsucked` will dynamically generate the
values of `cookies_file`, `courses_cache_file`, and  `announcements_cache_file`.

# Compiling cython binary

Some speed demons will want to optimize performance as much as possible, esp.
if `bb-unsucked` is going to be used in other scripts. This repo contains
a makefile which will build the binary `bb-unsucked` when you execute `make bb-unsucked`.

The binary outperforms the python module most effectively when reading
cached data which requires no network access. It does this by inserting some code,
`cython_main_interpose.c`, in the generated `.c` file that Cython outputs.

This code is responsible for trying to perform simple tasks without
the need to jump into a python runtime. good examples are printing help text and listing classes,
which the module takes 200ms doing and the binary takes 2ms to do.


