#!/usr/bin/env python3

class Finder:
  def __init__(self, window):
    self.setWindow(window)

  def setWindow(self, window):
    self.window = window
    self.siblings = self.window.parent.nodes

  def getWindow(self):
    return self.window

  def reverseSiblings(self):
    self.siblings = reversed(self.siblings)
    return self

  def getPrevSibling(self):
    siblings = iter(self.siblings)
    sibling = next(siblings)
    while sibling.id != self.window.id:
      next_sibling = next(siblings)
      if next_sibling.id == self.window.id:
        return sibling
      sibling = next_sibling
    return None

  def getNextSibling(self):
    return (Finder(self.getWindow())
        .reverseSiblings()
        .getPrevSibling())

  def getPrevByFilter(self, doFilter, getSibling=None):
    getSibling = getSibling if getSibling else Finder.getPrevSibling
    window = self.getWindow()
    while window and window.parent:
      prev =  getSibling(Finder(window)) # Finder(window).getSibling()
      if prev and doFilter(prev):
        return prev
      window = window.parent
    return None

  def getNextByFilter(self, doFilter):
    return self.getPrevByFilter(doFilter, Finder.getNextSibling)

  def find(self, **filters):
    for filter in filters:
      if not isinstance(filters[filter], list):
        filters[filter] = [filters[filter]]
    findings = []

    found = True
    for filter in filters:
      if not getattr(self.window, filter, None) in filters[filter]:
        found = False
        break
    if found:
      findings.append(self.window)

    for window in self.window.descendents():
      findings.extend(Finder(window).find(**filters))
    return findings

  def focused_leaves(self):
    leaves = []
    got_active_window = False
    for id in self.window.focus:
      con = self.find(id=id)[0]
      if con.descendents() == []:
        if not got_active_window:
          leaves.append(con)
          got_active_window = True
      else:
        leaves.extend(Finder(con).focused_leaves())
    return leaves
