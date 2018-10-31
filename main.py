import afinn165 as afinn
import re
import json
from collections import OrderedDict
from tkinter.filedialog import askopenfilename

"""
Chapman Nitta
CS 521 O2
August 13, 2018
Term Project
"""


def validate_upload():
	"""
	Validates if a user wants to wants to upload a text file for analysis
	:return: upload_file funcction
	"""
	decision = input('Would you like to upload a file to analyze? Please enter "Y" or "N": ').strip().lower()
	if decision == 'y':
		return upload_file()
	elif decision == 'n':
		print('Exiting program...')
		exit()
	else:
		print('Please enter a valid decision - "Y" or "N": ')
		return validate_upload()


def upload_file():
	"""
	Prompts a user to upload a text file if they said yes to the validate upload function
	:return: returns the name of the file the user selected
	"""
	try:
		file_name = askopenfilename(filetypes=(("Text File", "*.txt"), ("All Files", "*.*")), title="Choose a file")
		opened_file = open(file_name, 'r')
		file_name = opened_file.name
		return file_name
	except Exception as error:
		print('File not found')
		validate_upload()


def count_words:

	word_list = {}

	for word in words:
		if word not in word_list:
			word_list[word] = 1
		else:
			word_list[word] += 1


def main_menu(file):
	"""
	Displays the main menu for user input on the program options
	:param file: name of the txt file that user selected
	:return: Brings up options for users to run analysis on the data in the txt file
	"""
	print('================================')
	print('1. Show Text')
	print('2. Get Word Count')
	print('3. Sentiment Analysis')
	print('4. New File')
	print('5. Exit Program')
	print('================================')
	try:
		choice = int(input('Choose a numbered option from the menu above:').strip())
		return run_selection(choice, file)
	except ValueError:
		print()
		print('=========================================================')
		print('Please choose a valid numbered option from the list above')
		print('=========================================================')
		print()
		main_menu(file)
	except TypeError:
		print()
		print('=========================================================')
		print('Please choose a valid numbered option from the list above')
		print('=========================================================')
		print()
		main_menu(file)


def run_selection(choice, file):
	"""
	Executes the functions listed in the menu
	:param choice: The user selected menu choice
	:param file: The name of the user selected file
	:return: Methods from the File Class
	"""
	if choice == 1:
		file.show_text()
		return_to_main_menu(file)
	elif choice == 2:
		file.count_words()
		return_to_main_menu(file)
	elif choice == 3:
		file.analyze_text()
		return_to_main_menu(file)
	elif choice == 4:
		main()
	elif choice == 5:
		print('Exiting program')
		exit()
	else:
		print()
		print('Please enter a number listed in the menu above')
		main_menu(file)


def return_to_main_menu(file):
	"""
	Allows the user to return to the main menu after executing any of the options
	:param file: The name of the user selected file
	:return: Returns to the main menu screen or exits the program
	"""
	print()
	print('=========================================================================================')
	print('Would you like to return to the main menu? Type "Y" to go back or "N" to exit the program')
	print('=========================================================================================')
	print()
	decision = input('>').upper()
	if decision == 'Y':
		main_menu(file)
	elif decision == 'N':
		exit()
	else:
		print()
		print('========================')
		print('Please enter "Y" or "N."')
		print('========================')
		print()
		return_to_main_menu(file)


class File:
	__scrubbed_text = list
	word_count = {}
	rated_words = {}

	def __init__(self, file_name):
		self.file_name = file_name

	def __repr__(self):
		return 'File Name:', self.file_name

	def show_text(self):
		"""
		Prints out the content of the user selected file
		:return: The content of the user selected file
		"""
		open_file = open(self.file_name, 'r')
		print()
		print('================================')
		print(self.file_name)
		print('================================')
		print()
		print(open_file.read())

	def __scrub_text(self):
		"""
		Scrubs the txt to remove any special characters
		:return: The scrubbed text
		"""
		# Parses the relevant html that contains the text from the document object model
		open_file = open(self.file_name, 'r')
		text = open_file.read()
		text = text.replace('<br/>', '').replace('</div>', '').replace('\n', ' ').replace('\r', '').replace('\'', '')
		text = re.sub('[^A-Za-z0-9]+', " ", text).strip()
		self.scrubbed_text = text.lower().split(' ')
		self.scrubbed_text.sort()
		return self

	def count_words(self):
		"""
		Parses the scrubbed text and counts the number of instances there are of each word and places them in a
		dictionary
		:return: The dictionary containing the counts of the words in the user uploaded file
		"""
		self.__scrub_text()

		# loops the scrubbed text list and creates a dictionary to count how instances of each word there are in a file
		for word in self.scrubbed_text:
			if word not in self.word_count:
				self.word_count[word] = 1
			else:
				self.word_count[word] += 1

		print()
		print('================')
		print('Word Count')
		print('================')

		self.word_count = OrderedDict(sorted(self.word_count.items(), key=lambda t: t[1]))
		for key, value in self.word_count.items():
			print(key + ':', value)

		print()
		print('Word count for', self.file_name, 'has been exported to Word Count.txt')
		print()

		with open('Word Count.txt', 'w+') as outfile:
			outfile.write(json.dumps(self.word_count))
		return self

	def analyze_text(self):
		"""
		Parses the scrubbed text to see if any words in the text are also found in the AFINN165 list. If they are, it
		adds them to to dictionary and runs basic analysis on them
		:return: A dictionary listing of the words in the file that having matching sentiment scores, their summation,
		average, and count of unique words.
		"""
		self.__scrub_text()
		print()
		print('================')
		print('Sentiment Scores')
		print('================')

		unique_words = set()
		score = 0

		for key in self.scrubbed_text:
			if key in afinn.sentiment_score:
				unique_words.add(key)
				self.rated_words[key] = afinn.sentiment_score[key]
				score += afinn.sentiment_score[key]
			else:
				continue

		self.rated_words = OrderedDict(sorted(self.rated_words.items(), key=lambda t: t[1]))
		for key, value in self.rated_words.items():
			print(key + ':', value)

		with open('Sentiment Analysis.txt', 'w+') as outfile:
			outfile.write(json.dumps(self.rated_words))

		print()
		print('===============')
		print('File Statistics')
		print('===============')
		print()
		print('- Out of the', len(self.scrubbed_text), 'total words in this file,', len(unique_words), 'of them exist in the AFINN165 list.')
		try:
			average = float(score / len(unique_words))
			print('- Those', len(unique_words), 'words have an average sentiment score of', average)
			print('- Total Score:', score, '(Calculated via the sum of the words) ')
		except ZeroDivisionError:
			print('No words found associated in the AFINN165. Can\'t compute an average as a division by zero error '
			      'would occur.')

		print()
		print('Sentiment analysis for', self.file_name, 'has been exported to Sentiment Analysis.txt')
		print()



def main():
	file = File(validate_upload())
	main_menu(file)


main()
