"""
Plugin for ResolveUrl
Copyright (C) 2020 gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import re
from resolveurl.plugins.lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError


class LetsUploadResolver(ResolveUrl):
    name = "letsupload.io"
    domains = ['letsupload.io', 'letsupload.org']
    pattern = r'(?://|\.)(letsupload\.(?:io|org))/([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.FF_USER_AGENT}
        html = self.net.http_GET(web_url, headers=headers).content
        r = re.search(r"href='([^']+)'>download\s*now", html)
        if r:
            common.kodi.sleep(3000)
            headers.update({'Referer': web_url})
            html = self.net.http_GET(r.group(1), headers=headers).content
            f = re.search(r'href="([^"]+)', html)
            if f:
                return f.group(1) + helpers.append_headers(headers)
        raise ResolverError('Video cannot be located.')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/{media_id}')
