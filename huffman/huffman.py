import heapq
import os
import math

class heapNode:
	def __init__(self, char, freq):
		self.freq = freq
		self.char = char
		self.left = None
		self.right = None
	
	def __lt__(self, other):
		return self.freq < other.freq


class huffmanCoding:
	def __init__(self):
		self.path = ""
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}
		self.entropy = 0
		self.codeEntropy = 0
		self.frequency = {}
		self.output_path = ""
		self.padding = 0

	def printCodes(self):
		for key, code in self.codes.items():
			print(key + ": " + code)

	# functions for compression:

	def getFrequency(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def makeHeap(self):
		for key in self.frequency:
			node = (self.frequency[key], heapNode(key, self.frequency[key]))
			heapq.heappush(self.heap, node)

	def mergeNodes(self):
		while(len(self.heap)>1):
			f, node1 = heapq.heappop(self.heap)
			f, node2 = heapq.heappop(self.heap)

			mergedFreq = node1.freq + node2.freq
			merged = heapNode(None, mergedFreq)
			merged.left = node1
			merged.right = node2
			node = (mergedFreq, merged)
			heapq.heappush(self.heap, node)


	def makeCodesHelper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.makeCodesHelper(root.left, current_code + "0")
		self.makeCodesHelper(root.right, current_code + "1")


	def makeCodes(self):
		(f, root) = heapq.heappop(self.heap)
		current_code = ""
		if(root.char != None):
			current_code = "1"
		self.makeCodesHelper(root, current_code)


	def encodeText(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text


	def addPadding(self, encoded_text):
		extra_padding = (8 - len(encoded_text) % 8) % 8
		for i in range(extra_padding):
			encoded_text += "0"
		self.padding = extra_padding
		return encoded_text

	def getBytes(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b

	def compress(self):
		self.path = input("Enter file name: ")
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".bin"
		self.output_path = output_path

		with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
			text = file.read()

			self.frequency = self.getFrequency(text)
			self.makeHeap()
			self.mergeNodes()
			self.makeCodes()

			s = sum(self.frequency.values())
			for k, f in self.frequency.items():
				p = f/s
				self.entropy -= p * math.log2(p)
				self.codeEntropy += p * len(self.codes[k])

			encoded_text = self.encodeText(text)
			padded_encoded_text = self.addPadding(encoded_text)
			b = self.getBytes(padded_encoded_text)
			
			meta = bytearray()
			meta.append(len(self.reverse_mapping))
			meta.append(self.padding)
			meta = bytes(meta)
			output.write(bytes(meta))
			for code, key in self.reverse_mapping.items():
				output.write((str(code) + ":" + str(key) + "\n").encode())
			output.write(bytes(b))

		print("\nCompressed to " + output_path)
		print("Entropy of file: " + str(self.entropy))
		print("Entropy of code: " + str(self.codeEntropy))
		print("\nCodebook:-")
		self.printCodes()
		return output_path


	""" functions for decompression: """

	def removePadding(self, padded_encoded_text):
		extra_padding = self.padding
		if(extra_padding > 0):
			encoded_text = padded_encoded_text[:-1*extra_padding]
		else:
			encoded_text = padded_encoded_text
		return encoded_text

	def decodeText(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text


	def decompress(self):
		input_path = input("Enter file name: ")
		self.path = input_path
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + ".txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			codeSize = ord(file.read(1))
			self.padding = ord(file.read(1))

			while(codeSize > 0):
				meta = file.readline()
				meta = meta.decode().rstrip('\n')
				if(meta == ""):
					continue
				meta = meta.split(":", 1)
				self.reverse_mapping[meta[0]] = meta[1]
				if(meta[1] == ""):
					self.reverse_mapping[meta[0]] = "\n"
				codeSize -= 1

			bit_string = ""

			byte = file.read(1)
			while byte:
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			encoded_text = self.removePadding(bit_string)

			decompressed_text = self.decodeText(encoded_text)
			
			output.write(decompressed_text)

		print("Decompressed")
		return output_path