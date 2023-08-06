
# bb-unsucked, a Blackboard scripting wrapper
# Copyright (C) 2019 Jeffrey McAteer <jeffrey.p.mcateer@outlook.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


# cython: language_level=3

import sys

if sys.version_info[0] < 3:
  raise Exception("bb-unsucked requires Python 3")

# pip3 install requests beautifulsoup4
import os, pickle, requests
from getpass import getpass
from bs4 import BeautifulSoup
import sqlite3, shutil, time, json
import datetime
import pathlib
import configparser
import subprocess

_HOME_DIR = str(pathlib.Path.home())
# These configuration .ini files will be parsed in order when determining settings
CONFIG_FILES = [
  "/etc/bb-unsucked/config.ini",
  "{}/.bb-unsucked/config.ini".format(_HOME_DIR),
]

# Default config keys and values, if no config .ini files are found
# these are what will be used in BBUnsucked.config
CONFIG = {
  "BASE_DOMAIN": "https://www.blackboard.odu.edu",
  
  "COOKIES_FILE": "{}/.bb-unsucked/cookies.bin".format(_HOME_DIR),
  "AGRESSIVE_CACHING": False, # when True, trade slower beginning for faster future
  
  "COURSES_CACHE_FILE": "{}/.bb-unsucked/courses-cache.bin".format(_HOME_DIR),
  "COURSES_MAX_CACHE_S": 7 * 24 * 60 * 60,
  
  "ANNOUNCEMENTS_CACHE_FILE": "{}/.bb-unsucked/announcements-cache.bin".format(_HOME_DIR),
  "ANNOUNCEMENTS_MAX_CACHE_S": 6 * 60 * 60,
}

#
# Flat methods which perform operations on python values
#

def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

def ensure_dir_exists(dir_path: str):
  if not os.path.exists(dir_path):
    os.makedirs(dir_path)

def ensure_parent_dir_exists(file_path: str):
  ensure_dir_exists(os.path.dirname(file_path))

def read_in_config_file(c_file: str, existing_config: dict):
  """ Mutates and returns existing_config """
  if not os.path.exists(c_file):
    return existing_config
  config = configparser.ConfigParser()
  config.read(c_file)
  for config_key in existing_config.keys():
    if config_key in config['DEFAULT']:
      existing_config[config_key] = config['DEFAULT'][config_key]
  return existing_config

def read_in_all_config(config_files: list):
  our_config = CONFIG.copy()
  for c_file in config_files:
    our_config = read_in_config_file(c_file, our_config)
  return our_config

