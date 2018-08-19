
"""



"""


import os
import pathlib
import urllib.parse
import re
import fnmatch

SRE_TYPE = type(re.compile(""))


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
            # The part is not abbreviated, just append and move to next part:
            expanded_path = part_path
            print(" - path_part exists, expanded_path is now ", expanded_path)
        else:
            # Try to find path expansion for the non-existing part:
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


def make_path_match_func(pat, match_type="glob"):

    # print("Making pattern matching (sub-)function...")

    if isinstance(pat, list):
        matchfuncs = [make_path_match_func(pat) for pat in pat]

        def matcher(path):
            return any(m(path) for m in matchfuncs)
        return matcher

    if isinstance(pat, str):
        if match_type in ('glob', 'fnmatch'):
            # def matcher(path):
            #     return fnmatch.fnmatch(path, pat)
            # Maybe better to just use compiled regex (although fnmatch does some other nice things)
            pat = fnmatch.translate(pat)  # returns str, not compiled regex
        # assume pat is now a regex string:
        pat = re.compile(pat)
        print(" - match pattern:", pat)

    if isinstance(pat, SRE_TYPE):
        def matcher(path):
            # print("Matching: %s vs %s = %s" % (pat, path, pat.match(str(path))))
            # path = path.as_posix()  # else '/' doesn't match path separator on windows. Sigh.
            return bool(pat.match(path))
        return matcher
    else:
        # pat is not a string and it is not a compiled regex.
        # Assume at this point that pat is just a custom callable matching function.
        print("pat is not str or compiled regex, using as callable...")
        return pat


def make_path_filterfunc(
        include_dirs=True, include_files=True,
        exclude_dirs=False, exclude_files=False, exclude_symlinks=False,
        match_type="glob", match_rel_path=False, match_name_only=False
):
    """

    Args:
        include_dirs:
        include_files:
        exclude_dirs:
        exclude_files:
        exclude_symlinks:
        match_type:
        match_rel_path: Perform match against path as relative to this path.
        match_name_only:
            If matching name only, then ".*" will match /path/to/.hiddenfolder
            However, if matching by the full path, then you need to use "**/.*" to match.
            Two asterixes (**) with glob matching is used to indicate "anything, including slashes".
            For some reason, "*.md" will match /path/to/file.md - even without the **.


    Returns:

    """
    # print("include_dirs=%r, include_files=%r, exclude_dirs=%r, exclude_files=%r, exclude_symlinks=%r:" %
    #       (include_dirs, include_files, exclude_dirs, exclude_files, exclude_symlinks))

    if include_dirs in (True, False, None):
        def dir_is_included(path):
            return include_dirs
    else:
        # print("Making include_dirs match function...")
        dir_is_included = make_path_match_func(include_dirs, match_type=match_type)

    if include_files in (True, False, None):
        def file_is_included(path):
            return include_files
    else:
        # print("Making include_files match function...")
        file_is_included = make_path_match_func(include_files, match_type=match_type)

    if exclude_dirs in (True, False, None):
        def dir_is_excluded(path):
            return exclude_dirs
    else:
        # print("Making exclude_dirs match function...")
        dir_is_excluded = make_path_match_func(exclude_dirs, match_type=match_type)

    if exclude_files in (True, False, None):
        def file_is_excluded(path):
            return exclude_files
    else:
        # print("Making exclude_files match function...")
        file_is_excluded = make_path_match_func(exclude_files, match_type=match_type)

    def filterfunc(path):
        if not os.path.exists(path):
            print("ERROR: PATH DOES NOT EXISTS:", path)
        # print("filterfunc(%s):" % (path,))
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        # path_str = path.name if match_name_only else (
        #     path.relative_to(match_rel_path) if match_rel_path else path).as_posix()
        if match_name_only:
            path_str = path.name
        else:
            if match_rel_path:
                path_str = path.relative_to(match_rel_path).as_posix()
            else:
                path_str = path.as_posix()
        print("path_str: %r (path: %r)" % (path_str, path))
        if path.is_dir():
            print("Directory %s: dir_is_included(path) is %s and dir_is_excluded(path) is %s" % (
                path_str, dir_is_included(path_str), dir_is_excluded(path_str)))
            return dir_is_included(path_str) and not dir_is_excluded(path_str)
        if exclude_symlinks and path.is_symlink():
            return False
        print("File   %s: file_is_included(path) is %s and file_is_excluded(path) is %s" % (
            path_str, file_is_included(path_str), file_is_excluded(path_str)))
        return file_is_included(path_str) and not file_is_excluded(path_str)

    return filterfunc


def get_page_tree_recursive(
        path, rel_root=None,
        depth=99,
        filterfunc=None,
        include_dirs=True, include_files=True,
        exclude_dirs="**/.*", exclude_files="**/.*", exclude_symlinks=False,
        match_type="glob", match_rel_path=True, match_name_only=False,
        remove_ext_for_files=('.md',),
        parse_files=None
):
    """

    Args:
        path:
        rel_root:
        filterfunc:
        include_dirs:
        include_files:
        exclude_dirs:
        exclude_files:
        exclude_symlinks:
        match_type:
        match_name_only:
        parse_files:


    Args:
        rel_root:

    Returns:

    Data structure:
        We have both files and folders...
        Question: The index that we keep is probably going to be flat,
        and will have to be nested when loaded.
        List of dicts: [
            {'node_type': 'folder/document'}
        ]

    Examples:
        >>> folder = "/path/to/document_root"
        >>> get_page_tree_recursive(folder, rel_root=folder, include_files="*.md")

    """
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)

    # print("path:", path)
    # print("rel_root:", rel_root)
    # print("path.relative_to(rel_root)", path.relative_to(rel_root) if rel_root else "N/A")
    # ValueError: relative path can't be expressed as a file URI
    # uri_path = path.relative_to(rel_root).as_uri() if rel_root else path.as_uri()
    # print("uri_path:", uri_path)
    rel_path = path.relative_to(rel_root).as_posix() if rel_root else path.as_posix()
    url_path = "/" + rel_path
    # url_path aka href - but href is usually the complete path and we may prepend a custom per-site document root.
    # still, "url_path" also indicates "the path part of the url", which is not necessarily correct.
    # we should go with path_relative_to_document_root_url.

    if os.path.isfile(path):
        return {
            'node_type': 'file', 'is_file': True, 'is_dir': False,
            'fs_path': path,
            'url_path': (os.path.splitext(url_path)[0]
                         if remove_ext_for_files
                            and (remove_ext_for_files is True or url_path.endswith(remove_ext_for_files))
                         else url_path),
        }

    if filterfunc is None:
        filterfunc = make_path_filterfunc(
            include_dirs=include_dirs, include_files=include_files,
            exclude_dirs=exclude_dirs, exclude_files=exclude_files, exclude_symlinks=exclude_symlinks,
            match_type=match_type, match_rel_path=(match_rel_path and rel_root),
            match_name_only=match_name_only
        )
    childpaths = [path.joinpath(child) for child in os.listdir(path)]
    # print("\nMatching elements in folder:", path)
    # for childpath in childpaths:
    #     print(" - %s --> %s" % (childpath, filterfunc(childpath)))
    return {
        'node_type': 'folder', 'is_file': False, 'is_dir': True,
        'fs_path': path,
        'name': path.name,
        'url_path': url_path,
        'children': [
            get_page_tree_recursive(childpath, rel_root=rel_root, depth=depth-1, filterfunc=filterfunc)
            for childpath in childpaths
            if filterfunc(childpath)
        ] if depth > 1 else []
    }


