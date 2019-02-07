---
# Metadata ("YAML header" aka "YAML Front Matter", YFM)
# Note: Variable names are converted to lower-case.
# `Template`: Specify a Template to use to display this page (default: `index`). Templates must be located in the current theme's directory as `template_name.twig`.
# `title`: Is generally auto-generated based on user-customizable format string. Users may have different preferences for project page titles.
# `projectid`: Unique project identification keyword.
# `titledesc`: A very short description of the project.
# `description`: A slightly longer description; recognized by Pico).
# `motivation`, `goal`, `hypothesis`: Write these BEFORE you start the experiment.
# `outline`: A brief outline of the steps/parts performed in this experiment in order to produce the end product, possibly including the starting point if not mentioned under `motivation`.
# `result`, `outlook`: Write these AFTER you've completed the experiment.
# `comments`: Other comments about the experiment not matching either of goal/hypothesis/result/outlook.
# `summary_image`: Can be used to specify a single "thumbnail" that will be used to visually represent this experiment in a long overview.
# `status`: planned, started, completed, or cancelled.
# `startdate`, `enddate`, `date`: start and end dates for the experiment (when actually started, else null). Date can be the day *this file* was created.
# `author`: A single, primary author of this document; recognized by Pico
# `authors`: List everyone who co-authored *this* document.
# `collaborators`: List everyone involved with the experiment (even if they didn't contribute to this document).
# `projects`, `related_expids`, `related_pages`: List projects, related experiments (by ID), and other internal ELN pages related to this experiment.
# `links`: Links (URLs) to standard, named resources, e.g. labbook, webstrate, etc.
# For now, other ad-hoc references are added using standard Markdown named-references: A line with [arbitrary case-insensitive reference key]: https://myreference-url.org
document_type: Project-overview
template: RS_project
title: {title}
projectid: {projectid}
titledesc: {titledesc}
description: {titledesc}
motivation: ""
goal: ""
hypothesis: ""
outline: ""
result: ""
outlook: ""
comments: ""
summary_image: null
status: planned
status_comment: ""
date: {date}
startdate: {startdate}
enddate: null
author: scholer
authors: [scholer]
collaborators: [scholer]
# experiments: []
related_expids: []
related_pages: []
links:
    labbook: null
    webstrate: null
---
<!-- End YAML Front Matter (page metadata), begin actual Markdown page. -->
<!--

Usage:

* First, fill in the YAML metadata above. These are simple `key: value` pairs.
* The "new project" markdown template has {{variable}} placeholders, which are replaced with actual values when creating the page (using "Create New Project" command).
	* Note: If you are editing the input template file, you will see "{{variable}}" above surrounded by two braces because we don't want to substitute "variable". After variable substitution, it will have just a *single* brace and look "right" in the newly created page.)
* You can use %meta.variable% as placeholder to insert meta data on page for Pico page rendering.
* You can use the `template` metadata field to specify a template on a per-page basis.
* Pico recognizes and uses the following page meta headers: `title`, `description`, `author`, `date`, `robots`
* Pico additionally provides these derived variables: `id`, `url`, `time`, `date_formatted`, `raw_content`. - `date_formatted` is a string produced from the datetime given the configured date display format.


Nomenclature:

* Projects have a short/abbreviation keyword name, which is just the filename (without file extension).
	* I could have a "project id" similar to "expriment id", but I'm not sure yet what this should look like. 
	* Maybe "project identifier" could just be this abbreviated keyword name?
* Like experiments, projects have a `title`, which is usually auto-generated from other variables using a user-custom format string.
* Projects have a "title description", which is just the title without any other identifiers.
* Current project titledesc format is ... ?


Markdown quick reference:

* Links: [Link text](url)
* Inserting images: ![alt text](path/to/image.png "Logo Title Text 1") - "alt text" should describe the image; "title text" should provide additional information.
* Reference style: ![alt text][summary_image]
	* then later: [summary_image]: path/to/image.png
* Resizing images: Not generally supported. Either resize the image file, or use HTML: <img src="drawing.jpg" alt="Drawing" style="width: 200px;"/>


-->

<!-- Project: {title} -->


Current status: %meta.status%




Project journal:
----------------







