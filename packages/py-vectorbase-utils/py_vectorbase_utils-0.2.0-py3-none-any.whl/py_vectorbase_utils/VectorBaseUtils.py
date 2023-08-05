'''
    Copyright (C) 2018, Romain Feron

    This file is part of py_vectorbase_utils.

    py_vectorbase_utils is free software: you can redistr(intibute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    py_vectorbase_utils is distr(intibuted in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with py_vectorbase_utils.  If not, see <https://www.gnu.org/licenses/>.
'''

import logging
from Bio import Entrez
from py_vectorbase_rest import VectorBaseRest
from py_vectorbase_utils.download_genome import GenomeDownloader


class VectorBaseUtils():
    '''
    VectorBaseUtils is the base class implementing the utility functions.
    Parameters:
        - ncbi_email_address: email address to use for NCBI queries
        - log_level: 0 (all), 1 (debug), 2 (info), 3 (warning), 4 (error), 5 (critical)
    '''
    def __init__(self, ncbi_email_address='email@email.com', log_level=2):
        self.vb_api = VectorBaseRest()
        self.vb_download_url = 'https://www.vectorbase.org/download'
        self.Entrez = Entrez
        self.Entrez.email = ncbi_email_address
        self.ncbi_ftp_url = 'ftp.ncbi.nlm.nih.gov'
        self.log_level = log_level
        self.init_logger()
        self.genome_downloader = GenomeDownloader(self.vb_api, self.vb_download_url, self.Entrez, self.ncbi_ftp_url)

    def init_logger(self):
        # Check log level
        log_level_warning = False
        try:
            self.log_level = int(self.log_level)
            if self.log_level not in range(6):
                raise ValueError
        except ValueError:
            self.log_level = 2
            log_level_warning = True
        # Logger format
        logging.basicConfig(level=self.log_level * 10, format='[%(asctime)s]::%(levelname)s %(message)s', datefmt='%Y.%m.%d-%H:%M:%S')
        if log_level_warning:
            logging.warning('Incorrect value <' + self.log_level + '> for verbosity. Logging level was set to <info>.')
