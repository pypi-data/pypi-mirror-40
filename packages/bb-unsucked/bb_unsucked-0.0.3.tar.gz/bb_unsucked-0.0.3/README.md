
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

## authentication

To perform the authentication step the most reliable method is to
save a `.har` file of a recent blackboard session. `bb_unsucked` is
capable of parsing authentication session cookies out of the file `recent_request.har`.

![how to save a .har from a browser](howto-save-har.jpg "Saving .HAR")



