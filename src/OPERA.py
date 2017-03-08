# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Opera
                                 A QGIS plugin
 Outil de Prévision Effective du Risque Avalanche
                              -------------------
        begin                : 2017-03-01
        git sha              : $Format:%H$
        copyright            : (C) 2017 by ENSG
        email                : irisdegelis@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from OPERA_dialog import OperaDialog
import os.path
import urllib
import json
import processing
from qgis.core import *
import numpy as np


class Opera:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Opera_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Opera')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Opera')
        self.toolbar.setObjectName(u'Opera')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Opera', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = OperaDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/Opera/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Opera'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # pour reprojeter en Lambert 93 
            #processing.runalg("qgis:reprojectlayer", thabor_area, "EPSG:2154", "thabor")
            thabor_area = QgsVectorLayer("/home/dpts/Bureau/Lien vers plugins/Opera/data/05/thabor/shp/thabor.shp", "thabor", "ogr")
            xmin = thabor_area.extent().xMinimum()/1000
            xmax = thabor_area.extent().xMaximum()/1000
            ymin = thabor_area.extent().yMinimum()/1000
            ymax = thabor_area.extent().yMaximum()/1000
            
            mnt_list = []
            for x in range (int((xmin//5)*5),int(np.ceil(xmax/5)*5),5):
                for y in range (int((ymin//5)*5+5),int(np.ceil(ymax/5)*5+5),5):
                    x_str = str(x)
                    y_str = str(y)
                    if x < 1000:
                        x_str = "0" + str(x)
                    if y < 1000:
                        y_str = "0" + str(y)
                    path = "/home/dpts/Bureau/Lien vers plugins/Opera/data/05/mnt/"
                    path += "RGEALTI_FXX_" + x_str + "_" + y_str + "_MNT_LAMB93_IGN69.tif"
                    tile_mnt = QgsRasterLayer(path, "thabor_" + x_str + "_" + y_str)
                    print(tile_mnt.isValid())
                    mnt_list.append(tile_mnt)
                    
            QgsMapLayerRegistry.instance().addMapLayers(mnt_list)      
                    
            print(mnt_list)
