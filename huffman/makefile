all		:	huffman

huffman	:	nhuffman.py
			python nhuffman.py

run		:	huffman driver.py
			python -i driver.py
			
test	:	all tester.py
			python tester.py

clean	:	
			rm -rf __pycache__