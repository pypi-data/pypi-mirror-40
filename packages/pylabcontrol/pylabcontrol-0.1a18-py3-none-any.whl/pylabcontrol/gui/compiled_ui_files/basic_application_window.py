# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basic_application_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1733, 926)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_scripts = QtWidgets.QWidget()
        self.tab_scripts.setObjectName("tab_scripts")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_scripts)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.btn_store_script_data = QtWidgets.QPushButton(self.tab_scripts)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_store_script_data.setFont(font)
        self.btn_store_script_data.setObjectName("btn_store_script_data")
        self.horizontalLayout_4.addWidget(self.btn_store_script_data)
        self.btn_load_scripts = QtWidgets.QPushButton(self.tab_scripts)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_load_scripts.setFont(font)
        self.btn_load_scripts.setObjectName("btn_load_scripts")
        self.horizontalLayout_4.addWidget(self.btn_load_scripts)
        self.chk_show_all = QtWidgets.QCheckBox(self.tab_scripts)
        self.chk_show_all.setToolTip("")
        self.chk_show_all.setObjectName("chk_show_all")
        self.horizontalLayout_4.addWidget(self.chk_show_all)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.tree_scripts = QtWidgets.QTreeWidget(self.tab_scripts)
        self.tree_scripts.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_scripts.sizePolicy().hasHeightForWidth())
        self.tree_scripts.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tree_scripts.setFont(font)
        self.tree_scripts.setAutoFillBackground(False)
        self.tree_scripts.setLineWidth(1)
        self.tree_scripts.setMidLineWidth(0)
        self.tree_scripts.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tree_scripts.setAlternatingRowColors(True)
        self.tree_scripts.setWordWrap(True)
        self.tree_scripts.setHeaderHidden(False)
        self.tree_scripts.setObjectName("tree_scripts")
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_scripts)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item_0.setFont(0, font)
        item_0.setCheckState(0, QtCore.Qt.Checked)
        item_0 = QtWidgets.QTreeWidgetItem(self.tree_scripts)
        item_0.setCheckState(0, QtCore.Qt.Checked)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.tree_scripts.header().setDefaultSectionSize(300)
        self.tree_scripts.header().setHighlightSections(True)
        self.verticalLayout_4.addWidget(self.tree_scripts)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_start_script = QtWidgets.QPushButton(self.tab_scripts)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_start_script.setFont(font)
        self.btn_start_script.setObjectName("btn_start_script")
        self.horizontalLayout_5.addWidget(self.btn_start_script)
        self.btn_stop_script = QtWidgets.QPushButton(self.tab_scripts)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_stop_script.setFont(font)
        self.btn_stop_script.setObjectName("btn_stop_script")
        self.horizontalLayout_5.addWidget(self.btn_stop_script)
        self.btn_skip_subscript = QtWidgets.QPushButton(self.tab_scripts)
        self.btn_skip_subscript.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_skip_subscript.setFont(font)
        self.btn_skip_subscript.setObjectName("btn_skip_subscript")
        self.horizontalLayout_5.addWidget(self.btn_skip_subscript)
        self.btn_validate_script = QtWidgets.QPushButton(self.tab_scripts)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_validate_script.setFont(font)
        self.btn_validate_script.setObjectName("btn_validate_script")
        self.horizontalLayout_5.addWidget(self.btn_validate_script)
        self.progressBar = QtWidgets.QProgressBar(self.tab_scripts)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.progressBar.setFont(font)
        self.progressBar.setToolTip("")
        self.progressBar.setStatusTip("")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_5.addWidget(self.progressBar)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem1 = QtWidgets.QSpacerItem(138, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.lbl_time_estimate = QtWidgets.QLabel(self.tab_scripts)
        self.lbl_time_estimate.setObjectName("lbl_time_estimate")
        self.horizontalLayout_6.addWidget(self.lbl_time_estimate)
        spacerItem2 = QtWidgets.QSpacerItem(268, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.horizontalLayout_6.setStretch(2, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)
        self.tabWidget.addTab(self.tab_scripts, "")
        self.tab_probes = QtWidgets.QWidget()
        self.tab_probes.setObjectName("tab_probes")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_probes)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_plot_probe = QtWidgets.QPushButton(self.tab_probes)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_plot_probe.setFont(font)
        self.btn_plot_probe.setObjectName("btn_plot_probe")
        self.horizontalLayout_2.addWidget(self.btn_plot_probe)
        self.btn_load_probes = QtWidgets.QPushButton(self.tab_probes)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_load_probes.setFont(font)
        self.btn_load_probes.setObjectName("btn_load_probes")
        self.horizontalLayout_2.addWidget(self.btn_load_probes)
        self.chk_probe_plot = QtWidgets.QCheckBox(self.tab_probes)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.chk_probe_plot.setFont(font)
        self.chk_probe_plot.setObjectName("chk_probe_plot")
        self.horizontalLayout_2.addWidget(self.chk_probe_plot)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chk_probe_log = QtWidgets.QCheckBox(self.tab_probes)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.chk_probe_log.setFont(font)
        self.chk_probe_log.setObjectName("chk_probe_log")
        self.horizontalLayout.addWidget(self.chk_probe_log)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.tree_probes = QtWidgets.QTreeWidget(self.tab_probes)
        self.tree_probes.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_probes.sizePolicy().hasHeightForWidth())
        self.tree_probes.setSizePolicy(sizePolicy)
        self.tree_probes.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tree_probes.setHeaderHidden(False)
        self.tree_probes.setObjectName("tree_probes")
        self.tree_probes.header().setDefaultSectionSize(150)
        self.tree_probes.header().setHighlightSections(True)
        self.verticalLayout_5.addWidget(self.tree_probes)
        self.verticalLayout_7.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.tab_probes, "")
        self.tab_settings = QtWidgets.QWidget()
        self.tab_settings.setObjectName("tab_settings")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_settings)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.btn_load_instruments = QtWidgets.QPushButton(self.tab_settings)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_load_instruments.setFont(font)
        self.btn_load_instruments.setObjectName("btn_load_instruments")
        self.horizontalLayout_3.addWidget(self.btn_load_instruments)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.tree_settings = QtWidgets.QTreeWidget(self.tab_settings)
        self.tree_settings.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_settings.sizePolicy().hasHeightForWidth())
        self.tree_settings.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tree_settings.setFont(font)
        self.tree_settings.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tree_settings.setHeaderHidden(False)
        self.tree_settings.setObjectName("tree_settings")
        self.tree_settings.header().setDefaultSectionSize(200)
        self.tree_settings.header().setHighlightSections(True)
        self.verticalLayout_3.addWidget(self.tree_settings)
        self.verticalLayout_8.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tab_settings, "")
        self.tab_data = QtWidgets.QWidget()
        self.tab_data.setObjectName("tab_data")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.tab_data)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.btn_save_data = QtWidgets.QPushButton(self.tab_data)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_save_data.setFont(font)
        self.btn_save_data.setObjectName("btn_save_data")
        self.horizontalLayout_10.addWidget(self.btn_save_data)
        self.btn_delete_data = QtWidgets.QPushButton(self.tab_data)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_delete_data.setFont(font)
        self.btn_delete_data.setObjectName("btn_delete_data")
        self.horizontalLayout_10.addWidget(self.btn_delete_data)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.tree_dataset = QtWidgets.QTreeView(self.tab_data)
        self.tree_dataset.setDragEnabled(True)
        self.tree_dataset.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.tree_dataset.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.tree_dataset.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree_dataset.setUniformRowHeights(True)
        self.tree_dataset.setObjectName("tree_dataset")
        self.verticalLayout.addWidget(self.tree_dataset)
        self.horizontalLayout_12.addLayout(self.verticalLayout)
        self.horizontalLayout_13.addLayout(self.horizontalLayout_12)
        self.tabWidget.addTab(self.tab_data, "")
        self.verticalLayout_10.addWidget(self.tabWidget)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tabWidget_2.setFont(font)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.list_history = QtWidgets.QListView(self.tab)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.list_history.setFont(font)
        self.list_history.setAlternatingRowColors(True)
        self.list_history.setWordWrap(True)
        self.list_history.setObjectName("list_history")
        self.verticalLayout_9.addWidget(self.list_history)
        self.tabWidget_2.addTab(self.tab, "")
        self.tab_settings_2 = QtWidgets.QWidget()
        self.tab_settings_2.setObjectName("tab_settings_2")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.tab_settings_2)
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.tree_gui_settings = QtWidgets.QTreeView(self.tab_settings_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tree_gui_settings.setFont(font)
        self.tree_gui_settings.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.tree_gui_settings.setAlternatingRowColors(True)
        self.tree_gui_settings.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tree_gui_settings.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tree_gui_settings.setIndentation(0)
        self.tree_gui_settings.setUniformRowHeights(True)
        self.tree_gui_settings.setItemsExpandable(True)
        self.tree_gui_settings.setSortingEnabled(True)
        self.tree_gui_settings.setExpandsOnDoubleClick(True)
        self.tree_gui_settings.setObjectName("tree_gui_settings")
        self.tree_gui_settings.header().setDefaultSectionSize(200)
        self.tree_gui_settings.header().setSortIndicatorShown(True)
        self.verticalLayout_11.addWidget(self.tree_gui_settings)
        self.horizontalLayout_11.addLayout(self.verticalLayout_11)
        self.tabWidget_2.addTab(self.tab_settings_2, "")
        self.verticalLayout_10.addWidget(self.tabWidget_2)
        self.horizontalLayout_7.addLayout(self.verticalLayout_10)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.toolbar_space_1 = QtWidgets.QWidget(self.centralwidget)
        self.toolbar_space_1.setObjectName("toolbar_space_1")
        self.horizontalLayout_9.addWidget(self.toolbar_space_1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.plot_1 = QtWidgets.QWidget(self.centralwidget)
        self.plot_1.setObjectName("plot_1")
        self.horizontalLayout_16.addWidget(self.plot_1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.toolbar_space_2 = QtWidgets.QWidget(self.centralwidget)
        self.toolbar_space_2.setObjectName("toolbar_space_2")
        self.horizontalLayout_14.addWidget(self.toolbar_space_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.plot_2 = QtWidgets.QWidget(self.centralwidget)
        self.plot_2.setObjectName("plot_2")
        self.horizontalLayout_15.addWidget(self.plot_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_15)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 8)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 26)
        self.horizontalLayout_7.addLayout(self.verticalLayout_2)
        self.horizontalLayout_7.setStretch(0, 8)
        self.horizontalLayout_7.setStretch(1, 12)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1733, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setEnabled(True)
        self.menuFile.setAcceptDrops(True)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.btn_exit = QtWidgets.QAction(MainWindow)
        self.btn_exit.setObjectName("btn_exit")
        self.btn_load_gui = QtWidgets.QAction(MainWindow)
        self.btn_load_gui.setObjectName("btn_load_gui")
        self.btn_save_gui = QtWidgets.QAction(MainWindow)
        self.btn_save_gui.setObjectName("btn_save_gui")
        self.btn_about = QtWidgets.QAction(MainWindow)
        self.btn_about.setObjectName("btn_about")
        self.btn_test_2 = QtWidgets.QAction(MainWindow)
        self.btn_test_2.setObjectName("btn_test_2")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExport = QtWidgets.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionGo_to_pylabcontrol_GitHub_page = QtWidgets.QAction(MainWindow)
        self.actionGo_to_pylabcontrol_GitHub_page.setObjectName("actionGo_to_pylabcontrol_GitHub_page")
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.btn_save_gui)
        self.menuFile.addAction(self.btn_load_gui)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.btn_exit)
        self.menuHelp.addAction(self.btn_about)
        self.menuHelp.addAction(self.actionGo_to_pylabcontrol_GitHub_page)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Lukin Lab - B26 GUI"))
        self.btn_store_script_data.setText(_translate("MainWindow", "send to Datasets"))
        self.btn_load_scripts.setText(_translate("MainWindow", "import script"))
        self.chk_show_all.setText(_translate("MainWindow", "show all"))
        self.tree_scripts.headerItem().setText(0, _translate("MainWindow", "Parameter/Script                       "))
        self.tree_scripts.headerItem().setText(1, _translate("MainWindow", "Value"))
        self.tree_scripts.headerItem().setText(2, _translate("MainWindow", "show"))
        __sortingEnabled = self.tree_scripts.isSortingEnabled()
        self.tree_scripts.setSortingEnabled(False)
        self.tree_scripts.topLevelItem(0).setText(0, _translate("MainWindow", "New Item"))
        self.tree_scripts.topLevelItem(1).setText(0, _translate("MainWindow", "New Item"))
        self.tree_scripts.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "New Subitem"))
        self.tree_scripts.setSortingEnabled(__sortingEnabled)
        self.btn_start_script.setText(_translate("MainWindow", "start"))
        self.btn_stop_script.setText(_translate("MainWindow", "stop"))
        self.btn_skip_subscript.setText(_translate("MainWindow", "skip"))
        self.btn_validate_script.setText(_translate("MainWindow", "validate"))
        self.lbl_time_estimate.setText(_translate("MainWindow", "time remaining:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_scripts), _translate("MainWindow", "Scripts"))
        self.btn_plot_probe.setText(_translate("MainWindow", "plot probe"))
        self.btn_load_probes.setText(_translate("MainWindow", "load probe"))
        self.chk_probe_plot.setText(_translate("MainWindow", "plotting on"))
        self.chk_probe_log.setText(_translate("MainWindow", "logging on"))
        self.tree_probes.headerItem().setText(0, _translate("MainWindow", "Parameter"))
        self.tree_probes.headerItem().setText(1, _translate("MainWindow", "Value"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_probes), _translate("MainWindow", "Probes"))
        self.btn_load_instruments.setText(_translate("MainWindow", "import instrument"))
        self.tree_settings.headerItem().setText(0, _translate("MainWindow", "Instrument"))
        self.tree_settings.headerItem().setText(1, _translate("MainWindow", "Value"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_settings), _translate("MainWindow", "Instruments"))
        self.btn_save_data.setText(_translate("MainWindow", "save selected"))
        self.btn_delete_data.setText(_translate("MainWindow", "delete selected"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_data), _translate("MainWindow", "Datasets"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), _translate("MainWindow", "History"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_settings_2), _translate("MainWindow", "GUI Settings"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.btn_exit.setText(_translate("MainWindow", "Exit"))
        self.btn_load_gui.setText(_translate("MainWindow", "Load"))
        self.btn_save_gui.setText(_translate("MainWindow", "Save as"))
        self.btn_about.setText(_translate("MainWindow", "about"))
        self.btn_test_2.setText(_translate("MainWindow", "test"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionExport.setText(_translate("MainWindow", "Convert script or instrument .py files to .b26 files"))
        self.actionGo_to_pylabcontrol_GitHub_page.setText(_translate("MainWindow", "Go to pylabcontrol GitHub page"))

