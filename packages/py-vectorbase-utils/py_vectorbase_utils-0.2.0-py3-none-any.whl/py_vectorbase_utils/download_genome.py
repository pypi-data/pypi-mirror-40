'''
    Copyright (C) 2018, Romain Feron
    The download_genome_vectorbase function is based on code from
    Boris Schnider (C) 2018, Vectorbase-data-request

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

import ftplib
import gzip
import io
import logging
import os
import re
import shutil
import urllib
from time import time
import py_vectorbase_rest


class DownloadFile:
    '''
    Container class for download file information
    '''

    def __init__(self):
        self.species = None
        self.assembly_name = None
        self.assembly_file = None
        self.full_file_url = None
        self.local_filename = None
        self.date = None
        self.size = None

    def print_info(self):
        logging.info('\nFile info:')
        logging.info('    - species : ', self.species)
        logging.info('    - assembly_name : ', self.assembly_name)
        logging.info('    - assembly_file : ', self.assembly_file)
        logging.info('    - full_file_url : ', self.full_file_url)
        logging.info('    - local_filename : ', self.local_filename)
        logging.info('    - date : ', self.date)
        logging.info('    - size : ', self.size)


class GenomeDownloader:
    '''
    A general class grouping method to download genome files from VectorBase or from NCBI.
    Currently, two types of files are supported:
    - FASTA files for the assembly (the higher level of assembly is automatically downloaded)
    - RepeatMasker libraries
    '''

    def __init__(self, vb_api, vb_download_url, Entrez, ncbi_ftp_url):
        '''
        Constructor for GenomeDownloader class.
        vb_api, vb_download_url, Entrez, and ncbi_ftp_url are passed from the parent VectorBaseUtils instance.
        output_dir, origin (VectorBase or NCBI), and decompress can be set after construction to simplify syntax when downloading multiple genomes.
        '''
        self.vb_api = vb_api
        self.vb_download_url = vb_download_url
        self.vb_assembly_query_url = self.vb_download_url + 's?field_organism_taxonomy_tid[]=SPECIESASSEMBLY&field_status_value=Current'
        self.Entrez = Entrez
        self.ncbi_ftp_url = ncbi_ftp_url
        self.output_dir = './'
        self.origin = 'vectorbase'
        self.decompress = True
        self.info = DownloadFile()

    def download_genome(self, species, output_dir=None, origin=None, decompress=None):
        '''
        General wrapper function to download a genome.
        Output directory and download origin (VectorBase or NCBI) can be specified when calling the function,
        or they can be set for the GenomeDownloader instance if downloading many genomes.
        '''
        self.info = DownloadFile()
        self.info.species = species
        self.info.species_tag = '[' + species + '] '
        if not output_dir:
            output_dir = self.output_dir
        if not os.path.isdir(output_dir):
            logging.error(self.info.species_tag + 'Output directory <' + output_dir + '> does not exist.')
            return False
        if not origin:
            origin = self.origin
        if not decompress:
            decompress = self.decompress
        if origin == 'vectorbase':
            status = self.download_genome_vectorbase(output_dir=output_dir, decompress=decompress)
        elif origin == 'ncbi':
            status = self.download_genome_ncbi(output_dir=output_dir, decompress=decompress)
        else:
            logging.error(self.info.species_tag + 'Unknown value for origin parameter : <' + str(origin) + '>. Value should be "vectorbase" or "ncbi".')
            return False
        return status

    def download_repeat_library(self, species, output_dir=None):
        pass

    def get_assembly_info_from_vb(self):
        '''
        Get assembly name and assembly info page from a species name by querying VectorBase.
        Returns the query response
        '''
        try:
            vb_response = self.vb_api.assembly_info(species=self.info.species)  # Get assembly info from VB API
            self.info.assembly_name = vb_response['assembly_name']
            self.info.date = vb_response['assembly_date']
            if not self.info.date:
                self.info.date = '?'
            self.info.size = vb_response['base_pairs']
            if not self.info.size:
                self.info.size = '?'
            request_url = self.vb_assembly_query_url.replace("SPECIESASSEMBLY", self.info.assembly_name)
            response = urllib.request.urlopen(request_url)
        except py_vectorbase_rest.VectorBaseRestError:
            logging.error(self.info.species_tag + 'Could not find assembly info in VectorBase.')
            return None
        except KeyError:
            logging.error(self.info.species_tag + 'Could not find assembly name in assembly info.')
            return None
        except urllib.error.URLError:
            logging.error(self.info.species_tag + 'There was an error when trying to access assembly information page.')
            return None
        return response

    def save_file(self, response, decompress):
        '''
        Save an object from an URL to a local file, decompressing if specified.
        '''
        try:
            response = urllib.request.urlopen(self.info.full_file_url)
        except urllib.error.URLError:
            logging.error(self.info.species_tag + 'There was an error when trying to access download URL.')
            return False

        if decompress:
            self.info.local_filename = self.info.local_filename.replace('.gz', '')

        logging.info(self.info.species_tag + 'Downloading file <' + self.info.assembly_file + '> to <' + self.info.local_filename + '> ...')
        step_time_start = time()

        if decompress:
            temp_file = io.BytesIO(response.read())
            download_file_object = gzip.GzipFile(fileobj=temp_file)
            with open(self.info.local_filename, 'wb') as output_file:
                output_file.write(download_file_object.read())
        else:
            with open(self.info.local_filename, 'wb') as output_file:
                shutil.copyfileobj(response, output_file)

        logging.info(self.info.species_tag + 'Successfully downloaded file <' + self.info.assembly_file + '> to <' + self.info.local_filename + '> (' + str(int(time() - step_time_start)) + 's).')
        return True

    def download_genome_vectorbase(self, output_dir, decompress):
        '''
        Download a genome using Vectorbase API and VectorBase DL URLs.
        Steps:
        1) Get assembly name by querying VectorBase
        2) Get download page for assembly and identify the best assembly file
        3) Reconstruct download URL for identified file
        4) Download the file object to a local file
        '''
        output_dir = os.path.abspath(output_dir)  # Convert relative path to absolute path for output folder
        total_time_start = time()

        logging.info(self.info.species_tag + 'Retrieving assembly info from VectorBase ...')
        step_time_start = time()

        response = self.get_assembly_info_from_vb()
        if not response:
            return False

        logging.info(self.info.species_tag + 'Successfully retrieved assembly info (' + str(int(time() - step_time_start)) + 's)')
        logging.info(self.info.species_tag + 'Identifying best assembly file ...')
        step_time_start = time()

        temp = re.findall("{}.*?{}.fa.gz".format("-".join(self.info.species.capitalize().split("_")), self.info.assembly_name), str(response.read()))

        if len(temp) > 0:
            assembly_files = {a.split('_')[-2]: a for a in temp}
            if 'CHROMOSOMES' in assembly_files.keys():
                self.info.assembly_file = assembly_files['CHROMOSOMES']
            elif 'SCAFFOLDS' in assembly_files.keys():
                self.info.assembly_file = assembly_files['SCAFFOLDS']
            elif 'CONTIGS' in assembly_files.keys():
                self.info.assembly_file = assembly_files['CONTIGS']
            else:
                logging.error(self.info.species_tag + 'Could not find standard assembly file. Files found: ' + ','.join(assembly_files) + '.')
                return False
        else:
            logging.error(self.info.species_tag + 'Could not find any assembly file.')
            return False

        file_name_url = ''.join(char for char in self.info.assembly_file if char not in ["_", "."])
        tmp = file_name_url.split('-')
        # Special case for Anopheles-culicifacies-A : the '-A' is removed from the final URL ...
        if len(tmp) > 3:
            del tmp[2]
            file_name_url = '-'.join(tmp)
        self.info.full_file_url = "{}/{}".format(self.vb_download_url, file_name_url)
        self.info.local_filename = os.path.join(output_dir, self.info.assembly_file)

        logging.info(self.info.species_tag + 'Successfully indentified best assembly file <' + self.info.assembly_file + '> (' + str(int(time() - step_time_start)) + 's)')
        status = self.save_file(response, decompress)
        logging.info(self.info.species_tag + 'Total elapsed time : ' + str(int(time() - total_time_start)) + 's')
        return status

    def download_genome_ncbi(self, output_dir, decompress):
        '''
        Download a genome using Vectorbase API, NCBI Entrez API, and NCBI GenBank FTP.
        Steps:
        1) Get accession number from Vectorbase's API assembly_info
        2) Lookup accession number on NCBI and get GenBank FTP address
        3) Connect to NCBI's FTP and navigate to the right directory
        4) Download the genome file to the specified location (default: current directory)
        '''

        output_dir = os.path.abspath(output_dir)  # Convert relative path to absolute path for output folder
        total_time_start = time()

        logging.info('Retrieving accession number from VectorBase for species <' + self.info.species + '> ...')
        step_time_start = time()

        vb_response = self.vb_api.assembly_info(species=self.info.species)  # Get assembly info from VB API
        accession_number = vb_response['assembly_accession']  # Get accession number from API request response

        logging.info('Successfully retrieved accession number <' + accession_number + '> for species <' + self.info.species + '> (' + str(int(time() - step_time_start)) + 's)')
        logging.info('Retrieving ftp address from NCBI for species <' + self.info.species + '> ...')
        step_time_start = time()

        # Search for accession number using esearch from NCBI Entrez eutilies.
        # Results are stored in history (Entrez feature) to then be used by esummary.
        # Esummary returns all the information about the accession number, included the FTP path
        esearch_response = self.Entrez.esearch(db='assembly', term=accession_number, usehistory='y')
        esearch_response_parsed = self.Entrez.read(esearch_response)
        esummary_response = self.Entrez.esummary(db='assembly',
                                                 query_key=esearch_response_parsed['QueryKey'],
                                                 WebEnv=esearch_response_parsed['WebEnv'])
        esummary_response_parsed = self.Entrez.read(esummary_response)

        # Get FTP path from esummary response and trim it to only keep the full folder path
        genbank_ftp_path = esummary_response_parsed['DocumentSummarySet']['DocumentSummary'][0]['FtpPath_GenBank']
        genbank_ftp_path = genbank_ftp_path.replace('ftp://' + self.ncbi_ftp_url, '')

        logging.info('Successfully retrieved ftp address <' + genbank_ftp_path + '> for species <' + self.info.species + '> (' + str(int(time() - step_time_start)) + 's)')
        logging.info('Connecting to NCBI ftp for species <' + self.info.species + '>')
        step_time_start = time()

        genome_base_name = genbank_ftp_path.split('/')[-1]  # Genome file base name is the same as the folder name
        genome_file_name = genome_base_name + '_genomic.fna.gz'

        # Connect to NCBI FTP
        with ftplib.FTP(self.ncbi_ftp_url) as ncbi_ftp:
            ncbi_ftp.login()
            ncbi_ftp.cwd(genbank_ftp_path)  # Navigate to genome directory

            logging.info(self.info.species_tag + 'Successfully connected to NCBI ftp (' + str(int(time() - step_time_start)) + 's)')

            # Look for the correct file in the directory: <genome_base_name>_genomic.fna.gz
            dir_content = []
            ncbi_ftp.retrlines("LIST", dir_content.append)  # Store directory content into a list of strings
            for line in dir_content:
                temp = line.split(None, 8)
                if temp[8] == genome_file_name:  # File name is in the 9th field
                    local_filename = os.path.join(output_dir, genome_file_name)
                    logging.info(self.info.species_tag + 'Downloading file <' + genome_file_name + '> to folder <' + output_dir + '> ...')
                    step_time_start = time()
                    local_file = open(local_filename, "wb")  # Open a binary file to download the genome
                    ncbi_ftp.retrbinary("RETR " + temp[8], local_file.write, 16 * 1024)  # Read from the socket 16 bytes at a time
                    local_file.close()

        logging.info(self.info.species_tag + 'Successfully downloaded file <' + genome_file_name + '> to folder <' + output_dir + '> (' + str(int(time() - step_time_start)) + 's).')
        logging.info(self.info.species_tag + 'Total elapsed time : ' + str(int(time() - total_time_start)) + 's')
        return True