def save_obj(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def load_obj(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def get_file_age_s(file: str):
  try:
    mtime = os.path.getmtime(file)
  except OSError:
    return 99999999999 # return large age if file does not exist
  now = int(time.time())
  return now - mtime

def logged_in(html: str):
  logged_in = not ("Please enter your credentials and click the <b>Login</b> button below." in html)
  return logged_in

def correct_bb_timestamp_misc(string: str):
  """ For every single-digit in the string, pad it with a 0 so it is 2 digits wide """
  space_pieces = string.split(" ")
  for i in range(0, len(space_pieces)):
    if space_pieces[i] in [ str(c) for c in "1234567890"]:
      space_pieces[i] = "0"+space_pieces[i]
    
    elif space_pieces[i] in [ str(c)+"," for c in "1234567890"]:
      space_pieces[i] = "0"+space_pieces[i]
    
    elif ":" in space_pieces[i] and not space_pieces[i].endswith(":"):
      time_pieces = space_pieces[i].split(":")
      for j in range(0, len(time_pieces)):
        if time_pieces[j] in [ str(c) for c in "1234567890"]:
          time_pieces[j] = "0"+time_pieces[j]
        
      space_pieces[i] = ":".join(time_pieces)
    
  string = " ".join(space_pieces)
  # We assume "est" for all our time strings, it's hardcoded.
  return string.replace("EDT", "EST")

def write_to_interpose_cache(argv, contents):
  """I dislike seeing 300ms be taken to run 'bb-unsucked ls' after it is compiled to cython.
This data is moderately long-term and I can cache it in an easily readable format
so common operations happen without the need to have an entire python engine running.
In order for this to work the path to unsuck's data needs to be $HOME/.bb-unsucked/,
because I'm not parsing multiple .ini files using C.
"""
  # Simple hash function because I need it to be correct and free of 3rd party dependencies
  argv_hash = 0
  for arg in argv:
    for c in arg:
      argv_hash += ord(c)
  output_file = os.environ["HOME"]+"/.bb-unsucked/"+("%d" % argv_hash)+".cbincache"
  ensure_parent_dir_exists(output_file)
  with open(output_file, "w") as file_handle:
    file_handle.write(contents)

def sanitize_for_use_in_filesystem(some_text: str):
  camels = some_text.replace(" ", "_").lower()
  camels = "".join([ # whitelist of OK characters
    c for c in camels if c in "abcdefghijklmnopqrstuvwxyz0123456789-_."
  ])
  camels = camels.replace("__", "_")
  return camels

#
# Objects for use in more complex methods.
# class BBUnsucked is primary API
#


class BBUnsucked():
  """This is a driver class which will handle making sure cookies are forwarded between individual requests.
It will usually be the first thing scripts create, and all unsucked functionality should be reachable through this object.
"""
  
  def __init__(self, config_files=CONFIG_FILES):
    self.config = read_in_all_config(config_files)
    # after this point CONFIG should be considered immutable
    self.session = requests.Session()
  
  def fuse_mount(self, mount_point: str):
    try:
      import bb_unsucked.fuse_fs
      bb_unsucked.fuse_fs.main(mount_point, self)
    except Exception as ex:
      print(ex)
      print()
      print("Could not import bb_unsucked.fuse_fs, do you have fusepy installed?")
      print("try running: sudo pip3 install fusepy")
      
  def clear_caches(self):
    files = [
      self.config["COURSES_CACHE_FILE"],
      self.config["ANNOUNCEMENTS_CACHE_FILE"],
    ]
    for file in files:
      try:
        os.remove(file)
      except:
        pass
  
  def get_cookies(self):
    cookies_file = self.config["COOKIES_FILE"]
    if not os.path.exists(cookies_file):
      err_msg = """No authentication cookies found in {}!
Please read in your blackboard session cookies by running 'bb-unsucked build-cache path/to/recent_request.har'""".format(cookies_file)
      raise RuntimeError(err_msg)
    return load_obj(cookies_file)
  
  def get_tab_action_url(self):
    base = self.config["BASE_DOMAIN"]
    return "{}/webapps/portal/execute/tabs/tabAction".format(base)
  
  def verify_logged_in(self):
    try:
      self._parse_courses_from_home_dashboard()
      return True
    except:
      return False
  
  def import_har(self, harfile: str):
    cookies = {}
    base = self.config["BASE_DOMAIN"]
    with open(harfile, 'r') as file_handle:
      har_json = json.load( file_handle )
      for http_entry in har_json["log"]["entries"]:
        if http_entry["request"]["url"] == "{}/webapps/portal/execute/tabs/tabAction".format(base):
          # We want these cookies
          for cookie in http_entry["request"]["cookies"]:
            cookies[cookie["name"]] = cookie["value"]
    
    ensure_parent_dir_exists(self.config["COOKIES_FILE"])
    save_obj(cookies, self.config["COOKIES_FILE"])
    return cookies
  
  def tab_action_r(self, modId: str, tabId: str, tab_tab_group_id: str):
    form_data = {
      "action": "refreshAjaxModule",
      "modId": modId,
      "tabId": tabId,
      "tab_tab_group_id": tab_tab_group_id,
    }
    host_base = self.config["BASE_DOMAIN"]
    headers = {
      'referer': self.get_tab_action_url(),
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    r = self.session.post(self.get_tab_action_url(), cookies=self.get_cookies(), data=form_data, headers=headers)
    if not logged_in(r.text):
      raise RuntimeError("your cookies do not correspond to a valid Blackboard session. Please run 'bb-unsucked build-cache path/to/recent_session.har' and try again.")
    return r
  
  def _parse_courses_from_home_dashboard(self):
    #print("Parsing courses from dashboard...") # cache debugging
    r = self.tab_action_r("_4_1", "_1_1", "_1_1")
    courses = []
    for line in r.text.splitlines():
      if "a href=" in line:
        the_class = BBClass.from_a_link(line, config=self.config)
        if self.config["AGRESSIVE_CACHING"]:
          the_class.cache_as_much_as_possible(self.session, self.get_cookies())
        courses.append(the_class)
    return courses
  
  def classes(self):
    # self.config["COURSES_MAX_CACHE_S"]
    if get_file_age_s(self.config["COURSES_CACHE_FILE"]) < self.config["COURSES_MAX_CACHE_S"]:
      try:
        return load_obj(self.config["COURSES_CACHE_FILE"])
      except (AttributeError, ModuleNotFoundError) as error:
        # This occurs when Python saves the 'BBClass' and Cython tries to load it ('BBClass' gets name-mangled and cannot be restored)
        # The opposite works fine - Python can unpickle a Cython object just fine
        pass
    # Fall back to querying BB for courses, saving them for the future
    courses = self._parse_courses_from_home_dashboard()
    save_obj(courses, self.config["COURSES_CACHE_FILE"])
    return courses
  
  def current_classes(self):
    return [clazz for clazz in self.classes() if clazz.is_current()]

  def fuzzy_class_by_course_id(self, course_id):
    course_id = course_id.lower()
    for clazz in self.classes():
      if course_id in clazz.course_id.lower():
        return clazz
    return None

class BBClass():
  """" This class represents a single blackboard course. Specifically, a specific instance of a course (eg CS417 SPRING 2019) """
  
  def from_a_link(link: str, config: dict = CONFIG):
    """ Build a BBClass() from an <a> link that blackboard provides """
    href = link.split("\"", 1)[1].split("\"", 1)[0].strip()
    title = link.split(">", 1)[1].split("<", 1)[0].strip()
    return BBClass(href, title, config=config)
  
  def __init__(self, url: str, name: str, config: dict = CONFIG):
    """url may be relative, if so the value of BASE_DOMAIN in the config parameter will be added to make it absolute.
name must be of the form '201820_SPRING_MSIM495_29614: GAME PHYSICS' because it it parsed into components."""
    self.config = config
    if url.startswith("/"):
      url = self.config["BASE_DOMAIN"] + url
    self.url = url
    self.raw_name = name
    name_components = name.split("_") # 201820_SPRING_MSIM495_29614: GAME PHYSICS
    self.six_year = name[:6]
    self.season = name_components[1].strip()
    self.course_id = name.split("_")[2].strip()
    self.human_name = name.split(":", 1)[1].strip() if ":" in name else ""
    # sidebar_links are objects of {"url":"https://url.com", "text": "Human Name"}
    self.sidebar_links = []
  
  def cache_as_much_as_possible(self, session, cookies):
    """Uses web session to cache as much data as possible"""
    self.get_sidebar_links(session, cookies)
  
  def nice_name(self):
    return "{}: {}".format(self.course_id, self.human_name)
  
  def file_name(self):
    """ Returns name suitable for use in FUSE filesystem """
    camels = sanitize_for_use_in_filesystem(self.human_name)
    lower_course_id = self.course_id.lower()
    return "{}_{}".format(lower_course_id, camels)
  
  def is_current(self):
    """ returns True if this class is in the current season/semester """
    now = datetime.datetime.now()
    now_is_fall = now.month >= 7
    now_sixyear = str(now.year-1) + ("10" if now_is_fall else "20")
    
    return self.six_year == now_sixyear
  
  def announcements(self, session, cookies):
    if get_file_age_s(self.config["ANNOUNCEMENTS_CACHE_FILE"]) < self.config["ANNOUNCEMENTS_MAX_CACHE_S"]:
      try:
        return load_obj(self.config["ANNOUNCEMENTS_CACHE_FILE"])
      except AttributeError as error:
        # This occurs when Python saves the 'BBClass' and Cython tries to load it ('BBClass' gets name-mangled and cannot be restored)
        # The opposite works fine - Python can unpickle a Cython object just fine
        pass
    # Fall back to querying BB for courses, saving them for the future
    announcements = self._get_announcements(session, cookies)
    save_obj(announcements, self.config["ANNOUNCEMENTS_CACHE_FILE"])
    return announcements
  
  def _get_announcements(self, session, cookies):
    r = session.get(self.url, cookies=cookies)
    soup = BeautifulSoup(r.text, "html5lib")
    announcements = []
    # Will hold BBAnnouncement objects
    for elm in soup.findAll("div", {"class" : "details"}):
      children = elm.findChildren("p" , recursive=False)
      if len(children) > 0:
        post_timestamp = children[0].text # Posted on: Thursday, January 3, 2019 1:20:22 PM EST
        post_timestamp = correct_bb_timestamp_misc(post_timestamp) # Posted on: Thursday, January 03, 2019 01:20:22 PM EST
        timestamp_fmt = 'Posted on: %A, %B %d, %Y %H:%M:%S %p EST'
        post_epoch_s = int(datetime.datetime.strptime(post_timestamp, timestamp_fmt).strftime("%s"))
        post_containers = elm.findChildren("div", {"class" : "vtbegenerated"}, recursive=True)
        if len(post_containers) > 0:
          announcements.append(
            BBAnnouncement(post_epoch_s, post_containers[0])
          )
    return announcements
  
  def _get_sidebar_links(self, session, cookies):
    r = session.get(self.url, cookies=cookies)
    soup = BeautifulSoup(r.text, "html5lib")
    sidebar_links = []
    for elm in soup.findAll("a"):
      if elm["href"].startswith("/webapps/blackboard/content/"):
        url = elm["href"].strip()
        if url.startswith("/"):
          url = self.config["BASE_DOMAIN"] + url
        sidebar_links.append({
          "url": url,
          "text": elm.text.strip()
        })
      
    return sidebar_links
  
  def get_sidebar_links(self, session, cookies):
    if len(self.sidebar_links) < 1:
      self.sidebar_links = self._get_sidebar_links(session, cookies)
    # todo signal class save?
    return self.sidebar_links
  
  def content(self, session, cookies):
    for sidebar_elm in self.get_sidebar_links(session, cookies):
      print("todo query "+str(sidebar_elm))
  
  def __str__(self):
    return self.nice_name()
  
  def __repr__(self):
    return "BBClass({}, {})".format(self.url, self.human_name)

class BBAnnouncement():
  """ Represents a single BB announcement """
  
  def __init__(self, utc_date: int, htmlcontent):
    self.utc_date = utc_date
    self.text = htmlcontent.text.strip()
    #self.htmlcontent = htmlcontent
  
  def print(self):
    print(self.text)

