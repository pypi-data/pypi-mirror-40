
from bb_unsucked import * # WILDCARD_REMOVE_FOR_CYTHON_BUILD

if len(sys.argv) < 2:
  print_help()
  sys.exit(1)

cmd = sys.argv[1]

if cmd == "build-cache":
  if len(sys.argv) > 2:
    harfile = sys.argv[2]
    put_har_cookie_into(COOKIES_FILE, harfile)
    # TODO can we verify BB accepts the cookies?
    sys.exit(0)
  else:
    print("File argument required")
    sys.exit(1)

session = requests.Session()
if not os.path.exists(COOKIES_FILE):
  print(f"No authentication cookies found in {COOKIES_FILE}!")
  print("Please read in your blackboard session cookies by running")
  print("  bb_unsucked build-cache path/to/recent_request.har")
  sys.exit(1)
cookies = load_obj(COOKIES_FILE)

if cmd == "ls":
  if len(sys.argv) > 2 and sys.argv[2] == "-a":
    print_all_courses(session, cookies)
  else:
    print_curr_courses(session, cookies)

elif cmd == "announcements" or cmd == "ann":
  if len(sys.argv) > 2:
    course_id = sys.argv[2].upper()
    print_class_announcements(session, cookies, course_id)
    
  else:
    print_all_announcements(session, cookies)
  

else:
  print(f"Unknown command '{cmd}'")
  print_help()
  sys.exit(1)
