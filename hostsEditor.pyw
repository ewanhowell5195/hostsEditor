from tkinter import Tk, Frame, Listbox, Scrollbar, Label, END, messagebox
from os import path, startfile, system, stat
from stat import FILE_ATTRIBUTE_HIDDEN
from tkinter.ttk import Button, Entry
from ctypes import windll
from time import sleep
from re import search
import sys

if hasattr(sys, "_MEIPASS"):
	basePath = sys._MEIPASS
else:
	basePath = path.abspath(".")

colours = {
	"background": "#F2F2F2",
	"backgroundAlt": "#FFF"
}

file = "C:/Windows/System32/drivers/etc/hosts"

topText = """# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host

# localhost name resolution is handled within DNS itself.
#	127.0.0.1       localhost
#	::1             localhost
"""

def is_admin():
	try:
		return windll.shell32.IsUserAnAdmin()
	except:
		return False

def resourcePath(relativePath):
	return path.join(basePath, relativePath)

def start():
	global gui
	gui = Tk()
	gui.title("hostsEditor")
	gui.geometry("720x480")
	gui.resizable(False, False)
	gui.iconbitmap(resourcePath("files/icon.ico"))
	main()
	gui.mainloop()

def main():
	frame = Frame(gui, highlightbackground = "#7A7A7A", highlightthickness = 1, bg = colours["background"])
	frame.place(x = 11, y = 280)
	Button(gui, text = "Open Containing Folder", width = 22, cursor = "hand2", command = lambda: startfile(path.dirname(file))).place(x = 10, y = 446)
	Button(gui, text = "Save & Quit", width = 14, cursor = "hand2", command = saveExit).place(x = 616, y = 446)
	lines = []
	with open(file) as f:
		data = f.read().split("\n")
	for line in data:
		if line != "" and not line.startswith("#"):
			lines.append(line)
	listBoxBar(10, 10, 701, 427, lines)

def isHidden(filepath):
    return bool(stat(filepath).st_file_attributes & FILE_ATTRIBUTE_HIDDEN)

def saveExit():
	if messagebox.askokcancel("Save & Quit", "Are you sure you want to save and quit?"):
		if isHidden(file):
			system("attrib -h " + file)
			sleep(1)
		lines = listbox.get(0, END)
		with open(file, "w") as f:
			f.write(topText)
			for line in lines:
				f.write("\n" + line)
		gui.destroy()

def listBoxBar(x, y, width, height, defaultItems = None):
	global listbox
	frame = Frame(gui, width = width, height = height, bg = colours["background"])
	frame.pack_propagate(False)
	listFrame = Frame(frame, bg = colours["background"])
	listFrame.pack(side = "left", fill = "both")
	entryFrame = Frame(listFrame, height = 26, bg = colours["background"])
	entryFrame.pack_propagate(False)
	entryFrame.pack(side = "top", fill = "x")
	ipEntry = Entry(entryFrame)
	ipEntry.pack(side = "left", fill = "both", expand = 1)
	ipEntry.insert(0, "Enter IP Address...")
	def onIPClick(event):
		ipEntry.delete(0, END)
		ipEntry.unbind("<Button-1>", ipEntryID)
	ipEntryID = ipEntry.bind("<Button-1>", onIPClick)
	domainEntry = Entry(entryFrame)
	domainEntry.pack(side = "left", fill = "both", expand = 1)
	domainEntry.insert(0, "Enter Domain Name...")
	def onDomainClick(event):
		domainEntry.delete(0, END)
		domainEntry.unbind("<Button-1>", domainEntryID)
	domainEntryID = domainEntry.bind("<Button-1>", onDomainClick)
	listBoxFrame = Frame(listFrame, highlightbackground = "#7A7A7A", highlightthickness = 1, bg = colours["backgroundAlt"])
	listBoxFrame.pack(side = "bottom", fill = "both", expand = 1)
	listbox = Listbox(listBoxFrame, width = ((width) // 7 - 2) - 4, bd = 0, bg = colours["backgroundAlt"], highlightthickness = 0, font = ("Courier New", 9))
	listbox.pack(side = "left", fill = "y")
	if defaultItems != None:
		for item in defaultItems:
			listbox.insert(END, item)
		listbox.yview(END)
	scrollbar = Scrollbar(listBoxFrame)
	scrollbar.pack(side = "right", fill = "y")
	listbox.config(yscrollcommand = scrollbar.set)
	scrollbar.config(command = listbox.yview)
	buttonFrame = Frame(frame, bg = colours["background"])
	buttonFrame.pack(side = "right", fill = "both", expand = 1)
	def addItemToListbox():
		ip = ipEntry.get()
		domain = domainEntry.get()
		if ip == "" or domain == "":
			return messagebox.showerror(title = "Invalid inputs", message = "You need to enter both an IP address and a domain name")
		if " " in ip or " " in domain:
			return messagebox.showerror(title = "Invalid inputs", message = "You cannot use spaces in the IP address or domain name")
		if not search(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
			return messagebox.showerror(title = "Invalid IP address", message = "The provided IP address is invalid")
		if not "." in domain or not all([ord(x) < 256 for x in domain]):
			return messagebox.showerror(title = "Invalid domain name", message = "The provided domain name is invalid")
		ipEntry.delete(0, END)
		domainEntry.delete(0, END)
		text = f"{ip} {domain}"
		values = listbox.get(0, END)
		for item in values:
			if domain == item.split(" ")[1]:
				return messagebox.showerror(title = "Domain already in use", message = "That domain name is already in use")
		if text in values:
			return messagebox.showerror(title = "Value already exists", message = "That IP address and domain name already exists")
		listbox.insert(END, text)
		listbox.yview(END)
	def removeItemFromListbox():
		if len(listbox.curselection()) != 0:
			text = listbox.get(listbox.curselection())
			listbox.delete(listbox.curselection())
	def resetListbox():
		listbox.delete(0, END)
		if defaultItems != None:
			defaultItems.sort()
			for item in defaultItems:
				listbox.insert(END, item)
			listbox.yview(END)
	Button(buttonFrame, text = "+", cursor = "hand2", command = addItemToListbox).pack(side = "top", fill = "x")
	Button(buttonFrame, text = "-", cursor = "hand2", command = removeItemFromListbox).pack(side = "top", fill = "both", expand = 1)
	Button(buttonFrame, text = "↺", cursor = "hand2", command = resetListbox).pack(side = "top", fill = "both", expand = 1)
	frame.place(x = x, y = y)
	return listbox

if is_admin():
	start()
else:
	windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)