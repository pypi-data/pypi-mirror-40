from textwrap import dedent

import pytest
from zmei_generator.parser.parser import ZmeiParser


def _(code):
    parser = ZmeiParser()
    parser.parse_string(dedent(code))
    return parser.populate_collection_set('example')


def test_page_post():
    cs = _("""

        [boo]
        @post
    """)

    boo = cs.pages['boo']

    assert boo.allow_post is True


def test_page_post_with_code():
    cs = _("""

        [boo]
        @post {
            lala
        }
    """)

    boo = cs.pages['boo']

    assert boo.allow_post is True
    assert boo.page_code == '\nif request.method == "POST":\n    lala'


