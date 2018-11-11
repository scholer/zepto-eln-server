# Copyright 2018 Rasmus Scholer Sorensen

"""

Module for extracting and parsing YAML Front-Matter from documents.

"""

import re
import yaml
import sys
try:
    import frontmatter
except ImportError:
    print("`frontmatter` package not available; using local routines.")
    frontmatter = None


def split_yfm(raw_content, sep_regex=r'^-{3,}$', require_leading_marker='raise', require_empty_pre='raise'):
    yfm_sep_regex = re.compile(sep_regex, re.MULTILINE)
    splitted = yfm_sep_regex.split(raw_content, 2)  # Split at most two times (into three parts) on regex matches.

    if len(splitted) == 1:
        raise ValueError(f"Unable to extract YAML frontmatter from text; no matches for {sep_regex!r}")
    if len(splitted) == 2:
        if require_leading_marker:
            if require_leading_marker == 'raise':
                raise ValueError(f"Only found one YFM marker ({sep_regex!r}).")
            else:
                print(f"WARNING: Only found one YFM marker ({sep_regex!r}).", file=sys.stderr)
        yfm_text, md_text = splitted
    else:
        pre, yfm_text, md_text = splitted
        if len(pre.strip()) > 0 and require_empty_pre:
            raise ValueError('The part before the first front-matter delimiter ("---") is not empty.')
    return yfm_text, md_text


def parse_with_frontmatter(text):
    """ Parse, using the 'frontmatter' package. Reference function mostly.
    Note: The `frontmatter` package actually has a full "post" object class, which
    looks very similar to my `document` object.
    """
    import frontmatter
    from frontmatter import YAMLHandler
    # Unfortunately, frontmatter.parse doesn't have any way to determine if splitting gives an error (only YAML load).
    metadata, content = frontmatter.parse(text, handler=YAMLHandler)
    return metadata, content


class FrontmatterParserError(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_errors = 0
        # err_msg = None
        self.err_msgs = []
        self.err_details = []
        self.exceptions = []

    def get_err_msg(self):
        return " | ".join(self.err_msgs)

    def get_err_detail(self):
        return " | ".join(self.err_details)

    def add_error(self, err_msg, err_detail="", exception=None):
        self.err_msgs.append(err_msg)
        self.err_details.append(err_detail)
        self.exceptions.append(exception)
        self.n_errors += 1


def parse_yfm(raw_content, sep_regex=r'^-{3,}$', require_leading_marker='raise', require_empty_pre='raise'):
    """ Parse Yaml Front Matter from text and return metadata dict and stripped content.

    Args:
        raw_content: The raw Markdown document text to parse YAML front-matter from.
        sep_regex: The regex on which the YFM is separated from the surrounding text.
        require_leading_marker: Raise error if only one YFM marker is found.
        require_empty_pre: Raise error if the part before the YFM is not empty.

    Returns:
        Two-tuple of (frontmatter/metadata dict, and remaining, stripped, content).

    """
    err = FrontmatterParserError()

    if frontmatter:
        print("Parsing `raw_content` with frontmatter package...")
        yfm, md_content = parse_with_frontmatter(raw_content)

    try:
        yfm_text, md_content = split_yfm(
            raw_content, sep_regex=sep_regex,
            require_leading_marker=require_leading_marker, require_empty_pre=require_empty_pre)
    except ValueError as exc:
        err.add_error("Error splitting document front-matter: " + str(exc), exception=exc)
        return {}, md_content, err
    if not yfm_text:
        err_msg = f"WARNING: yfm_text is empty, {yfm_text!r}. Setting yfm to an empty dict."
        print(err_msg, file=sys.stderr)
        err.add_error(err_msg)
        return {}, md_content, err
    try:
        print("Loading yfm_text with yaml.load:", file=sys.stderr)
        print(yfm_text, file=sys.stderr)
        yfm = yaml.load(yfm_text)  # Exception caught in outer functions that has knowledge about filename.
    except (yaml.scanner.ScannerError, yaml.parser.ParserError) as exc:
        err_msg = f"ERROR: `{exc.__class__.__module__}.{exc.__class__.__name__}`  during `yaml.load(yfm_text)`."
        print(err_msg, file=sys.stderr)
        details = []
        yfm_lines = yfm_text.split('\n')

        info = f"> Exception message: {exc}"
        print(info, file=sys.stderr)
        details.append(info)

        for marker_name, marker in (('Context', exc.context_mark), ('Problem', exc.problem_mark)):
            if marker is None:
                print(f"> ({marker_name} is {marker})", file=sys.stderr)
                continue
            context_before, context_after = 2, 2
            context_lines_start, context_lines_stop = marker.line - context_before, marker.line + 1 + context_after
            context_lines = yfm_lines[context_lines_start:context_lines_stop]
            context_lines = [line.replace('\t', '⭾' ).replace(' ', '·') for line in context_lines]
            context_lines[context_before] += "    ⚠️"
            context_lines = "\n".join(context_lines)
            info = (f"\n> {marker_name} marker at line {marker.line}," 
                    f" showing lines {context_lines_start}–{context_lines_stop} below" 
                    " (⭾ and · indicates TAB and SPACE characters)"
                    f":\n\n{context_lines}\n")
            print(info, file=sys.stderr)
            details.append(info)
        # except yaml.parser.ParserError as exc:
        #     import pdbpp; pdbpp.set_trace()

        yfm_text_visible_tabs = yfm_text.replace(r'\t', r'\\t')
        info = f"\n> Full yfm_text (with visible tabs) is:\n\n{yfm_text_visible_tabs}\n"
        print(info, file=sys.stderr)
        details.append(info)

        info = "\n> Checking yfm_text for common errors..."
        tab_eol_lines = [str(i) for i, line in enumerate(yfm_text.split('\n')) if line.endswith('\t')]
        info += ("\n - Lines with tabs at the end:" +
                 ("YES! Lines: " + ", ".join(tab_eol_lines) if tab_eol_lines else "No."))
        space_eol_lines = [str(i) for i, line in enumerate(yfm_text.split('\n')) if line.endswith(' ')]
        info += ("\n - Lines with tabs at the end:" +
                 ("YES! Lines: " + ", ".join(space_eol_lines) if space_eol_lines else "No."))

        print(info, file=sys.stderr)
        details.append(info)

        err.add_error(err_msg, err_detail="\n"+"\n------\n".join(details)+"\n\n", exception=exc)
        yfm = {}

        # import pdb; pdb.set_trace()
        # raise exc

    if err.n_errors == 0:
        err = None
    return yfm, md_content, err

