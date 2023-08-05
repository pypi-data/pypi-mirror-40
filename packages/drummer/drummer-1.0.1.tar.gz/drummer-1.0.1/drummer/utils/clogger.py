#!/usr/bin/python3
# -*- coding: utf-8 -*-
from logging.handlers import TimedRotatingFileHandler
from .configuration import Configuration
import logging


class Clogger():
    """ custom logger with colored text """

    @staticmethod
    def get(config, **kwargs):

        # log setting
        # ------------------------------------------------------- #

        name = config.get('application-name')

        logger = logging.getLogger(name)

        # avoid multiple initializations
        if not logger.handlers:

            logging_config = config.get('logging')

            logfile = logging_config.get('filename')
            log_level = kwargs.get('level') or logging_config.get('level')

            streaming = kwargs.get('streaming') or False

            fileLogFormatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            fileLogHandler = TimedRotatingFileHandler(logfile, when='d', interval=7, backupCount=4)
            fileLogHandler.setFormatter(fileLogFormatter)

            logger.addHandler(fileLogHandler)

            if streaming:

                streamLogFormatter = logging.Formatter('%(asctime)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
                streamLogHandler = logging.StreamHandler()
                streamLogHandler.setFormatter(streamLogFormatter)

                logger.addHandler(streamLogHandler)

            logger.setLevel(log_level)

        return logger
