#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
"""Minimal hover tooltip, for widgets whose text can be wider than they are."""

import tkinter as tk


class Tooltip:
    def __init__(self, widget, text_getter, delay_ms=400):
        self.widget = widget
        self.text_getter = text_getter
        self.delay_ms = delay_ms
        self._after_id = None
        self._popup = None
        widget.bind('<Enter>', self._schedule, add='+')
        widget.bind('<Leave>', self._hide, add='+')
        widget.bind('<Destroy>', self._hide, add='+')

    def _schedule(self, event=None):
        self._cancel()
        self._after_id = self.widget.after(self.delay_ms, self._show)

    def _cancel(self):
        if self._after_id is not None:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

    def _show(self):
        text = self.text_getter()
        if not text:
            return
        self._hide()
        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 2
        self._popup = tk.Toplevel(self.widget)
        self._popup.wm_overrideredirect(True)
        self._popup.wm_geometry(f'+{x}+{y}')
        label = tk.Label(self._popup, text=text, background='#ffffe0',
                          relief='solid', borderwidth=1, anchor='w')
        label.pack(ipadx=4, ipady=2)

    def _hide(self, event=None):
        self._cancel()
        if self._popup is not None:
            self._popup.destroy()
            self._popup = None
