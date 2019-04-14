#!/usr/bin/env python3
#
# Script to automate pulling latest lecture notes.

import requests
import yaml
from sys import stdout

base_url = "https://www.cl.cam.ac.uk/teaching/1819/Types"

def url_of_lec(i):
  no_handout = [0,1,3]
  handout_s = "" if i in no_handout else "-handout"
  return "%s/lec-%d%s.pdf" % (base_url, i+1, handout_s)

def lm_of_url(url):
  print("HEAD %s" % url)
  r = requests.head(url)
  if r.status_code != 200:
    print("-> %s" % r)
    return None
  
  lm_hdr = "last-modified"
  if lm_hdr not in r.headers:
    print("-> no Last-Modified header")
    return None

  return r.headers[lm_hdr]

with open("errata.yml", "r") as stream:
  errata = yaml.safe_load(stream)

comb_lm_known = errata["combined"]["last-modified"]
comb_url = "%s/handout.pdf" % base_url
comb_lm = lm_of_url(comb_url)

if comb_lm is None:
  print("Failed to check combined notes for updates.")
elif comb_lm != comb_lm_known:
  print("Combined notes updated @ %s! Last checked @ %s." % (comb_lm, comb_lm_known))
else:
  print("Combined notes not updated, errata still valid.")

for lec in errata["lectures"]:
  lec_num = lec["lecture"]
  lm_known = lec["last-modified"]
  errata_for_lec = lec["errata"]
  lm = lm_of_url(url_of_lec(lec_num-1))
  if lm is None:
    print("Failed to check for updated on lecture %s" % lec_num)
    continue
  if lm != lm_known:
    print("Lecture %s updated! Need to check if errata still valid." % lec_num)
    continue
  print("Lecture %s not updated, errata still valid." % lec_num)
