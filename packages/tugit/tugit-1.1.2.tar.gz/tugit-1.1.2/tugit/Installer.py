import os
import subprocess
import sys

class Installer:
	def __init__(self):
		reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
		self._installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

	@property
	def installed_packages(self):
		return self._installed_packages.copy()

	def is_installed(self, package):
		return package in self._installed_packages

	def tug(self, package, url, ignore_if_installed=True, echo=1):
		if self.is_installed(package=package) and ignore_if_installed:
			return False
		else:
			if echo: print(f'bringing {package} from {url} ', end='')
			result = os.system(f'pip install git+{url}')
			if result==0:
				if echo: print('successful!')
				self._installed_packages.append(package)
			else:
				if echo: print('failed!')
				raise RuntimeError(f'tugit Installer could not install {package} from {url}')
			return True


