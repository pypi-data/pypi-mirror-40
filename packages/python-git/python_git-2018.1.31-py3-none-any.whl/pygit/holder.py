
# def open_shelves():
#     """Create shelves for used by python-git"""
#     try:
#         Path.mkdir(SHELF_DIR)
#     except FileExistsError:
#         shutil.rmtree(SHELF_DIR)
#         Path.mkdir(SHELF_DIR)
    
#     names = shelve.open(str(PurePath(SHELF_DIR / "NAME_SHELF"))) # Use the string representation to open path to avoid errors
#     indexes = shelve.open(str(PurePath(SHELF_DIR / "INDEX_SHELF")))
#     return names, indexes