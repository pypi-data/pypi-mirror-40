
import pandas as pd  # data mangling and transforming


class MockupAttributes:
    """Attributes class for creating mock up data."""

    def __init__(self, output_path='../sample_data/', n_cells=1000,
                 n_cells_p_antenna=3, n_users=100000, n_avg_daily_events=25,
                 cell_cname='CELL_ID', antenna_cname='SITE_ID',
                 long_cname='X', lat_cname='Y',
                 type_cname='CALL_RECORD_TYPE',
                 msisdn_cname='CALLER_MSISDN',
                 date_cname='CALL_DATE',
                 service_cname='BASIC_SERVICE',
                 location_cname='MS_LOCATION',
                 partner_type_cname='CALL_PARTNER_IDENTITY_TYPE',
                 partner_cname='CALL_PARTNER_IDENTITY',
                 tac_cname='TAC_CODE',
                 duration_cname='CALL_DURATION',
                 long_range=[28, 38], lat_range=[11, 16],
                 call_unit='s', max_call_duration=7000,
                 date_window=['2018-01-01', '2018-12-31'],
                 date_format=None,
                 loc_file_name='MS_LOCATION.csv',
                 raw_header=True, location_header=True):

        # outputpath
        self.output_path = output_path

        # number of generated cells
        self.n_cells = n_cells
        # number of cells per antenna
        self.n_cells_p_antenna = n_cells_p_antenna
        # number of desired user_ids
        self.n_users = n_users
        # generating n of total events
        # multiply users, daily events and days, then divide by 2 to
        # control for outgoing and incoming side of events
        n_days = len(pd.date_range(date_window[0], date_window[1]))
        self.n_total_events = round(self.n_users*n_avg_daily_events*n_days/2)

        # locations column names
        self.loc_column_names = {'cell': cell_cname,
                                 'antenna': antenna_cname,
                                 'long': long_cname,
                                 'lat': lat_cname}

        # raw data column names
        self.raw_column_names = {'type': type_cname,
                                 'msisdn': msisdn_cname,
                                 'date': date_cname,
                                 'service': service_cname,
                                 'location': location_cname,
                                 'partner_type': partner_type_cname,
                                 'partner': partner_cname,
                                 'tac': tac_cname,
                                 'duration': duration_cname}

        # coordinates ranges
        self.long_range = long_range
        self.lat_range = lat_range

        # call specific attributes
        self.call_unit = call_unit  # one of m (minutes) or s (seconds)
        self.max_call_duration = max_call_duration  # maxi duration of a call

        # date timestamp specifics
        self.date_window = date_window  # start and end date of raw metadata
        self.date_format = date_format  # output format of date timestamp

        # name of the file which holds the cell location coordinates
        self.loc_file_name = loc_file_name
        # keep headers of output files
        self.raw_header = raw_header
        self.location_header = location_header
