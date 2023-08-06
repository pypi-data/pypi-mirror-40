# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:03:34 2016

@author: Charles-David Hebert
"""

import numpy as np
# import configparser
import os


class StatsArrays:

    """A class that implements the automated statistics of array files written
       in text file format. Arrays files have the following name format:
       'name'+ 'iteration' + 'end' + 'ext'. 
       """

    array_files_default = ["green", "self", "hyb"]
    array_files_middle_default = ["", "Up", "Down"]

    def __init__(self, array_files=array_files_default, middle_files=array_files_middle_default,
                 ext_files=[".dat", ], iter_start=1, ignore_col=None, in_dir=os.getcwd(),
                 warning_only=True):
        """Initialize the StatsArrays object.

        Args:

        Keywords Args:
            arrays_files (list||str): the arrays files in a list or a single string for one file
            ext: the extensions of the arrays_files
            iter_start: the iteration from which to start the statistics
            ignore_col (None||int): the col to ignore in the computations for the std
            in_dir (str): the dir in which the arrays_files are found.
            warning_only: the boolen controlling if only warnings are issued if
                          the files are not found
        Returns:

        Raises:

         """

        # check the existence of work dir
        self.in_dir = os.path.abspath(in_dir)
        assert(os.path.exists(self.in_dir)), "ayaya, in_dir does not exist"

        # creata a list of the obs_files
        self.array_files = array_files if isinstance(
            array_files, list) else [array_files]
        self.middle_files = middle_files if isinstance(
            middle_files, list) else [middle_files]

        if ignore_col is None:
            self.ignore_col = ignore_col
        else:
            assert(isinstance(ignore_col, int)
                   ), "Ayayaya, ignore_col must be None or int"
            self.ignore_col = ignore_col

        self.ext_files = ext_files if isinstance(
            ext_files, list) else [ext_files]
        self.iter_start = iter_start
        self.warning_only = warning_only  # make the program continue if files don't
        # exist, but give warning message
        files = [file + str(self.iter_start) + middle +
                 ext for file in self.array_files for middle in self.middle_files for ext in self.ext_files]
        self.check_sanity(files, self.warning_only)
        self.means = None  # set by mean()
        self.stds = None  # set by std()

    def read_file(self, file_name):
        """reads a files and their contents in a numpy array

        Args:

        Keywords Args:
                     file_name: the  to be read into a numpy array
        Returns:
               (data, file_exists):      

        """

        file_exists = os.path.isfile(file_name)
        # print("filename = ", file_name)

        if file_exists:
            data = np.loadtxt(file_name)
        else:
            data = None

        return (data, file_exists)

    def check_sanity(self, files, warning_only):
        """Check if the constructing attributes are sain"""

        for file in files:
            file_path = os.path.join(self.in_dir, file)
            file_path_exists = os.path.isfile(file_path)

            if file_path_exists:
                continue
            elif warning_only:
                print("\n Warning, file ", file, " does not exist")
                print("")
            else:
                assert(os.path.isfile(file_path)), "Ayaya, file does not exist"

            # print(file_path)
            #print(os.path.isfile(file_path)), "ayaya file does not exist"

        if isinstance(self.ignore_col, int):
            assert(self.ignore_col >= 0 and self.ignore_col <= 2), \
                "Ayayya, wrong colum ignored in obs files"

    def mean(self):
        """Computes the means of the arrays_files."""

        means = dict()

        for array_file in self.array_files:
            for middle_file in self.middle_files:
                for ext_file in self.ext_files:
                    cpt = 0
                    file_name = os.path.join(
                        self.in_dir, array_file + str(self.iter_start) + middle_file + ext_file)
                    # print(file_name)
                    (data, file_exists) = self.read_file(file_name)
                    if file_exists:
                        mean = np.zeros(data.shape)
                        while(file_exists):
                            mean += data
                            cpt += 1
                            #print("cpt ", cpt)
                            #print(array_file + middle_file + str(self.iter_start + cpt) + ext_file)
                            file_name = os.path.join(
                                self.in_dir, array_file + str(self.iter_start + cpt) + middle_file + ext_file)
                            (data, file_exists) = self.read_file(file_name)

                        mean /= cpt
                        #print("MEAN ", mean)
                        means[array_file + middle_file +
                              "_mean" + ext_file] = mean

        self.means = means
        # print(means)

    def std(self):
        """Compute the std errors of the observables and their error if applicable"""

        if self.means is None:
            self.mean
        stds = dict()

        for array_file in self.array_files:
            for middle_file in self.middle_files:
                for ext_file in self.ext_files:
                    cpt = 0
                    file_name = os.path.join(
                        self.in_dir, array_file + str(self.iter_start) + middle_file + ext_file)
                    (data, file_exists) = self.read_file(file_name)
                    if file_exists:
                        std = np.zeros(data.shape)
                        if self.ignore_col is not None:
                            std = np.delete(std, self.ignore_col, 1)

                        while(file_exists):
                            mean = self.means[array_file +
                                              middle_file + "_mean" + ext_file]
                            if self.ignore_col is not None:
                                data = np.delete(data, self.ignore_col, 1)
                                mean = np.delete(mean, self.ignore_col, 1)
                            std += np.power(data - mean, 2.0)
                            cpt += 1
                            file_name = os.path.join(
                                self.in_dir, array_file + str(self.iter_start + cpt) + middle_file + ext_file)
                            (data, file_exists) = self.read_file(file_name)

                        std /= cpt
                        stds[array_file + middle_file +
                             "_std" + ext_file] = np.sqrt(std)

        self.stds = stds

    def write_results(self, out_dir="Results", file_out="results_stats_obs.txt"):
        """ """

        # Add checking if the directory exists, create it if not, also, back_up old
        # stats_files. by backing up the ancient result directory in a new
        # directory with name Result-date or something like this

        files_mean = [file + end + "_mean" +
                      ext for file in self.array_files for end in self.middle_files for ext in self.ext_files]
        files_std = [file + end + "_std" +
                     ext for file in self.array_files for end in self.middle_files for ext in self.ext_files]

        for (key, value) in self.means.items():
            file_name = os.path.join(os.path.abspath(out_dir), key)
            np.savetxt(file_name, value)

        for (key, value) in self.stds.items():
            file_name = os.path.join(os.path.abspath(out_dir), key)
            np.savetxt(file_name, value)


#        for (file, mean) in zip(files_mean, self.means):
#            file_out_mean = os.path.join(out_dir, file)
#            np.savetxt(file_out_mean, mean)
#
#        for (file, std) in zip(files_std, self.stds):
#            file_out_std = os.path.join(out_dir, file)
#            np.savetxt(file_out_std, std)
