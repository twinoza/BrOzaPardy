from brozapp.app import app
import logging


def main():
	# to log to a file, uncomment the next line
#	logging.basicConfig(filename='brozapp.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)  # for console logging
	logging.info('Started logging')
	app.run(host='0.0.0.0', port=5000, debug=True)
	logging.info('Finished logging')

if __name__ == '__main__':
	main()
