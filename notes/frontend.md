



Front-end web frameworks:
=========================

The front-end web framework is responsible for compiling the user interface,
creating and combining HTML, CSS, Javascript to produce a nice and consistent user experience.

While the templating system is responsible for compiling the base HTML document, 
putting things in the right places, the front-end web frameworks are used to create
the javascript and style sheets that make the page look nice and have the functionality it needs.

One raison d'être for web frameworks is the fact that browsers often render the 
same web page slightly differently, and they also have different defaults/presets.
So unless everything has been specified very precisely, the web browsers will just 
render it however it feels like.

Another reason for using a web framework is to provide a consistently good, "responsive"
user experience, across many devices, where e.g. screen size may vary considerably.




Front-end web frameworks, overview:
------------------------------------

JQuery-based front-end web frameworks:

* Bootstrap - JQuery, SASS. For mobile-first, responsive web design (RWD). 121k GitHub stars. 600 kb.
* SemanticUI - JQuery, Less. 40k Github stars. 800 kb. Semantic, tag ambivalence, responsive.


Other Javascript web frameworks:


Pure CSS/HTML web frameworks (no Javascript):

* Pure.CSS - CSS only. By Yahoo. 18k github stars. Minimal, scalable, modular CSS. 4 kb.
* Bulma - CSS only, no Javascript, CSS3 features (e.g. Flexbox), grid-based layout. 
* Skeleton - "Dead simple frameworks for smaller projects." No development since 2014.
* [W3.CSS](https://www.w3schools.com/w3css/default.asp) - CSS only, but may require 
    custom Javascript for actual page functionality. 
    Has [accordions](https://www.w3schools.com/w3css/w3css_accordions.asp), 
    [navigation](https://www.w3schools.com/w3css/w3css_navigation.asp), and 
    [sidebar](https://www.w3schools.com/w3css/w3css_sidebar.asp) elements
    that might be useful for the UI I would like to have. 
    


Uncategorized:

* Foundation - Sass. By ZURB. 27k Github stars. 200 kb. Semantic, mobile-first.
* HTML5 Boilerplate (H5BP) - 
* Simple Grid
* Unsemantic
* Material-UI
* Base
* Materialize
* Ink
* Basscss
* Groundwork
* Onsen UI
* Cardinal
* Jeet
* UIKit - JQuery.
* TopCoat
* Susy framework
* ArtDesignUI - 
* ToastGrid
* Material Design Lite
* Element - Uses Vue.js.


Refs:
* https://www.agriya.com/blog/15-alternatives-bootstrap-foundation-skeleton/



Frontend frameworks, comparison:
---------------------------------


### Pure.CSS

Examples:

* https://purecss.io/layouts/
* https://purecss.io/layouts/side-menu/ - I like this one.




Front-end Design & Implementation:
==================================


Adding a page tree navigation menu:
------------------------------------

We need to do three things:

1. Create a nested python list of `[("link_text", "url", [<child pages>]), ...]`.
    Or maybe use a dict instead of tuple for each element?
2. Create a HTML nested list of page links (or table).
3. Expand the list item corresponding to the current page.

The first must be done in Python.
The second is best be done with Python or Jinja.
The third can be done with Python, Jinja, or Javascript.


Implementation options:

1. First, Python should compile a list of pages as a variable to the Jinja template.

2. Second, the Jinja template then loops over the page list 
    and creates a list with `<li>` elements containing `<a>` page links.
    This HTML list could also be compiled in python and forwarded as a plain HTML string to Jinja.

3. Finally, we need to make sure the current page is expanded, and perhaps visible, in the page tree.
    This can be done in Python, Jinja, or Javascript:

    a. In Python, when compiling the plain page tree HTML string, 
        just check if the link parts matches the current url, and if it does, 
        mark it as "expanded".
        
    b. In the Jinja template, again just check the current url when adding the page tree HTML,
        and mark as expanded if the page's url matches the current url.
        
    c. Finally, the page tree can be expanded in Javascript after loading the page,
        by looping over all the elements and checking if the list item element's anchor href 
        matches the current URL.
        This is a bit more complex, but has the advantage that we can have a single, shared
        static page tree that we use for all pages, which is just expanded based on the currently viewed page.
        Since the shared page tree HTML can be cached, and the javascript is run client-side,
        this would require a minimal amount of server resources.


Pros and cons:

* Avoiding Javascript is always nice, so try the Python or Jinja approach.
* Since we are using templates between different python systems, 
    it would be optimal to have the tree generation in Jinja.

        
What HTML elements to use?

* Use a nested `<ol>` or `<ul>` HTML list, 
    with `<li>` list item elements with a single `<a>` anchor for page links.

* I want to be able to collapse and expand the folder navigation items, like a file browser.
    
    * This functionality is generally called an "accordion" or "accordion menu".
    * It is traditionally done with Javascript, as shown [here](https://www.w3schools.com/howto/howto_js_accordion.asp).
    * With HTML5, you can use the `<details>` and `<summary>` elements, which will give you
        elements that can expand/collapse (visible/hidden) without Javascript.
        This is traditionally done with Javascript, but always better to use plain HTML whenever possible.
        If you want to use Javascript for compatibility, this is included in many libraries,
        e.g. the bootstrap library.





Javascript page-tree libraries:

- Step 1: Google "javascript page tree navigation menu”.
- http://registry.origami.ft.com/components/o-hierarchical-nav / https://github.com/Financial-Times/o-hierarchical-nav
- jsTree, https://www.jstree.com/
  - demo: https://github.com/akshar-raaj/Using-jsTree
- http://www.easyjstree.com/
- https://stackoverflow.com/questions/5636375/how-to-create-a-collapsing-tree-table-in-html-css-js
    - this is for a table, not a list.
    - http://jsfiddle.net/Vd5BH/5/
    - http://maxazan.github.io/jquery-treegrid/
    - https://www.jstree.com/
    - https://plugins.jquery.com/tag/tree/
    - HTML <summary> tag - https://www.w3schools.com/tags/tag_summary.asp
- https://stackoverflow.com/questions/2989829/how-to-create-a-menu-tree-using-html
  - http://www.dynamicdrive.com/dynamicindex1/navigate1.htm
  - Also recommends a pure CSS/HTML solution with no JS.
- https://ourcodeworld.com/articles/read/146/top-5-best-tree-view-jquery-and-javascript-plugins
  - jQuery file tree, Bootstrap Treeview, jqTree, jsTree, FancyTree 
- https://webix.com/widget/tree/
- https://www.thecssninja.com/css/css-tree-menu - pure CSS.
- https://www.kollermedia.at/2007/04/11/20-free-javascript-and-ajax-tree-menus/
- https://www.w3schools.com/howto/howto_js_collapsible.asp
- https://www.w3schools.com/Bootstrap/bootstrap_collapse.asp
