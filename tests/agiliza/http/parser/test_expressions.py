"""
This file is part of Agiliza.

Agiliza is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Agiliza is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Agiliza.  If not, see <http://www.gnu.org/licenses/>.


Copyright (c) 2012 Vicente Ruiz <vruiz2.0@gmail.com>
"""
import unittest

from agiliza.http.parser.expressions import ACCEPT_MEDIA_RANGE


class ExpressionsTest(unittest.TestCase):

    def test_accept_media_range_must_match_all_types(self):
        match = ACCEPT_MEDIA_RANGE.match('*/*')

        self.assertNotEqual(
            match, None,
            "ACCEPT_MEDIA_RANGE does not accept all types"
        )

    def test_accept_media_range_must_accept_parameters(self):
        match = ACCEPT_MEDIA_RANGE.match('text/x-dvi; q=0.8')

        self.assertNotEqual(
            match, None,
            "ACCEPT_MEDIA_RANGE does not accept parameters"
        )

    def test_accept_media_range_must_not_match_some_text(self):
        match = ACCEPT_MEDIA_RANGE.match('Some text')

        self.assertEqual(
            match, None,
            "ACCEPT_MEDIA_RANGE accepts some text"
        )

    def test_accept_media_range_must_fetch_right_values(self):
        match = ACCEPT_MEDIA_RANGE.match('text/plain; q=0.5')

        media_type = match.group('type') or '*'
        media_subtype = match.group('subtype') or '*'
        media_q = float(match.group('q') or 1.0)

        match_dict = {
            'type': media_type,
            'subtype': media_subtype,
            'q': media_q
        }

        self.assertDictEqual(match_dict, {
                'type': 'text',
                'subtype': 'plain',
                'q': 0.5,
            },
            "ACCEPT_MEDIA_RANGE does not fetch right values"
        )


if __name__ == '__main__':
    unittest.main()
