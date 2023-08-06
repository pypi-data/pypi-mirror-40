
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
from pathlib import Path

HOME_DIR = str(Path.home())
UNSUCKED_APP_DIR = f"{HOME_DIR}/."

TMP_DIR = "/tmp/"
COOKIES_FILE = "/tmp/.bb-unsucked-cookies"
COURSES_CACHE_FILE = "/tmp/.bb-unsucked-course-cache"
# TODO move this to env variable or config file
FIREFOX_COOKIES_SQLITE = "/j/.mozilla/firefox/jaa9h6en.default/cookies.sqlite"
BASE_DOMAIN = "https://www.blackboard.odu.edu"
HOME_DASHBOARD = f"{BASE_DOMAIN}/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1"
TAB_ACTION = f"{BASE_DOMAIN}/webapps/portal/execute/tabs/tabAction"

class BBClass():
  def from_a_link(link: str):
    href = link.split("\"", 1)[1].split("\"", 1)[0].strip()
    if href.startswith("/"):
      href = BASE_DOMAIN + href
    title = link.split(">", 1)[1].split("<", 1)[0].strip()
    return BBClass(href, title)
  
  def __init__(self, url: str, name: str):
    self.url = url
    self.raw_name = name
    name_components = name.split("_") # 201820_SPRING_MSIM495_29614: GAME PHYSICS
    self.six_year = name[:6]
    self.season = name_components[1].strip()
    self.course_id = name.split("_")[2].strip()
    self.human_name = name.split(":", 1)[1].strip() if ":" in name else ""
  
  def nice_name(self):
    return f"{self.course_id}: {self.human_name}"
  
  def is_current(self):
    """ returns True if this class is in the current season/semester """
    now = datetime.datetime.now()
    now_is_fall = now.month >= 7
    now_sixyear = str(now.year-1) + ("10" if now_is_fall else "20")
    
    return self.six_year == now_sixyear
  
  def get_announcements(self, session, cookies):
    r = session.get(self.url, cookies=cookies)
    soup = BeautifulSoup(r.text, "html5lib")
    announcements = []
    # Will hold {"utc_date": "1234566", "htmlcontent", <Soup Element Object>}
    for elm in soup.findAll("div", {"class" : "details"}):
      children = elm.findChildren("p" , recursive=False)
      if len(children) > 0:
        post_timestamp = children[0].text # Posted on: Thursday, January 3, 2019 1:20:22 PM EST
        post_timestamp = correct_bb_timestamp_misc(post_timestamp) # Posted on: Thursday, January 03, 2019 01:20:22 PM EST
        timestamp_fmt = 'Posted on: %A, %B %d, %Y %H:%M:%S %p EST'
        post_epoch_s = int(datetime.datetime.strptime(post_timestamp, timestamp_fmt).strftime("%s"))
        post_containers = elm.findChildren("div", {"class" : "vtbegenerated"}, recursive=True)
        if len(post_containers) > 0:
          announcement_obj = {
            "utc_date": post_epoch_s,
            "htmlcontent": post_containers[0]
          }
          announcements.append(announcement_obj)
    return announcements
  
  def print_announcements(self, session, cookies):
    for announcement in self.get_announcements(session, cookies):
      print(announcement["htmlcontent"].text.strip())
      print("-" * 40)
      print()
    
  
  def __str__(self):
    return self.nice_name()
  
  def __repr__(self):
    return f"BBClass({self.url}, {self.human_name})"

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
    return 99999 # return large age if file does not exist
  now = int(time.time())
  return now - mtime

def put_ff_cookies_into(dest_cookies_file: str, src_ff_sqlite_db: str):
  conn = sqlite3.connect(src_ff_sqlite_db)
  c = conn.cursor()
  cookies = {}
  for row in c.execute("select * from moz_cookies where host = 'www.blackboard.odu.edu';"):
    # moz_cookies table schema:
    # moz_cookies (id INTEGER PRIMARY KEY, baseDomain TEXT, originAttributes TEXT NOT NULL DEFAULT '', name TEXT, value TEXT, host TEXT, path TEXT, expiry INTEGER, lastAccessed INTEGER, creationTime INTEGER, isSecure INTEGER, isHttpOnly INTEGER, inBrowserElement INTEGER DEFAULT 0, sameSite INTEGER DEFAULT 0, CONSTRAINT moz_uniqueid UNIQUE (name, host, path, originAttributes));
    name = row[3]
    value = row[4]
    #print("name="+str(name))
    #print("value="+str(value))
    cookies[name] = value
  
  save_obj(cookies, dest_cookies_file)
  
  conn.close()

def put_har_cookie_into(dest_cookies_file: str, src_file: str):
  cookies = {}
  with open(src_file, 'r') as myfile:
    har_json = json.load( myfile )
    for http_entry in har_json["log"]["entries"]:
      if http_entry["request"]["url"] == "https://www.blackboard.odu.edu/webapps/portal/execute/tabs/tabAction":
        # We want these cookies
        for cookie in http_entry["request"]["cookies"]:
          cookies[cookie["name"]] = cookie["value"]
    
  save_obj(cookies, dest_cookies_file)

def verify_logged_in(html: str):
  logged_in = not ("Please enter your credentials and click the <b>Login</b> button below." in html)
  if not logged_in:
    print(html+"\n\n")
    print("""Error: Blackboard reports you are not logged in.
Please confirm your Firefox profile matches the one
you are uring in your browser, and confirm you have logged in
to blackboard in your browser.
""")
    sys.exit(5)

