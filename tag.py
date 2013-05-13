import sys
import operator
import re


class ArgumentError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def word_freq(text):
	text = re.sub(r'[^A-Za-z0-9 ]', '', text)
	words = text.split()
	freq = {}
	for word in words:
		word = word.lower()
		if word in freq.keys():
			freq[word] += 1
		else:
			freq[word] = 1
	return freq

def word_filter(freq_list, threshold):
	#filters out words appearing fewer times than given threshold
	freq = dict((k,v) for k, v in freq_list.items() if v >= threshold)
	return freq

	
def write_freq(freq):
	# writes words and frequencies to a CSV
	fname = "frequencies.csv"
	f = open(fname, 'w')
	for item in freq:
		f.write(item[0] + "," + str(item[1]) + "\n")
	f.close()

def filter_stop_words(freq):
	f = open('stop_words.txt')
	raw = f.read()
	stop_words = raw.split()
	filtered = []
	words = freq.keys()
	for word in words:
		if word in stop_words:
			freq.pop(word, None)
	return freq

def main():
	try:
		if (len(sys.argv) < 3):
			raise ArgumentError('Too few arguments')
	except ArgumentError:
		print "Correct usage is ./tag.py [file] [threshold]"
	else:
		fname = sys.argv[1]
		f = open(fname)
		text = f.read()
		f.close()
		freq = filter_stop_words(word_filter(word_freq(text), int(sys.argv[2])))
		freq_sorted = sorted(freq.iteritems(), key=operator.itemgetter(1))
		print freq_sorted
		write_freq(freq_sorted)

main()


