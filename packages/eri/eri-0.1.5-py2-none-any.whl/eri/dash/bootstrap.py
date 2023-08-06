#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: eri.dash.bootstrap
Author: zlamberty
Created: 2018-08-21

Description:
    shorthand ways of building bootstrap elements for apps.

    in the long run, we should just use the existing react bootstrap components,
    but I don't know how to do that yet. c.f. https://react-bootstrap.github.io/

Usage:
    >>> import eri.dash.bootstrap
    >>>
    >>> app = dash.Dash()
    >>> eri.dash.bootstrap.add_bootstrap_css(app)
    >>> button = eri.dash.bootstrap.Button("my button", context="warning")

"""

from .. import logging as _logging


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

_LOGGER = _logging.getLogger(__name__)

_BOOTSTRAP_CONTEXTS = (
    'primary',
    'secondary',
    'success',
    'danger',
    'warning',
    'info',
    'light',
    'dark',
)

# xs seems to be not supported in bs4+. not clear to me
_BOOTSTRAP_SIZES = ('sm', 'md', 'lg',)

_BOOTSTRAP_HORIZ_ALIGN = {
    'left': 'justify-content-start',
    'center': 'justify-content-center',
    'right': 'justify-content-end',
    # if you don't know what these two mean, don't use them!
    'around': 'justify-content-around',
    'between': 'justify-content-between',
}

_BOOTSTRAP_COLOR_THEMES = ('dark', 'light')

_BOOTSTRAP_CSS = (
    "https://use.fontawesome.com/releases/v5.2.0/css/all.css",
    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css",
)

_BOOTSTRAP_JS = (
    "http://code.jquery.com/jquery-3.2.1.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js",
    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js",
)

class EriDashBootstrapError(Exception):
    """local error for better handling"""
    def __init__(self, msg, *args, **kwargs):
        _LOGGER.error(msg)
        super().__init__(msg, *args, **kwargs)


# ----------------------------- #
#   conditional imports         #
# ----------------------------- #

# I don't want to make the various dash libraries a requirement for installing
# the eri module, but obviously this library will require them. let's alert
# users to specific actions they should take if they run into problems
try:
    # import all the required dash objects
    import dash as _dash
    #import dash_core_components as _dcc
    import dash_html_components as _html
except ImportError:
    _LOGGER.debug(
        "this package requires that you have at least the following packages"
        " installed in your local python environment"
    )
    _LOGGER.debug('dash')
    _LOGGER.debug('dash_core_components')
    _LOGGER.debug('dash_html_components')
    _LOGGER.debug('all can be installed via pip (no conda package at this time)')
    _LOGGER.debug(
        'installation instructions can be found at '
        'https://dash.plot.ly/installation'
    )
    raise EriDashBootstrapError(
        "unable to load the required dash packages; please install them"
    )


# ----------------------------- #
#   app object modifications    #
# ----------------------------- #

def add_bootstrap_css_js(app, css_files=_BOOTSTRAP_CSS, js_files=_BOOTSTRAP_JS):
    """add the required css and js files for bootstrap to work

    for the className values to mean anything, you have to add css and
    javascript to your dash app. this function does that for you

    args:
        app (dash.Dash): the app for which you want bootstrap enabled
        css_files (iterable): collection of external urls of css files that will
            be added
        js_files (iterable): collection of external urls of javascript files
            that will be added

    returns:
        None

    raises:
        None

    """
    _LOGGER.debug('adding css resources')
    for css in css_files:
        _LOGGER.debug('adding css url {}'.format(css))
        app.css.append_css({"external_url": css})

    _LOGGER.debug('adding js resources')
    for js in js_files:
        _LOGGER.debug('adding js url {}'.format(css))
        app.scripts.append_script({"external_url": js})


# ----------------------------- #
#   utils                       #
# ----------------------------- #

def _bs_classname(type_, context=None):
    """string formatting to make simple bootstrap classnames"""
    return '{}{}'.format(
        type_,
        ' {}-{}'.format(type_, context) if context is not None else ''
    )


def _validate_context(context):
    """check if the context is one of the allowed values"""
    if (context is None) or (context in _BOOTSTRAP_CONTEXTS):
        return
    else:
        err = EriDashBootstrapError(
            "invalid bootstrap context value: {}".format(context)
        )
        _LOGGER.error(err)
        _LOGGER.debug('valid context values are:')
        _LOGGER.debug('None')
        for c in _BOOTSTRAP_CONTEXTS:
            _LOGGER.debug('"{}"'.format(c))
        raise err


def _validate_size(size):
    """check if the size is one of the allowed values"""
    if (size is None) or (size in _BOOTSTRAP_SIZES):
        return
    else:
        err = EriDashBootstrapError(
            "invalid bootstrap size value: {}".format(size)
        )
        _LOGGER.debug('valid size values are:')
        _LOGGER.debug('None')
        for c in _BOOTSTRAP_SIZES:
            _LOGGER.debug('"{}"'.format(c))
        raise err


def _validate_h_alignment(h_alignment):
    """check if the alignment is one of the allowed values"""
    if (h_alignment is None) or (h_alignment in _BOOTSTRAP_HORIZ_ALIGN):
        return
    else:
        err = EriDashBootstrapError(
            "invalid key for bootstrap horizontal value: {}".format(h_alignment)
        )
        _LOGGER.debug('valid horizontal alignment values are:')
        _LOGGER.debug('None')
        for ha in _BOOTSTRAP_HORIZ_ALIGN:
            _LOGGER.debug('"{}"'.format(ha))
        raise err


def _validate_color_theme(theme):
    """check if the color theme is one of the allowed values"""
    if (theme is None) or (theme in _BOOTSTRAP_COLOR_THEMES):
        return
    else:
        err = EriDashBootstrapError(
            "invalid value for bootstrap color theme: {}".format(theme)
        )
        _LOGGER.debug('valid color theme values are:')
        _LOGGER.debug('None')
        for ct in _BOOTSTRAP_COLOR_THEMES:
            _LOGGER.debug('"{}"'.format(ct))
        raise err


def _div_factory(type_, children, context=None, **kwargs):
    """create a div with the given type and context, and with body `children`

    most bootstrap objects have the same format:

        <div class="type type-context">

    factory exists to avoid re-typing that 100 times, that's all

    args:
        type_ (str): bootstrap component type (e.g. alert, badge)
        children (str or dash component): the dash child element of this div
        context (str): the bootstrap context (default: None)

    returns:
        html.Div: dash html Div component

    raises:
        EriDashBootstrapError

    """
    _validate_context(context)
    return _html.Div(children, className=_bs_classname(type_, context), **kwargs)


# ----------------------------- #
#   general bootstrap stuff     #
# ----------------------------- #

def Container(children, **kwargs):
    """just a stupid wrapper to create the div and avoid typing"""
    return _html.Div(children=children, className='container', **kwargs)


def Bold(s):
    """take the provided string and insert it as child to a styled span"""
    return _html.Span(s, style={"font-weight": 'bold'})


def EnumLi(k, v):
    """convert a key and value to <li><bold>k</bold>: v</li>"""
    return _html.Li([Bold(k), ': {}'.format(v)])


# ----------------------------- #
#   components                  #
# ----------------------------- #

# let's just cover the hits here: https://getbootstrap.com/docs/4.1/components/

def Alert(children, context, **kwargs):
    """create a bootstrap alert with body `children` and context `context`

    all additional kwargs (e.g. `id` values) will be passed directly to the
    `html.Div` object constructor

    c.f. https://getbootstrap.com/docs/4.1/components/alerts/

    args:
        children (str or dash component): dash child element of this alert div
        context (str): the bootstrap context (required). acceptable values found
            in _BOOTSTRAP_CONTEXTS

    returns:
        html.Div: dash html Div component

    raises:
        EriDashBootstrapError

    """
    return _div_factory('alert', children, context, **kwargs)


def Badge(children, context, pill=False, href=None, **kwargs):
    """create a bootstrap badge with body `children` and context `context`

    all additional kwargs (e.g. `id` values) will be passed directly to the
    `html.Span` or `html.A` object constructor

    c.f. https://getbootstrap.com/docs/4.1/components/badges/

    args:
        children (str or dash component): the dash child element of this alert
            div
        context (str): the bootstrap context
        pill (bool): whether or not to set the pill class name (will round the
            edges of the badge) (default: False)
        href (str): if proved, this wil create an anchor instead of a span, and
            will set the hyperref (default: None)

    returns:
        html.Span or html.A: dash component (type depens on whether or not href
            is provided)

    raises:
        EriDashBootstrapError

    """
    _validate_context(context)
    className = _bs_classname('badge', context)
    if pill:
        className += ' badge-pill'

    if href is None:
        return _html.Span(children=children, className=className, **kwargs)
    else:
        return _html.A(
            children=children, className=className, href=href, **kwargs
        )


def Button(children, context=None, outline_only=False, size=None, **kwargs):
    """add bootstrap styling to the built-in html component button object

    this is functionally exactly identical to the `html.Button` function, except
    that it overloads the `style` value in `kwargs` (if it exists) to include
    the necessary bootstraps as determined by `context`, `outline_only`, and
    `size` information

    c.f. https://getbootstrap.com/docs/4.1/components/buttons/

    args:
        children (str or dash component): the dash child element of this alert
            div
        context (str): the bootstrap context (default: None)
        outline_only (bool): whether or not to create an outline-only button (no
            backgroudn color) (default: False)
        size (str): one of the bootstrap size values (default: None)

    returns:
        html.Button: dash html Button component

    raises:
        EriDashBootstrapError

    """
    _validate_context(context)
    _validate_size(size)

    className = _bs_classname('btn', context)
    try:
        # prepend the provided className string
        className = '{} {}'.format(kwargs.pop('className'), className)
    except KeyError:
        pass

    if outline_only:
        className += ' btn-outline-{}'.format(context)

    if size:
        className += ' btn-{}'.format(size)

    return _html.Button(children=children, className=className, **kwargs)


def Card(children, header=None, footer=None, outline_only=False, **kwargs):
    """create a bootstrap card with body `children`

    all additional kwargs (e.g. `id` values) will be passed directly to the
    `html.Span` or `html.A` object constructor

    c.f. https://getbootstrap.com/docs/4.1/components/card/

    args:
        children (str or list): the dash child element of this alert div
        header (str or list): the dash child element of the card-header div
        footer (str or list): the dash child element of the card-footer div
        outline_only (bool): whether or not to create an outline-only card (no
            backgroudn color) (default: False)

    returns:
        html.Div: dash html Div component

    raises:
        EriDashBootstrapError

    """
    card_children = []
    if header:
        card_children.append(_html.Div(children=header, className="card-header"))
    card_children.append(children)
    if footer:
        card_children.append(_html.Div(children=footer, className="card-footer"))

    return _html.Div(className='card', children=card_children, **kwargs)


def Jumbotron(header_name, header_text=None, **kwargs):
    """simplest possible jumbotron, less complicated than the other components
    (by choice)

    c.f. https://getbootstrap.com/docs/4.1/components/jumbotron/

    args:
        header_name (str): text of the main header
        header_text (str): additional "lead" (sub-header) text (default: None)

    returns:
        html.Div: dash html Div component

    raises:
        EriDashBootstrapError

    """
    return _html.Div(
        className='jumbotron jumbotron-fluid',
        children=[
            _html.Div(
                className='container',
                children=[
                    _html.H1(header_name, className='display-4'),
                    _html.P(header_text, className='lead')
                ]
            )
        ]
    )


class ListGroupItem():
    def __init__(self, children, context, active=False, disabled=False, href=None):
        self.children = children
        _validate_context(context)
        self.context = context
        self.active = active
        self.disabled = disabled
        self.href = href


def ListGroup(items, flush=False, **kwargs):
    """the listgroup is an unordered list with box styling

    the `items` object is any iterable of any number of the following two types
    of item elements:

        1. a dash-acceptable child element -- these will be passed directly as
           the children of the contained `li` elements. these items can just be
           strings (most obvious case)
        2. ListGroupItem objects -- the object defined above will be assumed to
           have the following properties
            1. `children`: the children elements, could be a string or a dash
               component list
            2. `context`: the bootstrap context, can be None
            3. `active`: whether or not the box item should have the "active"
               class
            4. `disabled`: whether or not the box item should have the
               "disabled" class
            5. `href`: if this is meant to be an anchor / list element, an href
               at which that anchor points

    we will not check the validity of child elements, so you may receive an
    error in the construction of the main div. this is probably overkill, yes.

    c.f. https://getbootstrap.com/docs/4.1/components/list-group/

    args:
        items (list): an indexable describing the items in the list group.
            individual items can be strings or ListGroupItems
        flush (bool): whether or not to add the `list-group-flush` class and
            remove all external borders / corners

    returns:
        html.Ul: dash html Ul component

    raises:
        EriDashBootstrapError

    """
    ulcn = 'list-group'
    if flush:
        ulcn += ' list-group-flush'

    ul_children = []

    for item in items:
        if isinstance(item, ListGroupItem):
            classes = [_bs_classname('list-group-item', item.context)]

            if item.active:
                classes.append('active')
            if item.disabled:
                classes.append('disabled')
            className = ' '.join(classes)

            if item.href:
                ul_children.append(
                    _html.A(
                        children=item.children, className=className,
                        href=item.href
                    )
                )
            else:
                ul_children.append(
                    _html.Li(children=item.children, className=className)
                )
        else:
            ul_children.append(
                _html.Li(children=item, className='list-group-item')
            )

    return _html.Ul(className=ulcn, children=ul_children)


def Nav(items, horiz_alignment=None, make_vertical=False, tabs=False,
        pills=False, fill=False, in_navbar=False, **kwargs):
    """the nav is the main element of a navigation bar, but not identical to it.
    rather, it is a container of clickable links (e.g. it could appear at the
    top of an open container underneath a jumbotron). if you are looking for a
    full top-running navbar, look to EriNavbar below

    the `items` object is an iterable of dictionaries with the following keys:

        1. `children`: the contents put in as the children of the html.A element
        2. `href`: the place the link points (will default to "#")
        3. `active`: a boolean value representing whether or not that tab is the
           active tab (will default to False)
        4. `disabled`: a boolean value representing whether or not that tab is
           disabled (greyed out) (will default to False)

    c.f. https://getbootstrap.com/docs/4.1/components/navs/

    args:
        items (list): an indexable describing the items in the nav. individual
            items must be dicts
        horiz_alignment (str): one of "left", "right", "center", or None; will
            determine how the list content is aligned within the containing div
            (default: None)
        make_vertical (bool): whether or not to make the nav list vertical
            instead of horizontal (c.f.
            https://getbootstrap.com/docs/4.1/components/navs/#vertical)
            (default: False)
        tabs (bool): whether or not to make the nav links into tabs
            (default: False)
        pills (bool): whether or not to make the nav links into pills
            (default: False)
        fill (bool): whether or not to fill the containing div (spread the nav
            elements out). this may not be compatible with alignment
            (default: False)
        in_navbar (bool): whether or not this nav element is within a larger
            navbar element (default: False)

    returns:
        html.Ul: dash html Ul component

    raises:
        EriDashBootstrapError

    """
    NAV = 'navbar-nav' if in_navbar else 'nav'

    ul_classes = [NAV]

    if horiz_alignment and make_vertical:
        raise EriDashBootstrapError(
            "horizontal alignment is not valid for a vertical nav list. provide"
            " one, not both"
        )

    _validate_h_alignment(horiz_alignment)
    if horiz_alignment:
        ul_classes.append(_BOOTSTRAP_HORIZ_ALIGN[horiz_alignment])

    if make_vertical:
        ul_classes.append('flex-column')

    if tabs:
        ul_classes.append('{}-tabs'.format(NAV))

    if pills:
        ul_classes.append('{}-pills'.format(NAV))

    if fill:
        ul_classes.append('{}-fill'.format(NAV))

    ul_className = ' '.join(ul_classes)

    ul_children = []
    for item in items:
        li_className = 'nav-item'
        a_className = 'nav-link'

        if item.get('active', False):
            a_className += ' active'

        if item.get('disabled', False):
            a_className += ' disabled'

        ul_children.append(_html.Li(
            className=li_className,
            children=[_html.A(
                className=a_className,
                href=item.get('href', '#'),
                children=item['children']
            )]
        ))

    return _html.Ul(className=ul_className, children=ul_children)


def Navbar(items, brand=None, pills=False, theme='dark', context=None,
           **kwargs):
    """the nav is a navigation bar, listing banner clickable links

    the `items` object is an iterable of dictionaries with the following keys:

        1. `children`: the contents put in as the children of the html.A element
        2. `href`: the place the link points (will default to "#")
        3. `active`: a boolean value representing whether or not that tab is the
           active tab (will default to False)
        4. `disabled`: a boolean value representing whether or not that tab is
           disabled (greyed out) (will default to False)

    c.f. https://getbootstrap.com/docs/4.1/components/navs/

    args:
        items (list): an indexable describing the items in the nav. individual
            items must be dicts
        brand (str): path to a local png image file that should be used as
            as the "brand" object, the leftmost element in the navigation bar
            (c.f. https://getbootstrap.com/docs/4.1/components/navbar/#brand).
            None will skip this (default: None)
        pills (bool): whether or not to make the nav links into pills
            (default: False)
        theme (str): one of the supported bootstrap color scheme themes
            (default: 'dark)
        context (str): the bootstrap context for the navbar coloring

    returns:
        html.Ul: dash html Ul component

    raises:
        EriDashBootstrapError

    """
    navbar_classes = ['navbar', 'navbar-expand-sm']

    if theme:
        _validate_color_theme(theme)
        navbar_classes.append('navbar-{}'.format(theme))

        # if theme was set but context was not, the best default for context is
        # theme (that is, if navbar-dark is set, bg-dark should also be set)
        context = context or theme

    if context:
        _validate_context(context)
        navbar_classes.append('bg-{}'.format(context))

    navbar_className = ' '.join(navbar_classes)

    navbar_children = []
    if brand:
        navbar_children.append(
            _html.A(className="navbar-brand", href="#", children=[
                _html.Img(src=brand, width='30', height='30', alt='')
            ])
        )

    # build nav
    navbar_children.append(
        _html.Div(
            #className='container',
            children=Nav(items, pills=pills, in_navbar=True)
        )
    )

    return _html.Div(
        className=navbar_className,
        children=navbar_children,
    )
