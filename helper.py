import os
import sys
import getopt
import json
import re
import logging
import urllib2
import BaseHTTPServer
import codecs

class MyHelper:
    name = 'MyHelper.py'
    logger = ''

    __TARGET_DIR  = './'
    __TARGET_FILE = 'composer.lock'
    __OUTPUT_FILE = 'AUTHORS'

    __COMPOSER_DATA = {}

    __AUTHORS_DATA = []

    __UNDEFINED_AUTHORS = []

    def __init__(self):
        self.set_logger()
        self.logger.info('::'.join([self.__class__.__name__, sys._getframe().f_code.co_name]))

    def check_params(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'O:', ['dir='])
        except getopt.GetoptError as err:
            print str(err)
            sys.exit(1)
        for o, v in opts:
            if o == '-O':
                self.__OUTPUT_FILE = v
            elif o == '--dir':
                rp = re.compile('.+\/$');
                c = rp.match(v)
                self.__TARGET_DIR = v if rp.match(v) else v + '/'

        self.logger.info('::'.join([self.__class__.__name__, sys._getframe().f_code.co_name]) + '::' +
                         'target file : ' + self.__TARGET_DIR + self.__TARGET_FILE)
        self.logger.info('::'.join([self.__class__.__name__, sys._getframe().f_code.co_name]) + '::' +
                         'output file : ' + self.__TARGET_DIR + self.__OUTPUT_FILE)

        return self

    def get_composer_data(self):

        target_file = self.__TARGET_DIR + self.__TARGET_FILE 

        if not os.path.exists(target_file):
            self.logger.error('::'.join([self.__class__.__name__, sys._getframe().f_code.co_name]) + ' : ' +
                              'composer file doesn\'t exists.[' + target_file + ']')
            exit(1)
        
        composer_json = open(target_file).read()
        composer_data = json.loads(composer_json)

        self.__COMPOSER_DATA = {
                                    'packages': composer_data['packages'],
                                    'packages-dev': composer_data['packages-dev']
                               }

        return self

    def get_license_info(self):
        license_filenames = ('LICENSE', 'LISENCE.md')

        for k in self.__COMPOSER_DATA:
            self.__AUTHORS_DATA.append('[' + k + ']')
            self.__AUTHORS_DATA.append('----')

            for pkg in self.__COMPOSER_DATA[k]:
                file_exists = 0
                file_data = ''
                self.logger.info('::'.join([self.__class__.__name__, sys._getframe().f_code.co_name]) + '::' +
                                 pkg['name'] + ' checking...')

                for fn in license_filenames:
                    rp = re.compile('https:\/\/github.com/(.+)\.git$');
                    em = rp.search(pkg['source']['url'])
                    license_path = 'https://raw.githubusercontent.com/' + em.group(1) + '/master/' + fn
                    req = urllib2.Request(license_path)

                    try:
                        res = urllib2.urlopen(req)
                        page = res.read()
                        self.logger.info('::'.join([self.__class__.__name__, sys._getframe().f_code.co_name]) + '::' +
                                         license_path + ' found.')

                        # set package name
                        self.__AUTHORS_DATA.append(pkg['name'] + '\t' + pkg['version'] + '\n')

                        # set license
                        self.__AUTHORS_DATA.append(pkg['license'][0] + ' License\n')

                        # set authors info from page
                        lines = page.split('\n')
                        author_rp = re.compile('^Copyright.+$')
                        for line in lines:
                            author_em = author_rp.search(line)
                            if author_em:
                                author = author_em.group(0)
                                self.__AUTHORS_DATA.append(unicode(author, 'utf-8'))

                        # set license file path
                        self.__AUTHORS_DATA.append(u'\n' + license_path + u'\n')

                        self.__AUTHORS_DATA.append(u'----')

                        file_exists = 1
                        break

                    except urllib2.HTTPError as err:
                        # self.logger.warn(err.code)
                        # self.logger.warn(BaseHTTPServer.BaseHTTPRequestHandler.responses[err.code][1])
                        continue

                if file_exists == 0:
                    self.__UNDEFINED_AUTHORS.append(pkg['name'])
                    self.logger.warn('::'.join([self.__class__.__name__, sys._getframe().f_code.co_name]) + '::' +
                                     'license file not found.[' + pkg['name'] + ']')

        return self

    def make_authors_file(self):
        output_file = self.__TARGET_DIR + self.__OUTPUT_FILE

        try:
            f = codecs.open(output_file, 'w', 'utf-8')
        except IOError:
            self.logger.error('::'.join([self.__class__.__name__, sys._getframe().f_code.co_name]) + '::' +
                              output_file + ' cannot be opened.')
            exit(1)
        else:
            data = u'\n'.join(self.__AUTHORS_DATA)
            f.write(data)
            f.close

            self.logger.info('::'.join([self.__class__.__name__, sys._getframe().f_code.co_name]) + '::' +
                             output_file + ' successfully ceated.')

        return self

    def test_debug(self):
        print "DEBUG END POINT"

    """ set_logger()
    """
    def set_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] - %(message)s')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    """ get_target_file(self)
    get target composer file.
    """
    def get_target_file(self):
        return self.__TARGET_FILE
