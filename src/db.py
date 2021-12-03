# coding: utf-8
import simplejson as json
import hashlib
import codecs

#这里可以考虑客户端加盐，不过意义不大
MD5_SALT = ""
SUPER_USER = {
	"mario": "b32d73e56ec99bc5ec8f83871cde708a",
	#"safin": [TODO_YOUR_PWD_MD5] 
	
	#Md5 use method blow
	#md5(pwd)
}


def md5(s):	
	m = hashlib.md5()
	m.update(s)
	return m.hexdigest()

class LocalDatabase(object):
	def __init__(self):
		with codecs.open("./.local", "r") as f:
			data = f.read() or "{}"

			#print ("Check Data -> ", str(data))
			self.db = json.loads(str(data))

		if not "users" in self.db:
			self.db['users'] = {}

		if not "dcrun" in self.db:
			self.db['dcrun'] = []

	def save(self):
		with codecs.open("./.local", "w") as f:
			f.write(json.dumps(self.db, sort_keys=True, ensure_ascii=False, indent=4))

	def raw(self):
		return self.db

	def add_candidate(self, uid, pwd):
		self.db['users'][uid] = {
			"user": uid,
			"password": pwd,
			"valid": False
		}

		self.save()
		return True

	def is_user_exists(self, uid):
		if not uid:
			return False

		if self.is_super_user(uid):
			return True

		if not uid in self.db['users']: 
			return False

		return self.db['users'][uid] is not None

	def is_user_valid(self, uid, pwd):
		if not uid or not pwd:
			return False

		if self.is_super_user_valid(uid, pwd):
			return True

		if not uid in self.db['users']: 
			return False

		if not self.db['users'][uid]['password'] == pwd:
			return False

		return self.db['users'][uid]['valid']

	def is_super_user(self, uid):
		if not uid:
			return False

		if not uid in SUPER_USER:
			return False

		return True

	def is_super_user_valid(self, uid, pwd):
		if not uid or not pwd:
			return False
		if not uid in SUPER_USER:
			return False
		
		return SUPER_USER[uid] == pwd

	def handle_candidate(self, uid):
		if not self.is_user_exists(uid):
			return False

		user = self.db['users'][uid]
		if user['valid']:
			return False

		user['valid'] = True
		self.save()
		return True

	def delete_user(self, uid):
		if self.is_super_user(uid):
			return False

		if not uid in self.db['users']: 
			return False

		self.db['users'][uid] = None
		
		self.save()
		return True

	def new_dc_run(self):
		pass

	def update_dc_run_info(self, ip, match_player_cnt, online_player_cnt):
		pass