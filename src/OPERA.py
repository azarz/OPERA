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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from OPERA_dialog import OperaDialog
import os.path

# Import des bibliopthèques pour lire le BRA en ligne
import urllib
import json

# Bibliothèques pour les traitements QGIS
import processing
from qgis.core import *
import numpy as np
from qgis.analysis import *
from qgis.gui import *
from qgis.utils import iface


# Chemin vers le plugin OPERA, par défaut ~/.qgis2/python/plugins/Opera
PATH_TO_OPERA_PLUGIN = "/home/dpts/.qgis2/python/plugins/Opera"

# Dictionnaire associant une couleur à un risque
RISK_COLOR_DICT = {'1': QColor(202,219,68,230), '2': QColor(255,241,0,230), '3': QColor(247,148,29,230), '4': QColor(238,28,27,230), '5': QColor(0,0,0,255)}
# Dictionnaire associant une couleur à un risque lorsqu'on est dans la partie noir de la rose des vents
RISK_ORIENT_COLOR_DICT = {'1': QColor(165,179,35,255), '2': QColor(229,187,0,255), '3': QColor(255,87,15,255), '4': QColor(161,13,13,255), '5': QColor(0,0,0,255)}

#Dictionnaire associant à une orientation la tranche en degré correspondant
ORIENTATION_DICT = {"ne" : "(ori@1 >= 22.5 AND ori@1 <67.5)",
                    "e" : "(ori@1 >= 67.5 AND ori@1 <112.5)",
                    "se" : "(ori@1 >= 112.5 AND ori@1 <157.5)",
                    "s" : "(ori@1 >= 157.5 AND ori@1 <202.5)",
                    "sw" : "(ori@1 >= 202.5 AND ori@1 <247.5)",
                    "w" : "(ori@1 >= 247.5 AND ori@1 <292.5)",
                    "nw" : "(ori@1 >= 292.5 AND ori@1 <337.5)",
                    "n" : "((ori@1 >= 337.5 AND ori@1 <360) OR (ori@1 >= 0 AND ori@1 <22.5))"}

