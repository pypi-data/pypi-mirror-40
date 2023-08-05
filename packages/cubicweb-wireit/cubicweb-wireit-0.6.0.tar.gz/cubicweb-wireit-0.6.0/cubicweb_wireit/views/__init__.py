# -*- coding: utf-8 -*-
# copyright 2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""simple views (typically one line or so) for cubicweb-wireit"""

from cubicweb.predicates import is_instance
from cubicweb.web.views.baseviews import InContextView


class UploadedFileInContextView(InContextView):
    __regid__ = 'wireit_fileincontext'
    __select__ = InContextView.__select__ & is_instance('File')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        super(UploadedFileInContextView, self).cell_call(row, col)
        self.w('<img src="%s" alt="%s"/>' % (
            entity.icon_url(), self._cw._('icon for %s') % entity.data_format))
