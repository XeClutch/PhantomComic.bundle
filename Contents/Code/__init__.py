import os

### PhantomComic for Plex
### Copyright (c) Joshua Ozeri 2017
NAME = "PhantomComic for Plex 0.1"
PREFIX = "/photos/phantomcomic"
### PhantomComic is a Plex channel meant to be ran alongside the PhantomComic for Windows application.
### PhantomComic for Plex simply acts as a reader for the comics downloaded with the Windows application.

def Start():
	ObjectContainer.title1 = NAME

@handler(PREFIX, NAME)
def MainMenu():
	oc = ObjectContainer()
	for (root, comics, files) in os.walk("X:\\Comics\\data"):
		for name in comics:
			oc.add(DirectoryObject(key=Callback(ComicMenu, comic=name), title=open(root + "\\" + name + "\\detail").read()), thumb=R(root + "\\" + name + "\\banner"))
	return oc

@route(PREFIX + "/comicmenu", comic=string)
def ComicMenu(comic):
	oc = ObjectContainer()
	for (root, chapters, files) in os.walk("X:\\Comics\\data\\" + comic + "\\comic"):
		for chapter in chapters:
			oc.add(DirectoryObject(key=Callback(ChapterMenu, _comic=comic, _chapter=chapter), title=("Chapter " + chapter), thumb=(root + "\\" + comic + "\\comic\\" + chapter + "\\001")))
	return oc

@route(PREFIX + "/chaptermenu", _comic=string, _chapter=string)
def ChapterMenu(_comic, _chapter):
	oc = ObjectContainer()
	for (root, dirs, pages) in os.walk("X:\\Comics\\data\\" + _comic + "\\comic\\" + _chapter)
		for page in pages:
			url = (root + "\\" + _comic + "\\comic\\" + _chapter + "\\" + page)
			oc.add(PhotoObject(key=Callback(url), rating_key=url, title=("Page " + page)))
	return oc