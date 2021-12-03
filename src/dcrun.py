#coding: utf-8

class DCRun(object):
	def __init__(self):
		self.status = "invalid"
		self.target_ips = set([])

	def add_valid_room_ip(self, ip):
		self.target_ips.add(ip)

	def delete_room_ip(self, ip):
		try:
			self.target_ips.remove(ip)
		finally:
			pass

	def view_ips(self):
		


	