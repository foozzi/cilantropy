"""
.. module:: dist_worker
   :platform: Unix, Windows
   :synopsis: Cilantropy worker for working with packages.

:mod:`dist_worker` -- dist_worker Cilantropy worker for working with packages
==================================================================
"""

import subprocess
import sys


def main_worker(cmd):
	""" Main worker for run subproccess and 
	return result or error

	:param cmd: full command for run	
	:return: 2 parameters text, bool with 
	result and status error (True, False) 
	"""
	try:
		cmd_response = subprocess.run(
			cmd,
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			check=True,
		)
	except subprocess.CalledProcessError as e:
		return "The pip command did not succeed: {stderr}".format(
				stderr=e.stderr.decode("utf-8")
			), True

	return cmd_response.stdout.decode("utf-8").strip(), False



class Updater:
	""" class constructor for Updater

	:param dist_name: distribution name
	"""	
	
	def __init__(self, dist_name):
		self.pip3_cmd = "pip3"
		self.pip_upgrade = "--upgrade"
		self.pip_install = "install"
		self.pip_user_arg = "--user"

		self.dist_name = dist_name


	def upgrade(self):
		""" Just build command string for update package

		:return: Return result `main_worker`
		"""
		cmd = "{pip3_cmd} {pip_install} {dist_name} {pip_upgrade}".format(
			pip3_cmd=self.pip3_cmd, pip_install=self.pip_install,
			dist_name=self.dist_name, pip_upgrade=self.pip_upgrade
		)		

		return main_worker(cmd)



