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

from Bio import Entrez
from py_vectorbase_rest import VectorBaseRest
from py_vectorbase_utils.download_genome import GenomeDownloader


class VectorBaseUtils():
    '''
    VectorBaseUtils is the base class implementing the utility functions.
    '''
    def __init__(self, ncbi_email_address='email@email.com', logs=True):
        self.vb_api = VectorBaseRest()
        self.vb_download_url = 'https://www.vectorbase.org/download'
        self.Entrez = Entrez
        self.Entrez.email = ncbi_email_address
        self.ncbi_ftp_url = 'ftp.ncbi.nlm.nih.gov'
        self.logs = logs
        self.genome_downloader = GenomeDownloader(self.vb_api, self.vb_download_url, self.Entrez, self.ncbi_ftp_url, self.logs)
