#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
"""Generic Tk widget-tree cloning.

Used to duplicate PAGE-generated widget subtrees at runtime (populating the
two empty channel frames from the fully-designed one, and duplicating a
whole PSU panel when a second power supply is found) without hand-editing
the PAGE-generated GUI file.
"""

import tkinter as tk

_SKIP_OPTIONS = {'textvariable', 'variable', 'command', 'menu', 'class'}


def _clone_options(src):
    opts = {}
    for name in src.keys():
        if name in _SKIP_OPTIONS:
            continue
        try:
            value = src.cget(name)
        except tk.TclError:
            continue
        if value == '':
            continue
        opts[name] = value
    return opts


def apply_options(dest_widget, src_widget):
    """Copy src_widget's current configure() options onto dest_widget.

    Public so callers can match a hand-created top-level clone (e.g. a
    second PSU panel's own frame) to its source widget's look, the same way
    clone_widget_tree does for everything underneath it.
    """
    for name, value in _clone_options(src_widget).items():
        try:
            dest_widget.configure({name: value})
        except tk.TclError:
            pass


def clone_widget_tree(src_widget, dest_parent, clone_map=None):
    """Recursively clone src_widget's children under dest_parent.

    Copies each child's class, its current configure() options (except
    textvariable/variable/command/menu, which must stay independent per
    clone rather than being shared), and its place() geometry.

    Returns a dict mapping every original widget encountered to its clone,
    so callers can look up where a specific named widget (e.g. self.Entry1)
    ended up in the clone instead of relying on child ordering.
    """
    if clone_map is None:
        clone_map = {}

    for child in src_widget.winfo_children():
        new_widget = child.__class__(dest_parent)
        apply_options(new_widget, child)

        place_info = child.place_info()
        if place_info:
            # Drop 'in': place_info() resolves it to the original master
            # widget, not dest_parent. Omitting it defaults to the clone's
            # own master, which is dest_parent - exactly what we want.
            place_info = {k: v for k, v in place_info.items() if k != 'in'}
            new_widget.place(**place_info)

        clone_map[child] = new_widget

        if child.winfo_children():
            clone_widget_tree(child, new_widget, clone_map)

    return clone_map