class Bar(QProgressBar):
    value = 0
    def increaseValue(self):
        self.setValue(self.value)
        self.value += 1


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

    def checkbox_state_change(self):
        """Grise les options non utiles"""
        # Pour le chemin :
        self.dlg.couche_chemin.setEnabled(self.dlg.chemin_chkbx.isChecked())

        # Pour le BRA
        self.dlg.NE.setEnabled(self.dlg.radio_MRE.isChecked() and not self.dlg.checkBox.isChecked())
        self.dlg.N.setEnabled(self.dlg.radio_MRE.isChecked() and not self.dlg.checkBox.isChecked())
        self.dlg.NO.setEnabled(self.dlg.radio_MRE.isChecked() and not self.dlg.checkBox.isChecked())
        self.dlg.SE.setEnabled(self.dlg.radio_MRE.isChecked() and not self.dlg.checkBox.isChecked())
        self.dlg.SO.setEnabled(self.dlg.radio_MRE.isChecked() and not self.dlg.checkBox.isChecked())
        self.dlg.O.setEnabled(self.dlg.radio_MRE.isChecked() and not self.dlg.checkBox.isChecked())
        self.dlg.E.setEnabled(self.dlg.radio_MRE.isChecked() and not self.dlg.checkBox.isChecked())
        self.dlg.S.setEnabled(self.dlg.radio_MRE.isChecked() and not self.dlg.checkBox.isChecked())
        self.dlg.riskLow.setEnabled(not self.dlg.checkBox.isChecked())
        self.dlg.riskHigh.setEnabled(not self.dlg.checkBox.isChecked())
        self.dlg.altiThresh.setEnabled(not self.dlg.checkBox.isChecked())

    def run(self):
        """Run method that performs all the real work"""

        self.checkbox_state_change()

        # Ajoute le changement des champs lorsque les checkbox changent d'état
        self.dlg.checkBox.stateChanged.connect(self.checkbox_state_change)
        self.dlg.chemin_chkbx.stateChanged.connect(self.checkbox_state_change)
        self.dlg.radio_niveau.buttonClicked.connect(self.checkbox_state_change)


        # Population de la combobox pour le chemin
        self.dlg.couche_chemin.clear()
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == 0:
                self.dlg.couche_chemin.addItem(layer.name(), layer)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()



        # En appuyant sur la touche OK :
        if result:

            #Recupération du massif sur lequel on travaille
            massif_travail = self.dlg.massifs.currentText()
            massif_travail = massif_travail.lower()

            #Recupération de la methode
            niv_methode = self.dlg.radio_niveau.checkedButton().objectName()

            # Importation du shp qui décrit la zone et des ses coordonnées maximales et minimales
            area = QgsVectorLayer(PATH_TO_OPERA_PLUGIN + "/data/05/" + massif_travail + "/shp/" + massif_travail + ".shp", massif_travail, "ogr")
            xmin = area.extent().xMinimum()/1000
            xmax = area.extent().xMaximum()/1000
            ymin = area.extent().yMinimum()/1000
            ymax = area.extent().yMaximum()/1000

            root = QgsProject.instance().layerTreeRoot()
            gr_sc25 = root.addGroup("SC25_"+massif_travail)

            # Chargement des scan25 correspondant à la zone
            for x in range (int((xmin//10)*10),int(np.ceil(xmax/10)*10),10):
                    for y in range (int((ymin//10)*10+10),int(np.ceil(ymax/10)*10+10),10):

                        x_str = str(x)
                        y_str = str(y)

                        # On rjoute le 0 éventuel devant la centaine pour correspondre à la nomenclature IGN
                        if x < 1000:
                            x_str = "0" + str(x)
                        if y < 1000:
                            y_str = "0" + str(y)

                        path = PATH_TO_OPERA_PLUGIN + "/data/05/sc25/"
                        path += "SC25_TOUR_" + x_str + "_" + y_str + "_L93_E100.tif"
                        sc25 = QgsRasterLayer(path, "" + massif_travail + "_" + x_str + "_" + y_str)

                        # Si la couche est valide (si le fichier existe), on l'ajoute à la listte de couches
                        if sc25.isValid():
                            QgsMapLayerRegistry.instance().addMapLayer(sc25,False)
                            gr_sc25.insertLayer(1,sc25)


            # 1- MNT fusionné --------------------------------------------------------------------------
            # On cherche le MNT à son endroit normal
            mnt_path = PATH_TO_OPERA_PLUGIN + "/data/05/" + massif_travail + "/mnt.tif"
            full_dem = QgsRasterLayer(mnt_path, "" + massif_travail + "_full_dem")

            # Si le MNT couvrant la zone n'existe pas, on le crée
            if not full_dem.isValid():

                # On va chercher toutes les tuiles du MNT correspondant aux bornes du shp
                mnt_list = []

                for x in range (int((xmin//5)*5),int(np.ceil(xmax/5)*5),5):
                    for y in range (int((ymin//5)*5+5),int(np.ceil(ymax/5)*5+5),5):

                        x_str = str(x)
                        y_str = str(y)

                        # On rjoute le 0 éventuel devant la centaine pour correspondre à la nomenclature IGN
                        if x < 1000:
                            x_str = "0" + str(x)
                        if y < 1000:
                            y_str = "0" + str(y)

                        path = PATH_TO_OPERA_PLUGIN + "/data/05/mnt/"
                        path += "RGEALTI_FXX_" + x_str + "_" + y_str + "_MNT_LAMB93_IGN69.tif"
                        tile_mnt = QgsRasterLayer(path, "" + massif_travail + "_" + x_str + "_" + y_str)

                        # Si la couche est valide (si le fichier existe), on l'ajoute à la listte de couches
                        if tile_mnt.isValid():
                            mnt_list.append(tile_mnt)


                processing.runalg("gdalogr:merge",mnt_list,False,False,5,mnt_path)
                full_dem = QgsRasterLayer(mnt_path, "" + massif_travail + "_full_dem")
                
            #QgsMapLayerRegistry.instance().addMapLayer(full_dem)
            

            # 2- Carte des pentes --------------------------------------------------------------------------
            # On cherche la carte des pentes à son endroit normal
            slope_path = PATH_TO_OPERA_PLUGIN + "/data/05/" + massif_travail + "/pente.tif"
            slope_map = QgsRasterLayer(slope_path, "" + massif_travail + "_slopes")

            #Si elle n'existe pas, on la crée
            if not slope_map.isValid():
                processing.runalg("gdalogr:slope",full_dem,1,False,False,False,1.0,slope_path)
                slope_map = QgsRasterLayer(slope_path, "" + massif_travail + "_slopes")
            
            # QgsMapLayerRegistry.instance().addMapLayer(slope_map)
            


            # 3- Carte des orientations --------------------------------------------------------------------------
            # On cherche la carte des pentes à son endroit normal
            aspect_path = PATH_TO_OPERA_PLUGIN + "/data/05/" + massif_travail + "/orientation.tif"
            aspect_map = QgsRasterLayer(aspect_path, "" + massif_travail + "_aspect")

            #Si elle n'existe pas, on la crée
            if not aspect_map.isValid():
                processing.runalg("gdalogr:aspect",full_dem,1,False,False,False,False,aspect_path)
                aspect_map = QgsRasterLayer(aspect_path, "" + massif_travail + "_aspect")

            #QgsMapLayerRegistry.instance().addMapLayer(aspect_map)
            


            # 4- Récuperation des données du BRA Météo France -----------------------------------------------------
            
            # Si l'on charge le BRA automatiquement
            if self.dlg.checkBox.isChecked():
                # URL correspondant au JSON décrivant le BRA, les 2 derniers chiffres correspondant au numéro de département
                #url_meteo_fr = "http://www.meteofrance.com/mf3-rpc-portlet/rest/enneigement/bulletins/cartouches/AVDEPT05"
                url_meteo_fr = "/home/dpts/Bureau/Lien vers plugins/Opera/src/AVDEPT05.json"
                # On convertit la réponse en un dictionnaire Python
                response = urllib.urlopen(url_meteo_fr)
                bulletin_json = json.loads(response.read())

                # On recherche les prévisions par rapport au massif renseigné dans l'interface
                for mass in bulletin_json:
                    if mass["massif"]["slug"] == massif_travail:
                        bulletin_massif = mass


            # Sinon, on récupère les données entrées par l'utilisateur
            else:
                # Initialisation du bulletin
                bulletin_massif = {}
                bulletin_massif["risque"] = {}
                bulletin_massif["risque"]["evolution"] = {}
                bulletin_massif["risque"]["pente"] = {}
                bulletin_massif["risque"]["evolution"]["altitudeDependant"] = True

                # Récupération des valeurs entrées
                risque_bas = self.dlg.riskLow.currentText()
                risque_haut = self.dlg.riskHigh.currentText()
                thresh = self.dlg.altiThresh.value()

                # On applique ces valeurs au bulletin
                bulletin_massif["risque"]["evolution"]["risqueEvolution"] = risque_bas
                bulletin_massif["risque"]["evolution"]["risqueInitial"] = risque_bas
                bulletin_massif["risque"]["evolution"]["risqueEvolutionHighAltitude"] = risque_haut
                bulletin_massif["risque"]["evolution"]["risqueInitialHighAltitude"] = risque_haut

                bulletin_massif["risque"]["evolution"]["altitudeThreshold"] = thresh

                bulletin_massif["risque"]["pente"]["ne"] = self.dlg.NE.isChecked()
                bulletin_massif["risque"]["pente"]["n"] = self.dlg.N.isChecked()
                bulletin_massif["risque"]["pente"]["nw"] = self.dlg.NO.isChecked()
                bulletin_massif["risque"]["pente"]["se"] = self.dlg.SE.isChecked()
                bulletin_massif["risque"]["pente"]["sw"] = self.dlg.SO.isChecked()
                bulletin_massif["risque"]["pente"]["w"] = self.dlg.O.isChecked()
                bulletin_massif["risque"]["pente"]["e"] = self.dlg.E.isChecked()
                bulletin_massif["risque"]["pente"]["s"] = self.dlg.S.isChecked()

            #Lancement de l'algorithme de Munter correspondant au niveau choisi et affichage de la couche obtenue
            if niv_methode == "radio_MRD":
                print('MRD')
                mapRiskLayer, riskRenderer = MRD(bulletin_massif,slope_path,mnt_path, massif_travail)
                
            elif niv_methode == "radio_MRE":
                print('MRE')
                mapRiskLayer, riskRenderer = MRE(bulletin_massif,slope_path,mnt_path, aspect_path, massif_travail)

            else:
                print('MRP')
                mapRiskLayer, riskRenderer = MRP(bulletin_massif,slope_path,mnt_path, aspect_path, massif_travail)


            # Si l'on procède sur toute la zone, on affiche toute la zone, sinon, on n'affiche que le chemin
            if not self.dlg.chemin_chkbx.isChecked():
                mapRiskLayer.setCustomProperty("embeddedWidgets/count", 1)
                mapRiskLayer.setCustomProperty("embeddedWidgets/0/id", "transparency") 
                QgsMapLayerRegistry.instance().addMapLayer(mapRiskLayer)

            else:
                # Récupération du linearLayer à partir de l'interface
                indexCouche = self.dlg.couche_chemin.currentIndex()
                linearLayer = self.dlg.couche_chemin.itemData(indexCouche)
                risk_path(linearLayer, mapRiskLayer, riskRenderer)

            print("hey")



def MRD(BRA_massif, slope_map_path, full_dem_path, massif_travail):
    """
    Application de la méthode de réduction pour débutants ou élémentaire. Ajoute à la carte QGIS une carte quasi-binaire des régions
    dangereuses (2 en altitude haute, 1 sinon) ou non (0)

    :param BRA_massif: dictionnaire issu de BRA correspondant au massif de travail
    :type BRA_massif: dict

    :param slope_map_path: chaîne de caractères correspondant au chemin de la carte des pentes
    :type slope_map_path: str

    :param full_dem_path: chaîne de caractères correspondant au chemin du MNT du massif
    :type full_dem_path: str

    :param massif_travail: chaîne de caractères correspondant au massif de travail
    :type massif_travail: str

    :returns: Tuple de la couche de risque en sortie et de son style (renderer)
    :rtype: QgsRasterLayer, QgsSingleBandPseudoColorRenderer
    """

    # On importe la carte des pentes et le MNT
    slope_map = QgsRasterLayer(slope_map_path, "slopes")
    full_dem = QgsRasterLayer(full_dem_path, "full_dem")

    # List des entrées de la calculatrice raster
    entries = []
    # Définition des pentes
    slopes = QgsRasterCalculatorEntry()
    slopes.ref = 'slope@1'
    slopes.raster = slope_map
    slopes.bandNumber = 1
    entries.append(slopes)
    # Définition des altitudes
    altitude = QgsRasterCalculatorEntry()
    altitude.ref = 'alti@1'
    altitude.raster = full_dem
    altitude.bandNumber = 1
    entries.append(altitude)

    # Extraction du risque depuis le BRA : maximum entre le risque initial et le risque évolution (qui vaut 0 s'il n'y a pas d'évolution)
    risque = str(max(BRA_massif["risque"]["evolution"]["risqueEvolution"], BRA_massif["risque"]["evolution"]["risqueInitial"]))

    # Extraction du seuil d'altitude. Vaut 0 si ça ne dépend pas de l'altitude
    altitudeThreshold = str(BRA_massif["risque"]["evolution"]["altitudeThreshold"]) 

    # Extraction du risque en altitude. S'il n'y a qu'un seul niveau de risque en fonction de l'altitude, on prend donc le même risque.
    if BRA_massif["risque"]["evolution"]["altitudeDependant"]:
        risque_alt = str(max(BRA_massif["risque"]["evolution"]["risqueEvolutionHighAltitude"], BRA_massif["risque"]["evolution"]["risqueInitialHighAltitude"]))
    else:
        risque_alt = risque

    # Ajout du terme de difficulté : la MRE permet d'accéder à des pentes supérieures de 5° à la MRD
    terme_difficulte = 0.
    method_type = "mrd"



    #Définition de la formule, elle vaut 0 si l'on peut skier, 1 si l'on ne peut pas skier en altitude basse et 2 si l'on ne peut pas skier en altitude haute
    # Cas du risque 1:
    formula = "(slope@1 >= " + str(40. + terme_difficulte) + ") * (alti@1 < " + altitudeThreshold + ") * (" + risque + " = 1) + " # Cas de l'altitude basse
    formula+= "2 * (slope@1 >= " + str(40. + terme_difficulte) + ") * (alti@1 >= " + altitudeThreshold + ") * (" + risque_alt + " = 1) + " #Cas de l'altitude haute
    # Cas du risque 2:
    formula+= "(slope@1 >= " + str(35. + terme_difficulte) + ") * (alti@1 < " + altitudeThreshold + ") * (" + risque + " = 2) + " # Cas de l'altitude basse
    formula+= "2 * (slope@1 >= " + str(35. + terme_difficulte) + ") * (alti@1 >= " + altitudeThreshold + ") * (" + risque_alt + " = 2) + " #Cas de l'altitude haute
    # Cas du risque 3:
    formula+= "(slope@1 >= " + str(30. + terme_difficulte) + ") * (alti@1 < " + altitudeThreshold + ") * (" + risque + " = 3) + " # Cas de l'altitude basse
    formula+= "2 * (slope@1 >= " + str(30. + terme_difficulte) + ") * (alti@1 >= " + altitudeThreshold + ") * (" + risque_alt + " = 3) + " #Cas de l'altitude haute
    # Cas du risque 4:
    formula+= "(slope@1 >= " + str(25. + terme_difficulte) + ") * (alti@1 < " + altitudeThreshold + ") * (" + risque + " = 4) + " # Cas de l'altitude basse
    formula+= "2 * (slope@1 >= " + str(25. + terme_difficulte) + ") * (alti@1 >= " + altitudeThreshold + ") * (" + risque_alt + " = 4) +" #Cas de l'altitude haute
    # Cas du risque 5:
    formula+= "(slope@1 >= " + str(15. + terme_difficulte) + ") * (alti@1 < " + altitudeThreshold + ") * (" + risque + " = 5) + " # Cas de l'altitude basse
    formula+= "2 * (slope@1 >= " + str(15. + terme_difficulte) + ") * (alti@1 >= " + altitudeThreshold + ") * (" + risque_alt + " = 5)" #Cas de l'altitude haute

    # Chemin de sortie de la couche
    output_path = PATH_TO_OPERA_PLUGIN + '/tmp/' + massif_travail + '/' + method_type + '.tif'
    # Définition de l'instance de RasterCalculator à partir de la formule définie au dessus, et des dimensions de la carte des pentes
    calc = QgsRasterCalculator( formula, 
        output_path, 'GTiff', slope_map.extent(), slope_map.width(), slope_map.height(), entries)
    # On effectue le calcul
    calc.processCalculation()

    # On importe la carte obtenue en tant que couche QGIS
    layer_name = "output_" + method_type

    output_map = QgsRasterLayer(output_path, layer_name)

    # Définition du style d'affichage
    fcn = QgsColorRampShader()
    fcn.setColorRampType(QgsColorRampShader.INTERPOLATED)
    # Couleurs en fonction du risque et de la valeur du pixel
    lst = [ QgsColorRampShader.ColorRampItem(0, QColor(255,255,255,0)),
            QgsColorRampShader.ColorRampItem(1, RISK_COLOR_DICT[risque], "zone risque " + risque), 
            QgsColorRampShader.ColorRampItem(2, RISK_COLOR_DICT[risque_alt], "zone risque " + risque_alt) ]
    fcn.setColorRampItemList(lst)
    shader = QgsRasterShader()
    shader.setRasterShaderFunction(fcn)
    # On associe le style à la couche
    renderer = QgsSingleBandPseudoColorRenderer(output_map.dataProvider(), 1, shader)
    renderer.setOpacity(0.65)
    output_map.setRenderer(renderer)

    # On retourne la couche de sortie et son style
    return output_map, lst



def MRE(BRA_massif, slope_map_path, full_dem_path, aspect_map_path, massif_travail):
    """
    Application de la méthode de réduction pour débutants ou élémentaire. Ajoute à la carte QGIS une carte quasi-binaire des régions
    dangereuses (2 en altitude haute, 1 sinon) ou non (0)

    :param BRA_massif: dictionnaire issu de BRA correspondant au massif de travail
    :type BRA_massif: dict

    :param slope_map_path: chaîne de caractères correspondant au chemin de la carte des pentes
    :type slope_map_path: str

    :param full_dem_path: chaîne de caractères correspondant au chemin du MNT du massif
    :type full_dem_path: str

    :param massif_travail: chaîne de caractères correspondant au massif de travail
    :type massif_travail: str

    :returns: Tuple de la couche de risque en sortie et de son style (renderer)
    :rtype: QgsRasterLayer, QgsSingleBandPseudoColorRenderer
    """

    # On importe la carte des pentes et le MNT
    slope_map = QgsRasterLayer(slope_map_path, "slopes")
    full_dem = QgsRasterLayer(full_dem_path, "full_dem")
    aspect_map = QgsRasterLayer(aspect_map_path, "aspects")

    # List des entrées de la calculatrice raster
    entries = []
    # Définition des pentes
    slopes = QgsRasterCalculatorEntry()
    slopes.ref = 'slope@1'
    slopes.raster = slope_map
    slopes.bandNumber = 1
    entries.append(slopes)
    # Définition des altitudes
    altitude = QgsRasterCalculatorEntry()
    altitude.ref = 'alti@1'
    altitude.raster = full_dem
    altitude.bandNumber = 1
    entries.append(altitude)

    #Définition des orientations
    orientation = QgsRasterCalculatorEntry()
    orientation.ref = 'ori@1'
    orientation.raster = aspect_map
    orientation.bandNumber = 1
    entries.append(orientation)


    # Extraction du risque depuis le BRA : maximum entre le risque initial et le risque évolution (qui vaut 0 s'il n'y a pas d'évolution)
    risque = str(max(BRA_massif["risque"]["evolution"]["risqueEvolution"], BRA_massif["risque"]["evolution"]["risqueInitial"]))

    # Extraction du seuil d'altitude. Vaut 0 si ça ne dépend pas de l'altitude
    altitudeThreshold = str(BRA_massif["risque"]["evolution"]["altitudeThreshold"]) 

    # Extraction du risque en altitude. S'il n'y a qu'un seul niveau de risque en fonction de l'altitude, on prend donc le même risque.
    if BRA_massif["risque"]["evolution"]["altitudeDependant"]:
        risque_alt = str(max(BRA_massif["risque"]["evolution"]["risqueEvolutionHighAltitude"], BRA_massif["risque"]["evolution"]["risqueInitialHighAltitude"]))
    else:
        risque_alt = risque

    # Ajout du terme de difficulté : la MRE permet d'accéder à des pentes supérieures de 5° à la MRD   
    terme_difficulte = 5.
    method_type = "mre"



    #Définition de la formule, elle vaut 0 si l'on peut skier, 1 si l'on ne peut pas skier en altitude basse et 2 si l'on ne peut pas skier en altitude haute (*3 si on est dans les mauvaises orientations)
    # Cas du risque 1:
    formula = "((slope@1 >= " + str(40. + terme_difficulte) + ") * (alti@1 < " + altitudeThreshold + ") * (" + risque + " = 1) + " # Cas de l'altitude basse
    formula+= "2 * (slope@1 >= " + str(40. + terme_difficulte) + ") * (alti@1 >= " + altitudeThreshold + ") * (" + risque_alt + " = 1) + " #Cas de l'altitude haute
    # Cas du risque 2:
    formula+= "(slope@1 >= " + str(35. + terme_difficulte) + ") * (alti@1 < " + altitudeThreshold + ") * (" + risque + " = 2) + " # Cas de l'altitude basse
    formula+= "2 * (slope@1 >= " + str(35. + terme_difficulte) + ") * (alti@1 >= " + altitudeThreshold + ") * (" + risque_alt + " = 2) + " #Cas de l'altitude haute
    # Cas du risque 3:
    formula+= "(slope@1 >= " + str(30. + terme_difficulte) + ") * (alti@1 < " + altitudeThreshold + ") * (" + risque + " = 3) + " # Cas de l'altitude basse
    formula+= "2 * (slope@1 >= " + str(30. + terme_difficulte) + ") * (alti@1 >= " + altitudeThreshold + ") * (" + risque_alt + " = 3) + " #Cas de l'altitude haute
    # Cas du risque 4:
    formula+= "(slope@1 >= " + str(25. + terme_difficulte) + ") * (alti@1 < " + altitudeThreshold + ") * (" + risque + " = 4) + " # Cas de l'altitude basse
    formula+= "2 * (slope@1 >= " + str(25. + terme_difficulte) + ") * (alti@1 >= " + altitudeThreshold + ") * (" + risque_alt + " = 4) +" #Cas de l'altitude haute
    # Cas du risque 5:
    formula+= "(slope@1 >= " + str(15. + terme_difficulte) + ") * (alti@1 < " + altitudeThreshold + ") * (" + risque + " = 5) + " # Cas de l'altitude basse
    formula+= "2 * (slope@1 >= " + str(15. + terme_difficulte) + ") * (alti@1 >= " + altitudeThreshold + ") * (" + risque_alt + " = 5))" #Cas de l'altitude haute
    #Prise en compte de l'orientation
    formula+= " + " 
    #S
    formula += " (.5*(" + str(int(bool(BRA_massif["risque"]["pente"]["s"]))) + "*" + ORIENTATION_DICT["s"] + ") + "
    #SW
    formula += " + .5*(" + str(int(bool(BRA_massif["risque"]["pente"]["sw"]))) + "*" + ORIENTATION_DICT["sw"] + ") + "
    #W
    formula += " + .5*(" + str(int(bool(BRA_massif["risque"]["pente"]["w"]))) + "*" + ORIENTATION_DICT["w"] + ") + "
    #NW
    formula += " + .5*(" + str(int(bool(BRA_massif["risque"]["pente"]["nw"]))) + "*" + ORIENTATION_DICT["nw"] + ") + "
    #N
    formula += " + .5*(" + str(int(bool(BRA_massif["risque"]["pente"]["n"])))+ "*" + ORIENTATION_DICT["n"] + "))"

    # Chemin de sortie de la couche
    output_path = PATH_TO_OPERA_PLUGIN + '/tmp/' + massif_travail + '/' + method_type + '.tif'
    # Définition de l'instance de RasterCalculator à partir de la formule définie au dessus, et des dimensions de la carte des pentes
    calc = QgsRasterCalculator( formula, 
        output_path, 'GTiff', slope_map.extent(), slope_map.width(), slope_map.height(), entries)
    # On effectue le calcul
    calc.processCalculation()

    # On importe la carte obtenue en tant que couche QGIS
    layer_name = "output_" + method_type

    output_map = QgsRasterLayer(output_path, layer_name)

    # Définition du style d'affichage
    fcn = QgsColorRampShader()
    fcn.setColorRampType(QgsColorRampShader.INTERPOLATED)
    # Couleurs en fonction du risque et de la valeur du pixel
    lst = [ QgsColorRampShader.ColorRampItem(0, QColor(255,255,255,0)),
            QgsColorRampShader.ColorRampItem(0.5, QColor(255,255,255,0)),
            QgsColorRampShader.ColorRampItem(1, RISK_COLOR_DICT[risque], "zone risque " + risque), 
            QgsColorRampShader.ColorRampItem(1.5, RISK_ORIENT_COLOR_DICT[risque], "zone risque " + risque + " mauvaise orientation"), 
            QgsColorRampShader.ColorRampItem(2, RISK_COLOR_DICT[risque_alt], "zone risque " + risque_alt), 
            QgsColorRampShader.ColorRampItem(2.5, RISK_ORIENT_COLOR_DICT[risque_alt], "zone risque " + risque_alt + " mauvaise orientation") ]
    fcn.setColorRampItemList(lst)
    shader = QgsRasterShader()
    shader.setRasterShaderFunction(fcn)
    # On associe le style à la couche
    renderer = QgsSingleBandPseudoColorRenderer(output_map.dataProvider(), 1, shader)
    renderer.setOpacity(0.65)
    output_map.setRenderer(renderer)

    # On retourne la couche de sortie et son style
    return output_map, lst





def MRP(BRA_massif,slope_map_path, full_dem_path, aspect_map_path, massif_travail):
    """
    Application de la méthode de réduction pour experts

    :param BRA_massif: dictionnaire issu de BRA correspondant au massif de travail
    :type BRA_massif: dict

    :param slope_map_path: chaîne de caractères correspondant au chemin de la carte des pentes
    :type slope_map_path: str

    :param full_dem_path: chaîne de caractères correspondant au chemin du MNT du massif
    :type full_dem_path: str

    :param full_dem_path: chaîne de caractères correspondant au chemin de la carte des orientations
    :type full_dem_path: str

    :param massif_travail: chaîne de caractères correspondant au massif de travail
    :type massif_travail: str

    :returns: Tuple de la couche de risque en sortie et de son style (renderer)
    :rtype: QgsRasterLayer, QgsSingleBandPseudoColorRenderer
    """

    # On importe la carte des pentes et le MNT
    slope_map = QgsRasterLayer(slope_map_path, "slopes")
    full_dem = QgsRasterLayer(full_dem_path, "full_dem")
    aspect_map = QgsRasterLayer(aspect_map_path, "aspects")

    # List des entrées de la calculatrice raster
    entries = []
    # Définition des pentes
    slopes = QgsRasterCalculatorEntry()
    slopes.ref = 'slope@1'
    slopes.raster = slope_map
    slopes.bandNumber = 1
    entries.append(slopes)
    # Définition des altitudes
    altitude = QgsRasterCalculatorEntry()
    altitude.ref = 'alti@1'
    altitude.raster = full_dem
    altitude.bandNumber = 1
    entries.append(altitude)

    #Définition des orientations
    orientation = QgsRasterCalculatorEntry()
    orientation.ref = 'ori@1'
    orientation.raster = aspect_map
    orientation.bandNumber = 1
    entries.append(orientation)


    # Extraction du risque depuis le BRA : maximum entre le risque initial et le risque évolution (qui vaut 0 s'il n'y a pas d'évolution)
    risque = str(max(BRA_massif["risque"]["evolution"]["risqueEvolution"], BRA_massif["risque"]["evolution"]["risqueInitial"]))

    # Extraction du seuil d'altitude. Vaut 0 si ça ne dépend pas de l'altitude
    altitudeThreshold = str(BRA_massif["risque"]["evolution"]["altitudeThreshold"]) 

    # Extraction du risque en altitude. S'il n'y a qu'un seul niveau de risque en fonction de l'altitude, on prend donc le même risque.
    if BRA_massif["risque"]["evolution"]["altitudeDependant"]:
        risque_alt = str(max(BRA_massif["risque"]["evolution"]["risqueEvolutionHighAltitude"], BRA_massif["risque"]["evolution"]["risqueInitialHighAltitude"]))
    else:
        risque_alt = risque

    potentiel_danger = 2**(float(risque))
    potentiel_danger_alt = 2**(float(risque_alt))


    #Définition de la formule, elle est inferieure ou égale à 1 si l'on peut skier, entre 1 et 1.3, il faut faire attention et elle est supéreirue à 1.3 si l'on ne peut pas skier
    formula = "((alti@1 < " + altitudeThreshold + ")*" + str(potentiel_danger) + "+ (alti@1 >= " + altitudeThreshold + ")*" + str(potentiel_danger_alt) +  ")/("
    # Coefficient d'inclinaison
    formula += "(((" + str(30.) + "<= slope@1 AND slope@1 < " + str(34.) + ")*4)"
    formula += " + ((" + str(34.) + "<= slope@1 AND slope@1 < " + str(36.) + ")*3)"
    formula += " + ((" + str(36.) + "<= slope@1 AND slope@1 <= " + str(39.) + ")*2)"
    formula += " + (slope@1 > " + str(39.) + ")"
    formula += " + ((slope@1 < " + str(30.) + ")*5))"

    # Coefficient d'orientation
    formula += "* ( 3 * (ori@1 > 112.5 AND ori@1 < 292.5)"
    formula += " + 2 * ((ori@1 > 45 AND ori@1 <=112.5) OR (ori@1 >= 292.5 AND ori@1 <315)  )"
    formula += " + ((ori@1 > 0 AND ori@1 <= 45 ) OR ( ori@1 >= 315 AND ori@1 <= 360 )))"
    formula += ")"

    # Chemin de sortie de la couche
    output_path = PATH_TO_OPERA_PLUGIN + '/tmp/' + massif_travail + '/mrp' + '.tif'
    # Définition de l'instance de RasterCalculator à partir de la formule définie au dessus, et des dimensions de la carte des pentes
    calc = QgsRasterCalculator( formula, 
        output_path, 'GTiff', slope_map.extent(), slope_map.width(), slope_map.height(), entries)
    # On effectue le calcul
    calc.processCalculation()

    # On importe la carte obtenue en tant que couche QGIS
    layer_name = "output_mrp"

    output_map = QgsRasterLayer(output_path, layer_name)

    # Définition du style d'affichage
    fcn = QgsColorRampShader()
    fcn.setColorRampType(QgsColorRampShader.INTERPOLATED)
    # Couleurs en fonction de la valeur du pixel
    lst = [ QgsColorRampShader.ColorRampItem(0, QColor(0,255,0,0)), 
            QgsColorRampShader.ColorRampItem(0.99, QColor(0,255,0,0), "Risque résiduel :"), 
            QgsColorRampShader.ColorRampItem(1, RISK_COLOR_DICT['2'], "1"), 
            QgsColorRampShader.ColorRampItem(4, RISK_COLOR_DICT['4'], "4"), 
            QgsColorRampShader.ColorRampItem(8, QColor(190,30,46,230), "8")]
    fcn.setColorRampItemList(lst)
    shader = QgsRasterShader()
    shader.setRasterShaderFunction(fcn)
    # On associe le style à la couche
    renderer = QgsSingleBandPseudoColorRenderer(output_map.dataProvider(), 1, shader)
    renderer.setOpacity(0.65)
    output_map.setRenderer(renderer)

    # On retourne la couche de sortie et son style
    return output_map, lst



def risk_path(linearLayer, mapRiskLayer, riskRenderer):
    """
    Fonction qui à partir d'une polyligne verteur et d'une carte des risques renvoie les risques sur le chemin

    :param linearLayer: couche vecteur du chemin
    :type linearLayer: QgsVectorLayer

    :param linearLayer: couche raster correspondant à la carte des risques
    :type linearLayer: QgsRasterLayer

    :param linearLayer: renderer associé à la carte des risques
    :type linearLayer: QgsSingleBandPseudoColorRenderer
    """

    # Si besoin, on reprojette le chemin en Lambert 93
    if linearLayer.crs().authid() != "EPSG:2154":
        linLay = processing.runalg("qgis:reprojectlayer", linearLayer, "EPSG:2154", None)
        linearLayer = QgsVectorLayer(linLay['OUTPUT'], "chemin")

    # Définition d'un buffer autour du chemin (distance de 30 mètres pour avoir une largeur de 60 mètres)
    buff = processing.runalg('qgis:fixeddistancebuffer', linearLayer, 30, 5, True, None)
    
    # "Emporte-pièce" de la carte de risque à partir du buffer obtenu
    path = processing.runalg('gdalogr:warpreproject', {"INPUT": mapRiskLayer, "SOURCE_SRS": "EPSG:2154", 
                                                "DEST_SRS": "EPSG:2154", "TR": 0.0, "METHOD": 0, 
                                                "EXTRA": "-cutline " + buff['OUTPUT'], "RTYPE": 5, "OUTPUT": None})

    path_raster = QgsRasterLayer(path['OUTPUT'], "risks_along_path")

    # Définition du style d'affichage
    fcn = QgsColorRampShader()
    fcn.setColorRampType(QgsColorRampShader.INTERPOLATED)
    # Couleurs en fonction du renderer de la méthode
    fcn.setColorRampItemList(riskRenderer)
    shader = QgsRasterShader()
    shader.setRasterShaderFunction(fcn)
    # On associe le style à la couche
    renderer = QgsSingleBandPseudoColorRenderer(path_raster.dataProvider(), 1, shader)
    renderer.setOpacity(1)
    path_raster.setRenderer(renderer)
    
    QgsMapLayerRegistry.instance().addMapLayer(path_raster)

    return None