# coding: utf-8

import src.util
import uuid
import threading

ONLINE_CHECK = 300 #5分钟没有动作就会踢掉客户端

class MemCache(object):
	def __init__(self):
		self.onlineUsers = {}
		self.onlineUsersByToken = {}
		self.locker = threading.RLock()
		threading.Timer(5, self.user_checker).start()

		self.isDown = False

	def shutdown(self):
		print("Shutting Cache Down.")
		self.isDown = True

	def on_user_login(self, uid):
		token = None

		self.locker.acquire()
		try:
			if uid in self.onlineUsers:
				ou = self.onlineUsers[uid]
				ou["loginTime"] = util.inow()
				token = ou["token"]
			else:
				ou = {
					"loginTime": util.inow(),
					"token": str(uuid.uuid4()).replace('-','')
				}

				self.onlineUsers[uid] = ou
				self.onlineUsersByToken[ou['token']] = uid
		finally:
			self.locker.release()

		return ou["token"]

	def get_user(self, token):
		self.locker.acquire()

		uid = None
		try:
			if token in self.onlineUsersByToken:
				uid = self.onlineUsersByToken[token]
			
		finally:
			self.locker.release()

		return uid

	def user_checker(self):
		self.locker.acquire()
		try:
			for uid, uinfo in self.onlineUsers.items():
				if util.inow() - uinfo['loginTime'] > ONLINE_CHECK:
					self.onlineUsers[uid] = None
		finally:
			self.locker.release()

		if not self.isDown:
			threading.Timer(5, self.user_checker).start()