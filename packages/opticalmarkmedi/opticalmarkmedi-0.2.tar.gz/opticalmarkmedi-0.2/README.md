# optical_mark

Installation and Usage

opticalmarkmedi is available for python3

1. To install package, run:
	pip install opticalmarkmedi

Package requires some other library as:
	- imutils
	- numpy
	- opencv-python
	- scipy

Install all of them before import package

2. Import the package:
	import opticalmarkmedi

3. Usage the package:
	data_json = opticalmarkmedi.auto_mark("path/to/image")

This function return a json as the result of survey for each question