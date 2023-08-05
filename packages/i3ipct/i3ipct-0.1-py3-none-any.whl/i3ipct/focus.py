#!/usr/bin/env python3

from .find import Finder
import i3ipc
import sys

class Focus:
  def __init__(self, current_window):
    self.window = current_window
    self.allowed_parent_layouts = ['tabbed']
    self.allowed_window_types = ['con']
    self.finder_method = Finder.getNextByFilter

  def setAllowedParentLayouts(self, layouts):
    self.allowed_parent_layouts = layouts
    return self

  def setAllowedWindowTypes(self, types):
    self.allowed_window_types = types
    return self

  def filter(self, window):
    return (
      window.type in self.allowed_window_types
      and window.parent
      and window.parent.layout in self.allowed_parent_layouts
    )

  def setFinderMethod(self, method):
    self.finder_method = method
    return self

  def focusActiveWindowIn(self, container):
    if container:
      if len(container.leaves()) > 0:
        i3 = i3ipc.Connection()
        focused = Finder(container).focused_leaves()
        focused[0].command('focus')
      else:
        container.command('focus')

  def findAndFocus(self):
    container = self.finder_method(Finder(self.window), self.filter)
    self.focusActiveWindowIn(container)
    return self

  def right(self):
    (self
      .setAllowedParentLayouts(['splith'])
      .setFinderMethod(Finder.getNextByFilter)
      .findAndFocus())

  def left(self):
    (self
      .setAllowedParentLayouts(['splith'])
      .setFinderMethod(Finder.getPrevByFilter)
      .findAndFocus())

  def nextTabOrDown(self):
    (self
      .setAllowedParentLayouts(['splitv', 'tabbed'])
      .setFinderMethod(Finder.getNextByFilter)
      .findAndFocus())

  def prevTabOrUp(self):
    (self
      .setAllowedParentLayouts(['splitv', 'tabbed'])
      .setFinderMethod(Finder.getPrevByFilter)
      .findAndFocus())
