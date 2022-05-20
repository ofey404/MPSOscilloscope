import logging

from controller.pluginManager import PluginStatus
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QListWidget, QPushButton

logger = logging.getLogger(__name__)


class PluginPanelControl(QObject):
    pluginStatusUpdated = pyqtSignal(PluginStatus)

    def __init__(self,
                 updatePluginButton: QPushButton,
                 configFilePathLineEdit: QLineEdit,
                 enabledPluginsListWidget: QListWidget,
                 allAvailablePluginsListWidget: QListWidget,
                 pluginAddButton: QPushButton,
                 pluginRemoveButton: QPushButton,
                 ) -> None:
        super().__init__()
        self.updatePluginButton = updatePluginButton
        self.configFilePathLineEdit = configFilePathLineEdit
        self.enabledPluginsListWidget = enabledPluginsListWidget
        self.allAvailablePluginsListWidget = allAvailablePluginsListWidget
        self.pluginAddButton = pluginAddButton
        self.pluginRemoveButton = pluginRemoveButton

        self.cachedPluginStatus = None
        self._connectSignals()

    def updatePluginStatus(self):
        pList = self.cachedPluginStatus.orderedPostProcessor
        pList.clear()
        for i, plugin in enumerate(self.cachedPluginStatus.allPlugins):
            if self._pluginNameInEnabled(plugin.getMetadata().display_name):
                self.cachedPluginStatus.enabled[i] = True
                processor = plugin.getProcessor()
                # FIXME: Ugly... move this logic to pluginManager.
                if processor is not None:
                    pList.append(processor)
            else:
                self.cachedPluginStatus.enabled[i] = False
        self.pluginStatusUpdated.emit(self.cachedPluginStatus)

    def respondToPluginStatus(self, status: PluginStatus):
        # Cache status in front end.
        self.cachedPluginStatus = status

        lwAll = self.allAvailablePluginsListWidget
        lwEnabled = self.enabledPluginsListWidget
        lwAll.clear()
        lwEnabled.clear()
        for p, enabled in zip(status.allPlugins, status.enabled):
            name = p.getMetadata().display_name
            lwAll.addItem(name)
            if enabled:
                lwEnabled.addItem(name)

    def _pluginNameInEnabled(self, name):
        lwEnabled = self.enabledPluginsListWidget
        for i in range(lwEnabled.count()):
            if lwEnabled.item(i).text() == name:
                return True
        return False

    def _enableSelectedPlugin(self):
        lwAll = self.allAvailablePluginsListWidget
        lwEnabled = self.enabledPluginsListWidget

        currentRow = lwAll.currentRow()
        currentName = lwAll.item(currentRow).text()
        if not self._pluginNameInEnabled(currentName):
            lwEnabled.addItem(currentName)
            logger.info("Plugin enabled.")

    def _disableSelectedPlugin(self):
        lwEnabled = self.enabledPluginsListWidget
        currentRow = lwEnabled.currentRow()
        lwEnabled.takeItem(currentRow)
        logger.info("Plugin disabled.")

    def _connectSignals(self):
        self.updatePluginButton.clicked.connect(self.updatePluginStatus)
        self.pluginAddButton.clicked.connect(self._enableSelectedPlugin)
        self.pluginRemoveButton.clicked.connect(self._disableSelectedPlugin)
