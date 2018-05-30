#!/usr/bin/python3

import sys
from datetime import date

import matplotlib.pyplot as pyplot
import pandas as pd
from PyQt5.QtWidgets import (
	QAction, QApplication, QCheckBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenu,
	QMessageBox, QPushButton, QVBoxLayout, QWidget, qApp
	)

import Constants
import DBAccess

class Grocer( QMainWindow ):
	def __init__( self ):
		super().__init__()
		
		self.initUI()
	
	def initUI( self ):
		# -------
		# GENERAL
		# -------
		
		# Set Window attributes
		self.setGeometry( 300, 300, Constants.INITIALWIDTH, Constants.INITIALHEIGHT )  # Define initial size
		self.setWindowTitle( "Grocer" )
		self.status = self.statusBar()
		
		# Prep
		self.initDB()
		
		# Defaults for form
		self.lastDate = str( date.today() )
		self.itemBrand = ""
		self.storeName = ""
		
		# -------
		# MENUBAR
		# -------
		menu = self.menuBar()
		self.setMenuBar( menu )
		
		# Define menus
		menuFile = QMenu( "File", self )
		menuAdd = QMenu( "Add", self )
		menuData = QMenu( "Data", self )
		
		# Add menus to menubar
		menu.addMenu( menuFile )
		menu.addMenu( menuAdd )
		menu.addMenu( menuData )
		
		# ---------
		# FILE MENU
		# ---------
		
		# Define actions
		fileLoadDB = QAction( "Load Database", self )
		fileExit = QAction( "Exit", self )
		
		# Statusbar tips
		fileLoadDB.setStatusTip( "Load database" )
		fileExit.setStatusTip( "Exit program" )
		
		# Shortcuts
		fileLoadDB.setShortcut( 'Ctrl+L' )
		fileExit.setShortcut( 'Ctrl+Q' )
		
		# Triggers
		fileLoadDB.triggered.connect( self.initDB )
		fileExit.triggered.connect( qApp.quit )
		
		# Add to File menu
		menuFile.addAction( fileLoadDB )
		menuFile.addAction( fileExit )
		
		# ---------
		# ADD MENU
		# ---------
		
		# Define actions
		addAddItem = QAction( "Add Item", self )
		addAddCoupon = QAction( "Add Coupon", self )
		
		addAddItem.setShortcut( "Ctrl+I" )
		
		# Statusbar tips
		addAddItem.setStatusTip( "Add an item to database" )
		addAddCoupon.setStatusTip( "Add a coupon to database" )
		
		# Add to Add menu
		menuAdd.addAction( addAddItem )
		menuAdd.addAction( addAddCoupon )
		
		# Triggers
		addAddItem.triggered.connect( self.addItemScreen )
		addAddCoupon.triggered.connect( self.addCouponScreen )
		
		# -----------
		# DATA MENU
		# -----------
		
		# Define actions
		summaryItems = QAction( "Summary of Data", self )
		summaryItems.setStatusTip( "Search all items in database for a specific item" )
		summaryItems.triggered.connect( self.summaryScreen )
		
		chartMenu = QMenu( "Charts", self )
		
		chartMostValue = QAction( "Highest Value Per Unit", self )
		chartMostValue.setStatusTip( "Cheapest item per unit gained (price/quantity)" )
		chartMostValue.triggered.connect( self.showMostValue )
		chartMenu.addAction( chartMostValue )
		
		chartMostSale = QAction( "Most Recorded Items", self )
		chartMostSale.setStatusTip( "Top 3 items most seen in all ads" )
		chartMostSale.triggered.connect( self.showMostOnSale )
		chartMenu.addAction( chartMostSale )
		
		chartMostDiverse = QAction( "Most diverse Store", self )
		chartMostDiverse.setStatusTip( "Store with the highest amount of unique items for sale" )
		chartMostDiverse.triggered.connect( self.showMostDiverseStore )
		chartMenu.addAction( chartMostDiverse )
		
		menuData.addAction( summaryItems )
		menuData.addMenu( chartMenu )
		
		self.show()
	
	def initDB( self ):
		db = DBAccess.DBAccess()
		db.initialize()
		self.status.showMessage( "Database initialized" )
		self.setCentralText( "Use menu to add/search items to database" )
	
	def setCentralText( self, text ):
		widget = QWidget()
		self.setCentralWidget( widget )
		centralText = QLabel( text )
		hbox = QHBoxLayout()
		hbox.addStretch( 1 )
		hbox.addWidget( centralText )
		hbox.addStretch( 1 )
		
		vbox = QVBoxLayout()
		vbox.addStretch( 1 )
		vbox.addLayout( hbox )
		vbox.addStretch( 1 )
		widget.setLayout( vbox )
	
	def setStatus( self, message ):
		self.status.showMessage( message )
	
	def clearStatus( self ):
		self.status.clearMessage()
	
	def addItemScreen( self ):
		widget = QWidget()
		self.setCentralWidget( widget )
		
		nameLine = QHBoxLayout()
		self.itemNameEdit = QLineEdit()
		self.itemNameEdit.setPlaceholderText( "e.g. Laundry detergent, mango, chicken, etc" )
		nameLine.addWidget( QLabel( "Item name:" ) )
		nameLine.addWidget( self.itemNameEdit )
		
		randLine = QHBoxLayout()
		self.itemBrandEdit = QLineEdit()
		self.itemBrandEdit.setText( self.itemBrand )
		randLine.addWidget( QLabel( "Item brand:" ) )
		randLine.addWidget( self.itemBrandEdit )
		
		storeLine = QHBoxLayout()
		self.storeNameEdit = QLineEdit()
		self.storeNameEdit.setText( self.storeName )
		storeLine.addWidget( QLabel( "Store name:" ) )
		storeLine.addWidget( self.storeNameEdit )
		
		buttonLine = QHBoxLayout()
		nextButton = QPushButton( "Next" )
		nextButton.setDefault( True )
		cancelButton = QPushButton( "Cancel" )
		buttonLine.addStretch( 1 )
		buttonLine.addWidget( nextButton )
		buttonLine.addWidget( cancelButton )
		
		nextButton.clicked.connect( self.addItemButtons )
		cancelButton.clicked.connect( self.addItemButtons )
		
		screen = QVBoxLayout()
		screen.addLayout( nameLine )
		screen.addLayout( randLine )
		screen.addLayout( storeLine )
		screen.addLayout( buttonLine )
		widget.setLayout( screen )
	
	def addItemInfoScreen( self ):
		widget = QWidget()
		self.setCentralWidget( widget )
		self.clearStatus()
		
		priceLine = QHBoxLayout()
		self.itemPrice = QLineEdit()
		self.itemPrice.setPlaceholderText( "e.g. 11.99" )
		priceLine.addWidget( QLabel( "Price: $" ) )
		priceLine.addWidget( self.itemPrice )
		
		quantityLine = QHBoxLayout()
		self.itemQuantity = QLineEdit()
		self.itemQType = QLineEdit()
		self.itemQuantity.setText( "1" )
		self.itemQType.setText( "lb" )
		quantityLine.addWidget( QLabel( "Quantity Type:" ) )
		quantityLine.addWidget( self.itemQType )
		quantityLine.addWidget( QLabel( "Quantity:" ) )
		quantityLine.addWidget( self.itemQuantity )
		
		miscLine = QHBoxLayout()
		self.itemCouponUsed = QCheckBox()
		self.itemDate = QLineEdit()
		self.itemDate.setText( self.lastDate )
		miscLine.addWidget( QLabel( "Date:" ) )
		miscLine.addWidget( self.itemDate )
		miscLine.addStretch( 1 )
		miscLine.addWidget( QLabel( "Coupon used?" ) )
		miscLine.addWidget( self.itemCouponUsed )
		
		buttonLine = QHBoxLayout()
		addButton = QPushButton( "Add" )
		addButton.setDefault( True )
		cancelButton = QPushButton( "Cancel" )
		buttonLine.addStretch( 1 )
		buttonLine.addWidget( addButton )
		buttonLine.addWidget( cancelButton )
		addButton.clicked.connect( self.addItemButtons )
		cancelButton.clicked.connect( self.addItemButtons )
		
		screen = QVBoxLayout()
		screen.addLayout( priceLine )
		screen.addLayout( quantityLine )
		screen.addLayout( miscLine )
		screen.addLayout( buttonLine )
		
		widget.setLayout( screen )
	
	def addItemButtons( self ):
		sender = self.sender()
		if (sender.text() == "Next"):
			if (self.itemNameEdit.text() == "" or self.itemBrandEdit.text() == "" or self.storeNameEdit.text() == ""):
				self.displayMessage( "Fill out all forms", "Error" )
			else:
				self.itemName = self.itemNameEdit.text()
				self.itemBrand = self.itemBrandEdit.text()
				self.storeName = self.storeNameEdit.text()
				self.addItemInfoScreen()
		elif (sender.text() == "Add"):
			if (self.itemPrice.text() == "" or self.itemQuantity.text() == "" or \
					self.itemQType.text() == "" or self.itemDate.text() == ""):
				self.displayMessage( "Fill out all forms", "Error" )
			else:
				try:
					db = DBAccess.DBAccess()
					db.addStore( self.storeName )
					db.addItem( self.itemName, self.itemBrand )
					db.addPrice( self.itemName, self.itemBrand, float( self.itemPrice.text() ),
								 self.itemQType.text(), float( self.itemQuantity.text() ),
								 int( self.itemCouponUsed.isChecked() ), self.itemDate.text() )
					self.lastDate = self.itemDate.text()
					self.setStatus( "Item Added Successfully" )
				except:
					self.displayMessage( str( sys.exc_info()[ 0 ] ), "Database Error" )
				finally:
					self.addItemScreen()
		else:
			self.status.clearMessage()
			self.setCentralText( "Check menu for options" )
	
	def displayMessage( self, message, title ):
		msg = QMessageBox()
		msg.setText( message )
		msg.setWindowTitle( title )
		msg.setStandardButtons( QMessageBox.Ok )
		return msg.exec_()
	
	def addCouponScreen( self ):
		print( "Adding Coupon" )
		self.setCentralText( "TODO: Add Coupon functionality" )
	
	def showMostValue( self ):
		db = DBAccess.DBAccess()
		mostValue = pd.read_sql( '''SELECT DISTINCT ITEMNAME AS ITEM, (PRICES.PRICE/PRICES.QUANTITY) AS VAL
		FROM PRICES
									ORDER BY (PRICES.PRICE/PRICES.QUANTITY)
									LIMIT 5;
									''', db.getDBConnection() )
		pyplot.plot( mostValue[ 'ITEM' ], mostValue[ 'VAL' ] )
		pyplot.ylabel( "Cost per unit in $" )
		pyplot.xlabel( "Item Name" )
		pyplot.show()
	
	def showMostOnSale( self ):
		db = DBAccess.DBAccess()
		mostRecorded = pd.read_sql( '''SELECT ITEMNAME, COUNT( ITEMNAME) AS CNT FROM PRICES
										GROUP BY ITEMNAME ORDER BY COUNT( * ) DESC
										LIMIT 3;
										''', db.getDBConnection() )
		pyplot.plot( mostRecorded[ 'ITEMNAME' ], mostRecorded[ 'CNT' ] )
		pyplot.xlabel( "Item Name" )
		pyplot.ylabel( "# of ads item was found in" )
		pyplot.show()
	
	def showMostDiverseStore( self ):
		db = DBAccess.DBAccess()
		mostDiverseStore = pd.read_sql( '''
										SELECT BRAND, COUNT( * ) AS C FROM ( STORES INNER jOIN ITEMS ON
										BRAND=STORENAME )
										GROUP BY BRAND
										ORDER BY COUNT( * ) DESC
										limit 4;
										''', db.getDBConnection() )
		pyplot.plot( mostDiverseStore[ 'BRAND' ], mostDiverseStore[ 'C' ] )
		pyplot.ylabel( "# of unique items sold by store" )
		pyplot.xlabel( "Store Name" )
		pyplot.show()
	
	def summaryScreen( self ):
		widget = QWidget()
		self.setCentralWidget( widget )
		
		db = DBAccess.DBAccess()
		numItems = pd.read_sql( "SELECT DISTINCT ITEMNAME FROM PRICES;", db.getDBConnection() )
		numPrices = pd.read_sql( "SELECT ITEMNAME FROM PRICES;", db.getDBConnection() )
		mostValue = pd.read_sql( '''SELECT * FROM 'PRICES'
									ORDER BY (PRICES.PRICE/PRICES.QUANTITY)
									limit 1;''', db.getDBConnection() )
		mostRecorded = pd.read_sql( '''SELECT ITEMNAME, COUNT( ITEMNAME) AS CNT FROM PRICES
										GROUP BY ITEMNAME ORDER BY COUNT( * ) DESC
										LIMIT 3;
										''', db.getDBConnection() )
		mostDiverseStore = pd.read_sql( '''
										SELECT BRAND, COUNT( * ) AS C FROM ( STORES INNER jOIN ITEMS ON
										BRAND=STORENAME )
										GROUP BY BRAND
										ORDER BY COUNT( * ) DESC;
										''', db.getDBConnection() )
		
		summary = ""
		summary += "Number of Unique Items in DB: " + str( numItems[ 'ITEMNAME' ].count() )
		summary += "\nNumber of Prices Logged: " + str( numPrices[ 'ITEMNAME' ].count() )
		summary += "\nMost value item ( Price/Quantity ): " + str( mostValue[ 'ITEMNAME' ][ 0 ] )
		summary += "\nItem most on sale: " + str( mostRecorded[ 'ITEMNAME' ][ 0 ] ) + " (x" + \
				   str( mostRecorded[ 'CNT' ][ 0 ] ) + ")"
		summary += "\nMost diverse in-house products: " + str( mostDiverseStore[ 'BRAND' ][ 0 ] )
		
		summaryLine = QHBoxLayout()
		summaryLine.addStretch( 1 )
		summaryLine.addWidget( QLabel( summary ) )
		summaryLine.addStretch( 1 )
		
		screen = QVBoxLayout()
		screen.addStretch( 1 )
		screen.addLayout( summaryLine )
		screen.addStretch( 1 )
		
		widget.setLayout( screen )

if __name__ == "__main__":
	app = QApplication( sys.argv )
	grocer = Grocer()
	sys.exit( app.exec_() )
