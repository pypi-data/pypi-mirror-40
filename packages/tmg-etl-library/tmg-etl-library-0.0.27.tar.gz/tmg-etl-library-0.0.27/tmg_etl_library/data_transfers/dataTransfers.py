from tmg_etl_library.data_transfers.transfer import Transfer
from tmg_etl_library.components.configClasses import *

from tmg_etl_library.components.databases import bq, mysql
from tmg_etl_library.components.locals import csv

import uuid


class BQ_to_BQ(Transfer):
    def __init__(self, log, source, target, config=BQ_to_BQ_config()):
        super().__init__(log, source, target, config)
        self.id = uuid.uuid4()
        self.source = source
        self.target = target
        if not isinstance(config, BQ_to_BQ_config):
            raise TypeError('Config Must be of Type: BQ_to_BQ_config')
        self.config = config
        self.log = log
        self.bq_client = bq.BQClient(self.log, source.project if source else target.project)

    def run(self):
        if self.config.query:
            self.bq_client.run_query(self.config.query, destination=self.target,
                                     write_disposition=self.config.write_disposition,
                                     use_legacy_sql=self.config.use_legacy_sql)
        else:
            self.bq_client.copy_tables(source=self.source, target=self.target, config=self.config)


class BQ_to_CSV(Transfer):
    def __init__(self, log, BQTable, CSVFile, config=BQ_to_CSV_config()):
        super().__init__(log, BQTable, CSVFile, config)
        self.id = uuid.uuid4()
        self.BQTable = BQTable
        self.CSVFile = CSVFile
        if not isinstance(config, BQ_to_CSV_config):
            raise TypeError('Config Must be of Type: BQ_to_CSV_config')
        self.config = config
        self.log = log
        self.bq_client = bq.BQClient(self.log, BQTable.project)

    def run(self):
        if self.config.full_table:
            self.bq_client.full_table_to_file(self.BQTable, self.CSVFile, self.config)
        elif self.config.query:
            self.bq_client.query_to_file(self.config.query, self.CSVFile, self.config)
        else:
            raise TypeError("Either 'full_table' or 'query' must be set in the BQ_to_CSV_config class")


class BQ_to_MySQL(Transfer):
    def __init__(self, log, source, target, config=BQ_to_MySQL_config()):
        super().__init__(log, source, target, config)
        self.id = uuid.uuid4()
        self.source = source
        self.target = target
        if not isinstance(config, BQ_to_MySQL_config):
            raise TypeError('Config Must be of Type: BQ_to_MySQL_config')
        self.config = config
        self.log = log

    def run(self):
        pass


class CSV_to_BQ(Transfer):
    def __init__(self, log, CSVFile, BQTable, config=CSV_to_BQ_config()):
        super().__init__(log, CSVFile, BQTable, config)
        self.id = uuid.uuid4()
        self.CSVFile = CSVFile
        self.BQTable = BQTable
        if not isinstance(config, CSV_to_BQ_config):
            raise TypeError('Config Must be of Type: CSV_to_BQ_config')
        self.config = config
        self.log = log
        self.bq_client = bq.BQClient(self.log, BQTable.project)

    def run(self):
        self.bq_client.insert_csv(self.CSVFile, self.BQTable, self.config)


class CSV_to_MySQL(Transfer):
    def __init__(self, log, source, target, config=CSV_to_MySQL_config()):
        super().__init__(log, source, target, config)
        self.id = uuid.uuid4()
        self.source = source
        self.target = target
        if not isinstance(config, CSV_to_MySQL_config):
            raise TypeError('Config Must be of Type: CSV_to_MySQL_config')
        self.config = config
        self.log = log

    def run(self):
        pass


class MySQL_to_BQ(Transfer):
    def __init__(self, log, source, target, config=MySQL_to_BQ_config()):
        super().__init__(log, source, target, config)
        self.id = uuid.uuid4()
        self.source = source
        self.target = target
        if not isinstance(config, MySQL_to_BQ_config):
            raise TypeError('Config Must be of Type: MySQL_to_BQ_config')
        self.config = config
        self.log = log

    def run(self):
        pass

