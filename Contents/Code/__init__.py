import os

### PhantomComic for Plex
### Copyright (c) Joshua Ozeri 2017
NAME = "PhantomComic"
PREFIX = "/photos/phantomcomic"
### PhantomComic is a Plex channel meant to be ran alongside the PhantomComic for Windows application.
### PhantomComic for Plex simply acts as a reader for the comics downloaded with the Windows application.

def Start():
	ObjectContainer.title1 = NAME

@handler(PREFIX, NAME, art=R("art-default.png"), thumb=R("icon-default.png"))
def MainMenu():
	oc = ObjectContainer()
	root = Prefs["install_path"] + "data\\"
	comics = os.listdir(root)
	for comic in comics:
		if os.path.isdir(root + comic):
			oc.add(DirectoryObject(key=Callback(ComicMenu, comic=comic), title=Core.storage.load(root + comic + "\\detail.txt"), summary=Core.storage.load(root + comic + "\\desc.txt"), thumb=(Prefs["install_url"] + "/data/" + comic + "/banner.jpg")))
	return oc

@route(PREFIX + "/comicmenu")
def ComicMenu(comic):
	root = Prefs["install_path"] + "data\\"
	chapters = os.listdir(root + comic + "\\comic\\")
	oc = ObjectContainer()
	oc.title1 = Core.storage.load(root + comic + "\\detail.txt")
	for chapter in chapters:
		if os.path.isdir(root + comic + "\\comic\\" + chapter):
			url = (Prefs["install_url"] + "/data/" + comic + "/comic/" + chapter)
			oc.add(PhotoAlbumObject(
				key=Callback(GetPhotoAlbum, url=(root + comic + "\\comic\\" + chapter), title=("Chapter " + chapter)),
				rating_key=url,
				title=("Chapter " + chapter),
				source_title=Core.storage.load(root + comic + "\\detail.txt"),
				tagline=None,
				originally_available_at=None,
				thumb=(url + "\\001.jpg"),
				art=R("art-default.png")))
	return oc

# GetPhotoAlbum
#   Create and return the contents of a photo album.
@route(PREFIX + "/get/album")
def GetPhotoAlbum(url, title):
	# setup objectcontainer
	oc = ObjectContainer()
	oc.title2 = title
	# setup vars
	pages = os.listdir(url)
	# loop pages
	for page in pages:
		# create new photo object for each page
		oc.add(CreatePhotoObject(
			title=("Page " + page.replace(".jpg", "")),
			url=Callback(GetPhoto, url=(url.replace(Prefs["install_path"], Prefs["install_url"] + "/")) + "/" + page)))
	# ret oc
	return oc
# CreatePhotoObject
#   Initialize and return a photo object.
@route(PREFIX + "/createphotoobject")
def CreatePhotoObject(title, url, include_container=False, *args, **kwargs):
	po = PhotoObject(
		key = Callback(CreatePhotoObject, title=title, url=url, include_container=True),
		rating_key = url,
		#source_title = "Reader",
		title = title,
		thumb = url,
		art = R("art-default.png"),
		items = [MediaObject(parts = [PartObject(key=url)])]
	)
	if include_container:
		return ObjectContainer(objects=[po])
	return po
# GetPhoto
#   ----
@route(PREFIX + "/get/photo")
def GetPhoto(url):
	return Redirect(url)