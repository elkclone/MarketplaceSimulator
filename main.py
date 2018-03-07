import os
import sys
import curses
import time
import random

from marketplace import Marketplace, Pair, Order, OrderType
from agent import Agent

# Parameters


def simulation(stdscr):
	market = Marketplace()
	pair = Pair(market, 'BTC', 'USD', fees=0)

	agents = []
	for i in range(4):
		agent = Agent()
		agent.selectPair(pair)
		agent.deposit('USD', 5000)
		agent.deposit('BTC', 0.2)
		#agent.placeOrder(OrderType.BUY, 11258 + random.randint(0, 10), (10 + random.randint(0, 10)) / 10000)
		#agent.placeOrder(OrderType.SELL, 11258 + random.randint(0, 10), (10 + random.randint(0, 10)) / 10000)
		agents.append(agent)
		
	loop = True
	timer = time.time() - 1.
	timerUpdate = time.time()
	elapsedTime = 0

	stdscr.clear()
	stdscr.refresh()
	curses.start_color()
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

	while loop:
		#stdscr.clear()
		height, width = stdscr.getmaxyx()
		if time.time() - timer > 0.5:
			for agent in agents:
				priceSell = 11258 + random.randint(0, 10)
				amountSell = min(random.randint(1, 500) / 10000, agent.getWallet()['BTC'])
				priceBuy = 11258 + random.randint(0, 10)
				amountBuy = min(random.randint(1, 500) / 10000, agent.getWallet()['USD'] / priceBuy)
				
				if amountBuy > 0:
					agent.placeOrder(OrderType.BUY, priceBuy, amountBuy)
				if amountSell > 0:
					agent.placeOrder(OrderType.SELL, priceSell, amountSell)

			elapsedTime += time.time() - timer
			market.update()
			timer = time.time()

			timeString = "Elapsed time : {:3.0f}s".format(elapsedTime)
			stdscr.addstr(height - 2, width - len(timeString) - 2, timeString)
		
			buys, sells = pair.getOrders()
			buys = sorted(buys, key=lambda x: -x.getPrice())
			sells = sorted(sells, key=lambda x: -x.getPrice())
			history = pair.getHistory()

			header = "BUY ORDERS\tPRICE\tAMOUNT\tDATE"
			stdscr.addstr(0, 0, header, curses.color_pair(3))
			for k in range(1,len(buys)+1):
				buy = buys[-k]
				if k > height // 2:
					break

				price = "{:12f}".format(buy.getPrice())
				amount = "{:12f}".format(buy.getAmount())
				date = buy.getDate().strftime("%Y-%m-%d %H:%M:%S")
				row = "BUY\t" + price + "\t" + amount + "\t" + date
				stdscr.addstr(k, 0, row)

			stdscr.addstr(0, width // 3, "SELL ORDERS", curses.color_pair(3))
			for k in range(1,len(sells)+1):
				sell = sells[-k]
				if k > height // 2:
					break

				price = "{:12f}".format(sell.getPrice())
				amount = "{:12f}".format(sell.getAmount())
				date = buy.getDate().strftime("%Y-%m-%d %H:%M:%S")
				row = "SELL\t" + price + "\t" + amount + "\t" + date
				stdscr.addstr(k, width // 3, row)

			stdscr.addstr(0, 2 * width // 3, "DATA", curses.color_pair(3))
			stdscr.addstr(1, 2 * width // 3, "Volume : {:05.2f}".format(pair.getData("volume")))
			stdscr.addstr(2, 2 * width // 3, "Last : {:05.2f}".format(pair.getData("last")))
			stdscr.addstr(3, 2 * width // 3, "High : {:05.2f}".format(pair.getData("high")))
			stdscr.addstr(4, 2 * width // 3, "Low : {:05.2f}".format(pair.getData("low")))

			stdscr.addstr(height // 2 + 1, 0, "HISTORY", curses.color_pair(3))
			for k in range(1,len(history)+1):
				order = history[-k]
				if k + 1 >= height // 2:
					break

				price = "{:12f}".format(order.getPrice())
				amount = "{:12f}".format(order.getAmount())
				date = order.getDate().strftime("%Y-%m-%d %H:%M:%S")
				row = "{:5s}\t".format(order.getOrderType().name) + price + "\t" + amount + "\t" + date
				colorPair = curses.color_pair(1)
				if order.getOrderType().name == "SELL":
					colorPair = curses.color_pair(2)
				stdscr.addstr(height // 2 + k + 1, 0, row, colorPair)

			stdscr.addstr(height // 2 + 1, width // 2, "AGENTS", curses.color_pair(3))
			for k, agent in enumerate(agents):
				pairAVal = "{:14.10f}".format(agent.getWallet()['BTC'])
				pairBVal = "{:8.2f}".format(agent.getWallet()['USD'])
				row = str(agent) +  "\t" + pairAVal + "\t" + pairBVal
				stdscr.addstr(height // 2 + k + 2, width // 2, row)

			
			stdscr.refresh()
		#k = stdscr.getch()

if __name__ == '__main__':
	curses.wrapper(simulation)
