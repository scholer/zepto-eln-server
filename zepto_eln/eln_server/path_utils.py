
"""



"""


import os


def is_newer(this, another):
    """ Return True if `this` file is newer than `another` file. """
    return os.path.getmtime(this) > os.path.getmtime(another)


def longest_common_startstr(sa, sb):
    """ returns the longest common substring from the beginning of sa and sb

    Args:
        sa:
        sb:

    Returns:

    Source:
    * https://stackoverflow.com/questions/18715688/find-common-substring-between-two-strings  (Eric)
    """
    def _iter():
        for a, b in zip(sa, sb):
            if a == b:
                yield a
            else:
                return

    return ''.join(_iter())


def find_index_file_for_dir(dirpath, ext='.md', strip_ext=True, indexfn='index.md', sep='/'):
    """ For a given directory, try to find a default index file.
    This is either `index.md`, or the file with the longest overlap with the parent directory's name.

    Args:
        dirpath:
        ext:
        strip_ext:
        indexfn:

    Returns:

    """
    # files = [fp for fp in [os.path.join(dirpath, fn) for fn in os.listdir(dirpath)] if os.path.isfile(fp)]
    files = [fn for fn in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, fn))]
    # filter by the correct extension:
    if ext:
        files = [fn for fn in files if fn.endswith(ext)]
    if len(files) == 0:
        raise RuntimeError("Could not find any index files for directory: " + dirpath)

    if indexfn in files:
        found_fn = indexfn
    else:
        pardirname = os.path.basename(dirpath)
        exact_matches = [fn for fn in files if os.path.split(fn)[0] == pardirname]
        if exact_matches:
            assert len(exact_matches) == 1
            return exact_matches[0]
        # sort by overlap first, then filename:
        files_scored = sorted(
            [(len(longest_common_startstr(os.path.splitext(fn)[0], pardirname)), fn) for fn in files], reverse=True)
        # matching_files = [fn for score, fn in files_scored if score > 0]  # has best match first
        best_score, longest_match = files_scored[0]
        if best_score > 0:
            found_fn = longest_match  # use longest, i.e. the file that has the most in common with the parent dirname.
        else:
            raise RuntimeError("Could not find any index files for directory: " + dirpath)
    if strip_ext:
        found_fn = found_fn.rsplit(ext, 1)[0]

    return sep.join([dirpath, found_fn])


def find_path_expansion(abbrev, rel=None, pathsep='/'):
    """ Find path expansion for a single path abbreviation.
    If rel is none, will expand the last path part of `abbrev`.

    Args:
        abbrev:
        rel:
        sep:

    Returns:

    Examples:
        >>> os.listdir('.')
        'Alice', 'Bob', 'Bobby', 'Shibo'
        >>> find_path_expansion('Bo', rel='.')
        './Bob'
        >>> find_path_expansion('./Bo')  # Uses '.' as the relative part.
        './Bob'

    """
    if pathsep is None:
        pathsep = '/'  # This works on both windows and posix.
    abbrev = os.path.normpath(abbrev)
    print("abbrev, rel:", abbrev, rel)
    if rel is None:
        rel, abbrev = os.path.split(abbrev)
        print("rel, abbrev:", rel, abbrev)
    else:
        rel = os.path.normpath(rel)
        print("norm rel:", rel)
    assert os.path.isdir(rel)
    # pardirname = os.path.basename(rel)  # No, using parent dirname is for finding index files, not expanding abbrevs.
    # print("pardirname:", pardirname)
    cand_elems = os.listdir(rel)
    print("cand_elems:", cand_elems)
    cand_paths = [pathsep.join([rel, cand]) for cand in cand_elems if cand.startswith(abbrev)]
    print("cand_paths:")
    print("\n".join(cand_paths))
    if cand_paths:
        # cands now has the rel dirpath prefix:
        md_files = [cand for cand in cand_paths if cand.endswith('.md') and os.path.isfile(cand)]
        print("md_files:", md_files)
        # Return the shortest file or directory that starts with the abbreviated abbrev part:
        if md_files:
            return md_files[0]
        dirs = [cand for cand in cand_paths if os.path.isdir(cand)]
        print("dirs:", dirs)
        if dirs:
            return dirs[0]
    raise RuntimeError(f"Could not find any abbrev expansion for abbrev: {abbrev!r}.")


