#!/usr/bin/python3

import sqlite3
from datetime import date
from pathlib import Path

from pandas import read_sql_query

import Constants

class DBAccess:
	
	def __init__( self ):
		self.databaseFile = Constants.DBPATH
	
	def initialize( self ):
		# If there is no database in working directory create it
		if not self.databaseFile.exists():
			db = self.getDBConnection()
			print( "Database file created" )
			
			# Initialize Store table
			db.execute( '''CREATE TABLE STORES
				(STORENAME TEXT PRIMARY KEY NOT NULL );''' )
			print( "STORES table created" )
			
			# Initialize Item table
			db.execute( ''' CREATE TABLE ITEMS
				(
				NAME TEXT NOT NULL,
				BRAND TEXT NOT NULL,
				PRIMARY KEY ( NAME, BRAND )
				);
			''' )
			print( "ITEMS table created" )
			
			# Initialize Price table
			db.execute( ''' CREATE TABLE PRICES
				(
				LOGDATE DATE NOT NULL,
				PRICE FLOAT NOT NULL,
				QUANTITY FLOAT,
				QUANTITYTYPE TEXT,
				COUPONUSED BOOLEAN,
				ITEMNAME TEXT NOT NULL,
				ITEMBRAND TEXT NOT NULL,
				PRIMARY KEY ( LOGDATE, ITEMNAME )
				FOREIGN KEY ( ITEMNAME ) REFERENCES ITEMS( NAME ),
				FOREIGN KEY ( ITEMBRAND ) REFERENCES ITEMS( BRAND ) );
				''' )
			print( "PRICE table created" )
			
			# Initialize Coupon table
			db.execute( ''' CREATE TABLE COUPONS
			(
			EXPDATE DATE NOT NULL,
			DISCTYPE INT,
			DISCVALUE FLOAT,
			STORECARD BOOLEAN,
			COUPONTYPE TEXT,
			ITEMNAME TEXT NOT NULL,
			ITEMBRAND TEXT NOT NULL,
			PRIMARY KEY ( EXPDATE ),
			FOREIGN KEY ( ITEMNAME ) REFERENCES ITEMS( NAME )
			FOREIGN KEY ( ITEMBRAND ) REFERENCES ITEMS( BRAND )
			);''' )
			print( "COUPONS table created" )
			
			# Initialize Storetag table
			db.execute( ''' CREATE TABLE STORETAGS
				(
				TAG TEXT NOT NULL,
				STORENAME TEXT NOT NULL,
				PRIMARY KEY ( TAG ),
				FOREIGN KEY ( STORENAME ) REFERENCES STORES ( STORENAME )
				);''' )
			print( "STORETAGS table created" )
			
			# Initialize Itemtag table
			db.execute( ''' CREATE TABLE ITEMTAGS
				(
				TAG TEXT NOT NULL,
				ITEMNAME TEXT NOT NULL,
				PRIMARY KEY ( TAG ),
				FOREIGN KEY ( ITEMNAME ) REFERENCES ITEMS ( NAME )
				);''' )
			print( "ITEMTAGS table created" )
			
			self.closeDBConnection( db )
			print( "Database Initialized" )
		else:
			print( "Database present" )
	
	def getDBConnection( self ):
		return sqlite3.connect( self.databaseFile._str )
	
	def closeDBConnection( self, connection ):
		connection.close()
	
	def addStore( self, name ):
		# Add a store to db
		connection = self.getDBConnection()
		cursor = connection.cursor()
		
		try:
			cursor.execute( "INSERT INTO STORES VALUES ( \"{0}\" );".format( name ) )
			print( "ADDED STORE: {0}".format( name ) )
		except sqlite3.OperationalError:
			print( "Error adding store: {0}".format( name ) )
		except sqlite3.IntegrityError:
			pass
		finally:
			connection.commit()
			cursor.close()
			self.closeDBConnection( connection )
	
	def addItem( self, name, brand ):
		# Add Item to database
		connection = self.getDBConnection()
		cursor = connection.cursor()
		
		try:
			cursor.execute( "INSERT INTO ITEMS VALUES ( \"{0}\", \"{1}\" );".format( name, brand ) )
			print( "ADDED ITEM: [Brand] {0} | [Name] {1}".format( brand, name ) )
		except sqlite3.OperationalError:
			print( "Error adding item: [Brand] {0} | [Name] {1}".format( brand, name ) )
		except sqlite3.IntegrityError:
			pass
		finally:
			connection.commit()
			cursor.close()
			self.closeDBConnection( connection )
	
	def addPrice( self,
				  itemName,
				  itemBrand,
				  price = 0.00,
				  quantType = "Unit",
				  quantity = 1,
				  couponUsed = 0,
				  date = date.today() ):
		
		# Add item price to database
		connection = self.getDBConnection()
		cursor = connection.cursor()
		
		try:
			cursor.execute( '''
			INSERT INTO PRICES
			VALUES ( date( '{0}' ), {1}, {2}, \"{3}\", {4}, \"{5}\", \"{6}\" );
			'''.format( date, price, quantity, quantType, couponUsed, itemName, itemBrand ) )
			print( "ADDED ITEM PRICE: [Brand] {0} | [Name] {1}".format( itemBrand, itemName ) )
		except sqlite3.OperationalError:
			print( "Error adding price for item: [Brand] {0} | [Name] {1}".format( itemBrand, itemName ) )
		except sqlite3.IntegrityError:
			pass
		finally:
			connection.commit()
			cursor.close()
			self.closeDBConnection( connection )
	
	def addCoupon( self,
				   itemName,
				   itemBrand,
				   discType,
				   discValue,
				   couponType = "Manufacturer",
				   storeCard = 0,
				   expDate = str( date.today() )
				   ):
		
		# Add item price to database
		connection = self.getDBConnection()
		cursor = connection.cursor()
		
		try:
			cursor.execute( '''
			INSERT INTO COUPONS
			VALUES ( date( '{0}' ), {1}, {2}, {3}, '{4}', '{5}', '{6}' );
			'''.format( expDate, discType, discValue, storeCard, couponType, itemName, itemBrand ) )
			print( "ADDED COUPON: [Brand] {0} | [Name] {1}".format( itemBrand, itemName ) )
		except sqlite3.OperationalError:
			print( "Error adding coupon: [Brand] {0} | [Name] {1}".format( itemBrand, itemName ) )
		except sqlite3.IntegrityError:
			pass
		finally:
			connection.commit()
			cursor.close()
			self.closeDBConnection( connection )
	
	def addStoreTag( self, store, tag ):
		# Add Item to database
		connection = self.getDBConnection()
		cursor = connection.cursor()
		
		try:
			cursor.execute( "INSERT INTO STORETAGS VALUES ( \"{0}\", \"{1}\" );".format( tag, store ) )
			print( "ADDED STORE TAG: [Brand] {0} | [Name] {1}".format( store, tag ) )
		except sqlite3.OperationalError:
			print( "Error adding tag: [Brand] {0} | [Name] {1}".format( store, tag ) )
		except sqlite3.IntegrityError:
			pass
		finally:
			connection.commit()
			cursor.close()
			self.closeDBConnection( connection )
	
	def addItemTag( self, item, tag ):
		# Add Item to database
		connection = self.getDBConnection()
		cursor = connection.cursor()
		
		try:
			cursor.execute( "INSERT INTO ITEMTAGS VALUES ( \"{0}\", \"{1}\" );".format( tag, item ) )
			print( "ADDED ITEM TAG: [Brand] {0} | [Name] {1}".format( item, tag ) )
		except sqlite3.OperationalError:
			print( "Error adding tag: [Brand] {0} | [Name] {1}".format( item, tag ) )
		except sqlite3.IntegrityError:
			pass
		finally:
			connection.commit()
			cursor.close()
			self.closeDBConnection( connection )
	
	def searchItem( self, itemName, itemBrand ):
		connection = self.getDBConnection()
		cursor = connection.cursor()
		
		cursor.close()
		self.closeDBConnection()
	
	def __str__( self ):
		connection = self.getDBConnection()
		tables = ("STORES", "ITEMS", "PRICES", "COUPONS", "STORETAGS", "ITEMTAGS")
		output = ""
		for x in tables:
			output += "\nTable: " + x + "\n"
			output += str( read_sql_query( "SELECT * FROM {0}".format( x ), connection ) ) + "\n"
		return output

def test():
	test = DBAccess()
	test.databaseFile = Path( "TESTDB.db" )
	test.initialize()
	test.addStore( "Winco" )
	test.addItem( "banana", "Winco" )
	test.addPrice( "banana", "Winco", 10, date = "2018-05-12" )
	test.addStoreTag( "Winco", "cheap" )
	test.addItemTag( "banana", "Potassium" )
	test.addCoupon( 'banana', 'winco', 0, 15 )
	print( test )

if __name__ == '__main__':
	db = DBAccess()
	db.initialize()
	print( db )
