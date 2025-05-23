# ***************************************************************************
# *   Copyright (c) 2009, 2010 Yorik van Havre <yorik@uncreated.net>        *
# *   Copyright (c) 2009, 2010 Ken Cline <cline@frii.com>                   *
# *   Copyright (c) 2020 FreeCAD Developers                                 *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************
"""Provides the object code for the Point object."""
## @package point
# \ingroup draftobjects
# \brief Provides the object code for the Point object.

## \addtogroup draftobjects
# @{
import math
from PySide.QtCore import QT_TRANSLATE_NOOP

import FreeCAD as App
from draftobjects.base import DraftObject
from draftutils import gui_utils


class Point(DraftObject):
    """The Draft Point object."""

    def __init__(self, obj, x=0, y=0, z=0):
        super().__init__(obj, "Point")

        _tip = QT_TRANSLATE_NOOP("App::Property", "X Location")
        obj.addProperty("App::PropertyDistance", "X", "Draft", _tip, locked=True)

        _tip = QT_TRANSLATE_NOOP("App::Property", "Y Location")
        obj.addProperty("App::PropertyDistance", "Y", "Draft", _tip, locked=True)

        _tip = QT_TRANSLATE_NOOP("App::Property", "Z Location")
        obj.addProperty("App::PropertyDistance", "Z", "Draft", _tip, locked=True)

        obj.X = x
        obj.Y = y
        obj.Z = z

        obj.setPropertyStatus('Placement', 'Hidden')

    def onDocumentRestored(self, obj):
        super().onDocumentRestored(obj)
        gui_utils.restore_view_object(obj, vp_module="view_point", vp_class="ViewProviderPoint")

    def execute(self, obj):
        base = obj.Placement.Base
        xyz_vec = App.Vector(obj.X.Value, obj.Y.Value, obj.Z.Value)

        if self.props_changed_placement_only():
            if base != xyz_vec:
                obj.X = base.x
                obj.Y = base.y
                obj.Z = base.z
            self.props_changed_clear()
            return

        import Part
        obj.Shape = Part.Vertex(App.Vector(0, 0, 0))
        if base != xyz_vec:
            obj.Placement.Base = xyz_vec
        self.props_changed_clear()

    def onChanged(self, obj, prop):
        self.props_changed_store(prop)


# Alias for compatibility with v0.18 and earlier
_Point = Point

## @}
