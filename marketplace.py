import os
import sys
from enum import Enum
import datetime

class OrderType(Enum):
	BUY = 0,
	SELL = 1

class Marketplace():

	def __init__(self):
		self.name = "Marketplace"
		self.pairs = []

	def addPair(self, pair):
		self.pairs.append(pair)

	def update(self):
		for pair in self.pairs:
			pair.update()

class Pair():
	
	def __init__(self, market, pairA, pairB, fees=0):
		self.pairA = pairA
		self.pairB = pairB
		self.fees = fees
		self.buyOrders = []
		self.sellOrders = []
		self.history = []
		market.addPair(self)

	def buy(self, agent, price, amount):
		order = Order(agent, price, amount, orderType=OrderType.BUY)
		self.buyOrders.append(order)

	def sell(self, agent, price, amount):
		order = Order(agent, price, amount, orderType=OrderType.SELL)
		self.sellOrders.append(order)

	def getOrders(self):
		return self.buyOrders, self.sellOrders

	def getHistory(self):
		return self.history

	def update(self):
		for buy in self.buyOrders:
			for sell in self.sellOrders:
				if not(buy in self.buyOrders):
					continue
				# We find sell and buy orders at same price
				if sell.getPrice() == buy.getPrice():
					price = sell.getPrice()
					if sell.getAmount() > buy.getAmount():
						deltaAmount = sell.getAmount() - buy.getAmount()
						self.buyOrders.remove(buy)
						self.history.append(buy)
						self.history.append(Order(sell.getAgent(), price, sell.getAmount() - deltaAmount, orderType=OrderType.SELL))
						sell.setAmount(deltaAmount)

					elif sell.getAmount() < buy.getAmount():
						deltaAmount = buy.getAmount() - sell.getAmount()
						self.sellOrders.remove(sell)
						self.history.append(buy)
						self.history.append(Order(buy.getAgent(), price, buy.getAmount() - deltaAmount, orderType=OrderType.BUY))
						buy.setAmount(deltaAmount)

					else:
						self.sellOrders.remove(sell)
						self.buyOrders.remove(buy)
						self.history.append(sell)
						self.history.append(buy)

					amountOrder = min(sell.getAmount(), buy.getAmount())
					sell.getAgent().deposit(self.pairB, amountOrder * price)
					sell.getAgent().withdraw(self.pairA, amountOrder)
					buy.getAgent().deposit(self.pairA, amountOrder)
					buy.getAgent().withdraw(self.pairB, amountOrder * price)
						

	def __str__(self):
		res = "BUY Orders :"
		for buyOrder in self.buyOrders:
			res += "\n" + str(buyOrder)
		return res

	def getData(self, name):
		if name == "volume":
			data = sum([ o.getAmount() for o in self.history if o.getOrderType() == OrderType.BUY ])
		elif name == "low":
			data = min([ o.getPrice() for o in self.history if o.getOrderType() == OrderType.BUY ])
		elif name == "high":
			data = max([ o.getPrice() for o in self.history if o.getOrderType() == OrderType.BUY ])
		elif name == "last":
			if len(self.history) == 0:
				data = 0
			else:
				data = self.history[-1].getPrice()
		return data

class Order():
	
	def __init__(self, agent, price, amount, orderType=OrderType.BUY):
		self.agent = agent
		self.price = price
		self.amount = amount
		self.orderType = orderType
		self.date = datetime.datetime.now()

	def __str__(self):
		return self.orderType.name + " Order : {:2.4f} at {:2.4f}.".format(self.amount, self.price)

	def getDate(self):
		return self.date

	def getAgent(self):
		return self.agent

	def getOrderType(self):
		return self.orderType

	def getPrice(self):
		return self.price

	def setAmount(self, q):
		self.amount = q

	def getAmount(self):
		return self.amount
		
