import os
import sys
from marketplace import OrderType

class Agent():



	def __init__(self):
		self.name = "Agent"
		self.currentPair = None
		self.wallet = { 'USD': 0,
				'BTC': 0 }

	def __str__(self):
		return self.name

	def selectPair(self, pair):
		self.currentPair = pair

	def placeOrder(self, orderType, price, amount):
		if self.currentPair == None:
			raise ValueError("The pair is not selected.")
		if orderType == OrderType.BUY:
			self.currentPair.buy(self, price, amount)
		elif orderType == OrderType.SELL:
			self.currentPair.sell(self, price, amount)
	
	def deposit(self, currency, amount):
		self.wallet[currency] += amount

	def withdraw(self, currency, amount):
		self.wallet[currency] -= amount

	def getWallet(self):
		return self.wallet