def tab_action_r(session, cookies, modId: str, tabId: str, tab_tab_group_id: str):
  form_data = {
    "action": "refreshAjaxModule",
    "modId": modId,
    "tabId": tabId,
    "tab_tab_group_id": tab_tab_group_id,
  }
  #form_data = f"action=refreshAjaxModule&modId={modId}&tabId={tabId}&tab_tab_group_id={tab_tab_group_id}"
  headers = {
    'referer': HOME_DASHBOARD,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
  }
  r = session.post(TAB_ACTION, cookies=cookies, data=form_data, headers=headers)
  verify_logged_in(r.text)
  return r

def parse_courses_from_home_dashboard(session, cookies):
  #print("Parsing courses from dashboard...") # cache debugging
  r = tab_action_r(session, cookies, "_4_1", "_1_1", "_1_1")
  courses = []
  for line in r.text.splitlines():
    if "a href=" in line:
      the_class = BBClass.from_a_link(line)
      courses.append(the_class)
  
  return courses

def get_courses_caching(session=None, cookies=None, max_cache_s=(24 * 60 * 60)):
  "Passing session and cookies is optional, and will force a cache-only read."
  if session == None or get_file_age_s(COURSES_CACHE_FILE) < max_cache_s:
    try:
      return load_obj(COURSES_CACHE_FILE)
    except AttributeError as error:
      # This occurs when Python saves the 'BBClass' and Cython tries to load it ('BBClass' gets name-mangled and cannot be restored)
      # The opposite works fine - Python can unpickle a Cython object just fine
      pass
  
  # perform fetch
  courses = parse_courses_from_home_dashboard(session, cookies)
  save_obj(courses, COURSES_CACHE_FILE)
  return courses

def print_all_courses(session, cookies):
  for course in get_courses_caching(session, cookies):
    print(course.nice_name())

def print_curr_courses(session, cookies):
  for course in get_courses_caching(session, cookies):
    if course.is_current():
      print(course.nice_name())

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

def print_announcement_page(session, url, max_age_s=(7 * 24 * 60 * 60)):
  r = session.get(url)
  now_s = int(time.time())
  #print(r.text)
  soup = BeautifulSoup(r.text, "html5lib")
  for elm in soup.findAll("div", {"class" : "details"}):
    children = elm.findChildren("p" , recursive=False)
    if len(children) > 0:
      post_timestamp = children[0].text # Posted on: Thursday, January 3, 2019 1:20:22 PM EST
      post_timestamp = correct_bb_timestamp_misc(post_timestamp) # Posted on: Thursday, January 03, 2019 01:20:22 PM EST
      timestamp_fmt = 'Posted on: %A, %B %d, %Y %H:%M:%S %p EST'
      post_epoch_s = int(datetime.datetime.strptime(post_timestamp, timestamp_fmt).strftime("%s"))
      if now_s - post_epoch_s < max_age_s:
        # print the announcement because it's age is < max_age_s
        post_containers = elm.findChildren("div", {"class" : "vtbegenerated"}, recursive=True)
        if len(post_containers) > 0:
          print("-" * 16)
          print(post_containers[0].text.strip())
          print("")

def print_all_announcements(session, cookies, max_age_s=(7 * 24 * 60 * 60)):
  r = tab_action_r(session, cookies, "_1_1", "_1_1", "_1_1")
  printed_a_hrefs = []
  for line in r.text.splitlines():
    if "h3" in line:
      course_title = line.split(">", 1)[1].split("<", 1)[0]
      print("")
      print(course_title)
      print("=" * len(course_title))
    elif "href=" in line:
      rel_announcements_url = line.split("\"", 1)[1].split("\"", 1)[0].strip()
      abs_url = BASE_DOMAIN + rel_announcements_url
      if abs_url in printed_a_hrefs:
        continue
      printed_a_hrefs.append(abs_url)
      print_announcement_page(session, abs_url, max_age_s)

def print_class_announcements(session, cookies, class_id, max_age_s=(7 * 24 * 60 * 60)):
  for course in get_courses_caching(session, cookies):
    if course.course_id == class_id:
      course.print_announcements(session, cookies)

def load_requests_session_and_cookies():
  """ Loads a requests session, pulling cached cookies if they exist """
  session = requests.Session()
  if not os.path.exists(COOKIES_FILE):
    print(f"No authentication cookies found in {COOKIES_FILE}!")
    print("Please read in your blackboard session cookies by running")
    print("  bb_unsucked build-cache path/to/recent_request.har")
    sys.exit(1)
  cookies = load_obj(COOKIES_FILE)
  
  return session, cookies

def print_help():
  print("""Usage:
  bb-unsucked ls [-a]
    List current semester courses
    -a will print all courses
    
  bb-unsucked announcements [course_id]
  bb-unsucked ann [course_id]
    Print all current announcements.
    if course_id is given (like "CS330") only announcements from that course will be printed.
  
  bb-unsucked build-cache path/to/recent_session.har
    Read cookies from a .har file and store them in a temporary directory

bb-unsucked version 0.0.1, Copyright (C) 2019 Jeffrey McAteer <jeffrey.p.mcateer@outlook.com>
bb-unsucked comes with ABSOLUTELY NO WARRANTY; for details see LICENSE file
""")

