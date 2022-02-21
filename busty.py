#!/usr/bin/env python3

# Busty Py Directory Buster
# Because, surely, we needed another one
# "Rate" is just a control, not the actual speed
# Maybe in the future I'll add a worker pool if I need it to go faster.

import requests
import argparse
from time import sleep

class Busty:
	def __init__(self, args):
		self.args = args
	
	def run(self):
		# Track length of line outputs so they can be cleared properly
		cLen, pLen = 0, 0
		
		# Append '/' to the URL if it's not there (port too)
		if self.args.url[-1] == '/':
			self.args.url[-1] = ':'
			self.args.url += self.args.port+'/'
		else:
			self.args.url += ':'+self.args.port+'/'
		
		# Prepend 'http://' to the URL if it's not there
		if 'http' not in self.args.url: self.args.url = 'http://'+self.args.url
		
		# Define some colors
		c = {"teal":"\x1b[36m", "red":"\x1b[31m", "green":"\x1b[32m", "amber":"\x1b[33m", "error":"\x1b[101;41m", "reset":"\033[0m"}
		
		# Print the banner and details of run
		print(f"{c['red']}//------------------------------------------\\\\")
		print(f" >> {c['teal']}Busty Py, Yet Another Directory Buster{c['red']} <<")
		print(f"\\\\------------------------------------------//{c['reset']}")
		print(f"{c['red']}// {c['teal']}Host:{c['reset']}", self.args.url)
		# For request rates >= 1 per second
		if self.args.rate >= 1:
			print(f"{c['red']}|  {c['teal']}Rate:{c['reset']}", self.args.rate, "requests/sec")
		# For request rates > 1 per second
		else:
			print(f"{c['red']}|  {c['teal']}Rate:{c['reset']}", "{:.2f}".format(1/self.args.rate), "seconds/request")
		print(f"{c['red']}\\\\ {c['teal']}Wordlist:{c['reset']}", self.args.wordlist)
		
		# Run the test
		with open(self.args.wordlist, encoding='latin-1') as wordlist:
			for Line in wordlist:
				cLen = len(Line.strip())
				print(f" [ ] Checking:  {Line.strip()}"+" "*(pLen-cLen), end='\r')
				pLen = cLen # Difference between this line length, and the previous
				
				# Use try/except to "gracefully" excape from connection errors
				try: response = requests.get(self.args.url+Line.strip(), headers={'user-agent':'custom'}, allow_redirects=False, verify=False)
				except: print(f"\n{c['error']} << Connection Error >> \033[0m\n Ckeck the URL and port?\n Is the host still up?\n"); exit()
				status = response.status_code
				# 200-299 codes are a good hit
				if status >= 200 and status < 300:
					print(f" {c['green']}[+] {status} Found: {Line.strip()}{c['reset']}"+" "*(pLen-cLen+3))
				# 300-399 codes are a redirects
				elif status >= 300 and status < 400:
					print(f" {c['amber']}[!] {status} Redir: {Line.strip()} -> {response.headers['location']}{c['reset']}"+" "*(pLen-cLen+3))
				sleep(1/self.args.rate) # 
		print()
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Busty Py.  Becuase why not?")
	parser.add_argument('-u', '--url',
		required=True,
		type=str,
		help='Specify the host you wish to scan. IP addresses or domains are acceptable input.')
	
	parser.add_argument('-p', '--port',
		type=str,
		default='80',
		help='Specify the port to establish the connection on.')
	
	parser.add_argument('-r', '--rate',
		type=float,
		default=2,
		help='Set the rate of scan in requests per second.')
	
	parser.add_argument('-w', '--wordlist',
		required=True,
		type=str,
		help='Set the /path/to/wordlist file to use.')
	
	args = parser.parse_args()
	busty = Busty(args)
	try:
		busty.run()
	except KeyboardInterrupt:
		print(f"\n\x1b[101;41m << User Keyboard Interrupt >> \033[0m"+" "*20+"\n")
		exit()