def expand_abbreviated_path(
        path, root, pathsep='/',  # os.path.pathsep,
        return_index_for_dir=True, indexfile_ext='.md', strip_indexfile_ext=True,
        return_relpath=True, ensure_forwardslash=True
):
    """ Expand all "abbreviated" parts of `path`, returning a "full length" path matching an actual URI.

    Args:
        path:
        root:
        pathsep: How to join paths
        return_index_for_dir:
        indexfile_ext: The extension to look for when finding index files.
        return_relpath:
        ensure_forwardslash: Convert windows backslashes to forward slashes.

    Returns:
        Expanded path (str)

    Examples:
        # Basic example, expand '2018/RS510' to '2018_Aarhus/RS510 ONI Nanoimager demo and PAINT':
        >>> expand_abbreviated_path(path='2018/RS510', root='D:/Dropbox/_experiment_data/', return_index_for_dir=False, strip_indexfile_ext=False, return_relpath=False, ensure_forwardslash=False)
        'D:\\Dropbox\\_experiment_data\\2018_Aarhus/RS510 ONI Nanoimager demo and PAINT'

        # '2018_Aarhus/RS510 ONI Nanoimager demo and PAINT' is a folder; return the index file:
        >>> expand_abbreviated_path(path='2018/RS510', root='D:/Dropbox/_experiment_data/', return_index_for_dir=True, strip_indexfile_ext=False, return_relpath=False, ensure_forwardslash=False)
        'D:\\Dropbox\\_experiment_data\\2018_Aarhus/RS510 ONI Nanoimager demo and PAINT/RS510.md'

        # We generally call markdown files without the extension when we want to view it as a rendered HTML page,
        # thus it is generally more useful to always get the index file path without extension:
        >>> expand_abbreviated_path(path='2018/RS510', root='D:/Dropbox/_experiment_data/', return_index_for_dir=True, strip_indexfile_ext=True, return_relpath=False, ensure_forwardslash=False)
        'D:\\Dropbox\\_experiment_data\\2018_Aarhus/RS510 ONI Nanoimager demo and PAINT/RS510'

        # Finally, since this is a web server, paths are best described relative to the document root:
        >>> expand_abbreviated_path(path='2018/RS510', root='D:/Dropbox/_experiment_data/', return_index_for_dir=True, strip_indexfile_ext=True, return_relpath=True, ensure_forwardslash=True)
        '2018_Aarhus/RS510 ONI Nanoimager demo and PAINT/RS510'

* The `/eln_server/` entry point accepts "abbreviated" paths which will be expanded:
    That is, if you request `/eln_server/2018/RS532/`
    and `<root>/2018` doesn't exists, but `<root>/2018_Aarhus` does exists,
    then the request is redirected to `/eln_server/2018_Aarhus/RS532/`.
    If `<root>/2018_Aarhus/RS532/` doesn't exists, but `<root>/2018_Aarhus/RS532_Test_experiment/` does,
    then the request is redirected to `/eln_server/2018_Aarhus/RS532_Test_experiment/`.
    If `<root>/2018_Aarhus/RS532_Test_experiment/` exists and is a folder,
    then if index.md exists, then we redirect to `/eln_server/2018_Aarhus/RS532_Test_experiment/index`
    otherwise, the first .md file that is fully included in the folder name is served by redirecting to
    that filename (without extension).
    For instance, say we have the following files:
        README.md, RS532.md, RS532.html, analyze_RS532.py, RS532a.md, RS.md, RS532.bak.md.
    First we filter .md files:
        README.md, RS532.md, RS532a.md, RS.md, RS532.bak.md.
    Then we remove files that doesn't start with the same as the directory:
        >>> files = [fn for fn in files if dirname.startswith(os.path.splitext(fn)[0])]
        RS532.md, RS.md
    Then we take the last file:
        >>> fn = sorted(files)[-1]
        RS532.md
    Then we redirect to:
        `/eln_server/2018_Aarhus/RS532_Test_experiment/RS532`.

    """
    expanded_path = os.path.normpath(root)
    print(f"\n\nStarting expansion of path {path!r}from {expanded_path!r}...")
    for part in path.split(pathsep):
        print("expanded_path, path:", expanded_path, path)
        part_path = os.path.join(expanded_path, part)
        print(" - path_part:", part_path)
        if os.path.exists(part_path):
            expanded_path = part_path
            print(" - path_part exists, expanded_path is now ", expanded_path)
        else:
            try:
                print(f" - trying to find path expansion for path={part} using rel={expanded_path}.")
                expanded_path = find_path_expansion(part, rel=expanded_path, pathsep=pathsep)
                print(f" - SUCCESS! expanded_path is now {expanded_path!r}.")
            except RuntimeError as exc:
                print("Could not find path expansion for path:", path)
                print(" - Breakdown at:", expanded_path)
                print(" - Next part:", part)
                raise exc
    if os.path.isdir(expanded_path) and return_index_for_dir:
        print(f"Expanded path {expanded_path!r} is a directory; finding index file...")
        expanded_path = find_index_file_for_dir(expanded_path, ext=indexfile_ext, strip_ext=strip_indexfile_ext)
        print(f" - expanded_path with index file:", expanded_path)
    if return_relpath:
        expanded_path = os.path.relpath(expanded_path, start=root)
        print(f" - expanded_path made relative to root:", expanded_path)
    if ensure_forwardslash and os.name == 'nt':
        # Ways to check OS: os.name, sys.platform, platform.system(), psutil.WINDOWS/OSX/LINUX
        expanded_path = expanded_path.replace("\\", "/")
        print(f" - expanded_path, after converting slashes:", expanded_path)
    return expanded_path
