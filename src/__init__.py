# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Opera
                                 A QGIS plugin
 Outil de Prévision Effective du Risque Avalanche
                             -------------------
        begin                : 2017-03-01
        copyright            : (C) 2017 by ENSG
        email                : irisdegelis@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Opera class from file Opera.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .OPERA import Opera
    return Opera(iface)
