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
from skimage import io


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
            #Recupération du massif sur lequel on travail
            massif_travail = self.dlg.massifs.currentText()
            massif_travail = massif_travail.lower()


            # pour reprojeter en Lambert 93 
            # processing.runalg("qgis:reprojectlayer", area, "EPSG:2154", "massif")

            # Importation du shp qui décrit la zone et des ses coordonnées maximales et minimales
            area = QgsVectorLayer("/home/dpts/Bureau/Lien vers plugins/Opera/data/05/" + massif_travail + "/shp/" + massif_travail + ".shp", massif_travail, "ogr")
            xmin = area.extent().xMinimum()/1000
            xmax = area.extent().xMaximum()/1000
            ymin = area.extent().yMinimum()/1000
            ymax = area.extent().yMaximum()/1000
            

            # On va chercher toutes les tuiles du MNT correspondant aux bornes du shp
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
                    tile_mnt = QgsRasterLayer(path, "" + massif_travail + "_" + x_str + "_" + y_str)

                    # Si la couche est valide, on l'ajoute à la listte de couches
                    if tile_mnt.isValid():
                        mnt_list.append(tile_mnt)
                    
#            QgsMapLayerRegistry.instance().addMapLayers(mnt_list)
                   


            #Calcul du MNT de la zone entière
            mnt_path = "/home/dpts/Bureau/Lien vers plugins/Opera/data/05/" + massif_travail + "/mnt.tif"
            full_dem = QgsRasterLayer(mnt_path, "" + massif_travail + "_full_dem")

            if not full_dem.isValid():
                processing.runalg("gdalogr:merge",mnt_list,False,False,5,mnt_path)
                full_dem = QgsRasterLayer(mnt_path, "" + massif_travail + "_full_dem")
                
            # QgsMapLayerRegistry.instance().addMapLayer(full_dem)
            

            #Calcul de la carte des pentes
            slope_path = "/home/dpts/Bureau/Lien vers plugins/Opera/data/05/" + massif_travail + "/pente.tif"
            slope_map = QgsRasterLayer(slope_path, "" + massif_travail + "_slopes")

            if not slope_map.isValid():
                processing.runalg("gdalogr:slope",full_dem,1,False,False,False,1.0,slope_path)
                slope_map = QgsRasterLayer(slope_path, "" + massif_travail + "_slopes")
            
            # QgsMapLayerRegistry.instance().addMapLayer(slope_map)
            


            #Calcul de la carte des orientations
            aspect_path = "/home/dpts/Bureau/Lien vers plugins/Opera/data/05/" + massif_travail + "/orientation.tif"
            aspect_map = QgsRasterLayer(aspect_path, "" + massif_travail + "_aspect")

            if not aspect_map.isValid():
                processing.runalg("gdalogr:aspect",full_dem,1,False,False,False,False,aspect_path)
                aspect_map = QgsRasterLayer(aspect_path, "" + massif_travail + "_aspect")

            # QgsMapLayerRegistry.instance().addMapLayer(aspect_map)
            


            #Récuperation des données météo france du BRA
            url_meteo_fr = "http://www.meteofrance.com/mf3-rpc-portlet/rest/enneigement/bulletins/cartouches/AVDEPT05"
            response = urllib.urlopen(url_meteo_fr)
            bulletin_json = json.loads(response.read())
            for mass in bulletin_json:
                if mass["massif"]["slug"] == massif_travail:
                    print(mass["risque"]["pente"]["ne"])

            res = MRD(bulletin_json[5],slope_path,mnt_path)
            print("hey")





def MRD(BRA_massif,slope_map_path,full_dem_path):

    slope = np.array(io.imread(slope_map_path), dtype = float)
    dem = np.array(io.imread(full_dem_path), dtype = float)
    shape = slope.shape
    res = nb.zeros(shape)
    risque_ini = BRA_massif["risque"]["evolution"]["risqueInitial"]
    for l in range(shape[0]):
        for c in range (shape[1]):

            risque = risque_ini
            pente = slope[l][c]

            if dem[l][c] > 9000000: #TODO: thershold
                #risque = risque_evol
                pass


            if risque == 1:
                if pente > 40:
                    res[l][c] = 1

            elif risque == 2:
                if pente > 35:
                    res[l][c] = 1

            elif risque == 3:
                if pente > 30:
                    res[l][c] = 1

            elif risque == 4:
                if pente > 25:
                    res[l][c] = 1

            else:
                res[l][c] = 1

    io.imshow(res)
    return res
