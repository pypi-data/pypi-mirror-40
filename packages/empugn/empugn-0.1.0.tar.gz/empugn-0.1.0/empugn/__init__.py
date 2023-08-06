from collections.abc import Mapping, Sequence

from yattag import Doc

HTML_DOCTYPES = ['html', '5']
VOID_TAGS = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr']


def empugn(input, doctype='html'):
    """
    Given parsed YAML/JSON, outputs HTML or XML.
    """
    doc = Doc()

    if doctype:
        doc.asis('<!DOCTYPE {doctype}>'.format(doctype=doctype))

    _empugn(input, doc, doctype)

    return doc.getvalue()


def _empugn(input, doc, doctype):
    if input in (None, {}, []):
        pass
    elif isinstance(input, str):
        doc.text(input)
    elif isinstance(input, Sequence):
        for item in input:
            _empugn(item, doc, doctype)
    elif isinstance(input, Mapping):
        item, = input.items()
        tag_name, args = item

        if not isinstance(tag_name, str):
            raise TypeError('tag name must be a string, not {what}'.format(what=type(tag_name)))

        if isinstance(args, Mapping):
            attrs = args
            children = attrs.pop('children') if 'children' in attrs else []
        else:
            attrs = {}
            children = args

        if children:
            if doctype in HTML_DOCTYPES and tag_name in VOID_TAGS:
                raise ValueError('{tag_name} is a void tag and may not have children'.format(tag_name=tag_name))
            with doc.tag(tag_name, *attrs.items()):
                _empugn(children, doc, doctype)
        else:
            # Empty element
            if doctype in HTML_DOCTYPES:
                # outputting HTML, so need to take extra care with empty elements
                if tag_name in VOID_TAGS:
                    # while the / in <link /> is not required, it is allowed by the standard and ignored on void tags
                    doc.stag(tag_name, *attrs.items())
                else:
                    # <div /> on the other hand is not supported at all and will break in browsers, so emit <div></div>
                    with doc.tag(tag_name, *attrs.items()):
                        pass
            else:
                # outputting XML, so <foo /> is always ok
                doc.stag(tag_name, *attrs.items())

    else:
        doc.text(str(input))
