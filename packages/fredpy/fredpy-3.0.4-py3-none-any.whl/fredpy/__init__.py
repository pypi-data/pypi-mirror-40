import requests,dateutil, pylab, datetime, os
import numpy as np
import pandas as pd
import statsmodels.api as sm
tsa = sm.tsa

# API key attribute needs to be set
api_key=None

def load_api_key(path):
    try:
        # Try to load file from currect working directory
        with open(path,'r') as api_key_file:
            return api_key_file.readline()
    except:

        try:
            # Try to find file in OSX home directory
            items = os.getcwd().split('/')[:3]
            items.append(path)
            path = '/'.join(items)
            with open(path,'r') as api_key_file:
                return api_key_file.readline()

        except:
            path = os.path.join(os.getcwd(),path)
            with open(path,'r') as api_key_file:
                return api_key_file.readline()


######################################################################################################
# The series class and methods

class series:

    '''Defines a class for downloading, storing, and manipulating data from FRED.'''

    def __init__(self,series_id=None):

        '''Initializes an instance of the series class.

        Args:
            series_id (string): unique FRED series ID. If series_id equals None, an empy series 
                                object is created.

        Returns:
            None

        Attributes:
            data:                       (numpy ndarray) data values.
            daterange:                  (string) specifies the dates of the first and last observations.
            dates:                      (list) list of date strings in YYYY-MM-DD format.
            datetimes:                  (numpy ndarray) array containing observation dates formatted as datetime objects.
            frequency:                  (string) data frequency. 'Daily', 'Weekly', 'Monthly', 'Quarterly', 'Semiannual', or 'Annual'.
            frequency_short:            (string) data frequency. Abbreviated. 'D', 'W', 'M', 'Q', 'SA, or 'A'.
            last_updated:               (string) date series was last updated.
            notes:                      (string) details about series. Not available for all series.
            release:                    (string) statistical release containing data.
            seasonal_adjustment:        (string) specifies whether the data has been seasonally adjusted.
            seasonal_adjustment_short:  (string) specifies whether the data has been seasonally adjusted. Abbreviated.
            series_id:                  (string) unique FRED series ID code.
            source:                     (string) original source of the data.
            t:                          (int) number corresponding to frequency: 365 for daily, 52 for weekly, 12 for monthly, 4 for quarterly, and 1 for annual.
            title:                      (string) title of the data series.
            units:                      (string) units of the data series.
            units_short:                (string) units of the data series. Abbreviated.
        '''

        if type(series_id) == str:



            request_url = 'https://api.stlouisfed.org/fred/series?series_id='+series_id+'&api_key='+api_key+'&file_type=json'
            r = requests.get(request_url)
            results = r.json()

            self.series_id = series_id
            self.title = results['seriess'][0]['title']
            self.frequency = results['seriess'][0]['frequency']
            self.frequency_short = results['seriess'][0]['frequency_short']
            self.units = results['seriess'][0]['units']
            self.units_short = results['seriess'][0]['units_short']
            self.seasonal_adjustment = results['seriess'][0]['seasonal_adjustment']
            self.seasonal_adjustment_short = results['seriess'][0]['seasonal_adjustment_short']
            self.last_updated = results['seriess'][0]['last_updated']
            try:
                self.notes = results['seriess'][0]['notes']
            except:
                self.notes = ''

            obs_per_year = {'D':365,'W':52,'M':12,'Q':4,'SA':2,'A':1}
            try:
                self.t = obs_per_year[self.frequency_short]
            except:
                self.t = np.nan


            request_url = 'https://api.stlouisfed.org/fred/series/observations?series_id='+series_id+'&api_key='+api_key+'&file_type=json'
            r = requests.get(request_url)
            results = r.json()

            count = results['count']

            self.data = np.zeros(count)
            self.dates = [None]*count
            for i in range(count):
                try:
                    self.data[i] = results['observations'][i]['value']
                except:
                    self.data[i] = np.nan
                self.dates[i] = results['observations'][i]['date']

            if np.isnan(self.data[0]):
                index =0
                for i,value in enumerate(self.data):
                    if np.isnan(value):
                        index+=1
                    else:
                        break
                self.data = self.data[index:]
                self.dates = self.dates[index:]
                
            self.datetimes = np.array([dateutil.parser.parse(s) for s in self.dates])
            self.daterange = 'Range: '+self.dates[0]+' to '+self.dates[-1]



            request_url =  'https://api.stlouisfed.org/fred/series/release?series_id='+series_id+'&api_key='+api_key+'&file_type=json'
            r = requests.get(request_url)
            results = r.json()
            self.release = results['releases'][0]['name']
            release_id = results['releases'][0]['id']


            request_url =  'https://api.stlouisfed.org/fred/release/sources?release_id='+str(release_id)+'&api_key='+api_key+'&file_type=json'
            r = requests.get(request_url)
            results = r.json()
            self.source = results['sources'][0]['name']

        else:

            self.data = np.array([])
            self.daterange = ''
            self.dates = []
            self.datetimes = np.array([])
            self.frequency = ''
            self.frequency_short = ''
            self.last_updated = ''
            self.notes = ''
            self.release = ''
            self.seasonal_adjustment = ''
            self.seasonal_adjustment_short = ''
            self.series_id = ''
            self.source = ''
            self.t = 0
            self.title = ''
            self.units = ''
            self.units_short = ''

    def apc(self,log=True,method='backward'):

        '''Computes the percentage change in the data over one year.

        Args:
            log (bool):        If True (default), computes the percentage change as 100⋅log[x(t)/x(t-1)]. 
                               If False, compute the percentage change as 100⋅[x(t)/x(t−1)−1].
            method (string):   If ‘backward’ (default), compute percentage change from the previous period. 
                               If ‘forward’, compute percentage change from current to subsequent period.

        Returns:
            fredpy series
        '''

        new_series = self.copy()
        
        T = len(self.data)
        t = self.t
        if log==True:
            pct = 100 * np.log(self.data[t:]/ self.data[0:-t])
        else:
            pct = 100 * (self.data[t:]/self.data[0:-t] - 1)
        if method=='backward':
            dte = self.dates[t:]
        elif method=='forward':
            dte = self.dates[:T-t]

        new_series.data  =pct
        new_series.dates =dte
        new_series.datetimes = np.array([dateutil.parser.parse(s) for s in dte])
        new_series.units = 'Percent'
        new_series.units_short = '%'
        new_series.title = 'Annual Percentage Change in '+self.title
        new_series.daterange = 'Range: '+new_series.dates[0]+' to '+new_series.dates[-1]

        return new_series

    def bpfilter(self,low=6,high=32,K=12):

        '''Computes the bandpass (Baxter-King) filter of the data. Returns a list of two fredpy.series
        instances containing the cyclical and trend components of the data:

            [new_series_cycle, new_series_trend]

        .. Note: 
            In computing the bandpass filter, K observations are lost from each end of the
            original series so the attributes dates, datetimes, and data are 2K elements 
            shorter than their counterparts in the original series.

        Args:
            low (int):  Minimum period for oscillations. Select 24 for monthly data, 6 for quarterly 
                        data (default), and 3 for annual data.
            high (int): Maximum period for oscillations.  Select 84 for monthly data, 32 for quarterly 
                        data (default), and 8 for annual data.
            K (int):    Lead-lag length of the filter. Select, 84 for monthly data, 12 for for quarterly
                        data (default), and 1.5 for annual data.

        Returns:
            list of two fredpy.series instances
        '''

        new_series_cycle = self.copy()
        new_series_trend = self.copy()

        if low==6 and high==32 and K==12 and self.t !=4:
            print('Warning: data frequency is not quarterly!')
        elif low==3 and high==8 and K==1.5 and self.t !=1:
            print('Warning: data frequency is not annual!')
            
        cycle = tsa.filters.bkfilter(self.data,low=low,high=high,K=K)
        actual = self.data[K:-K]
        trend = actual - cycle
        
        new_series_cycle.dates = self.dates[K:-K]
        new_series_cycle.datetimes = np.array([dateutil.parser.parse(s) for s in new_series_cycle.dates])
        new_series_cycle.data = cycle
        new_series_cycle.units = 'Deviation relative to trend'
        new_series_cycle.units_short = 'Dev. rel. to trend'
        new_series_cycle.title = self.title+' - deviation relative to trend (bandpass filtered)'
        new_series_cycle.daterange = 'Range: '+new_series_cycle.dates[0]+' to '+new_series_cycle.dates[-1]


        new_series_trend.dates = self.dates[K:-K]
        new_series_trend.datetimes = np.array([dateutil.parser.parse(s) for s in new_series_trend.dates])
        new_series_trend.data = trend
        new_series_trend.title = self.title+' - trend (bandpass filtered)'
        new_series_trend.daterange = 'Range: '+new_series_trend.dates[0]+' to '+new_series_trend.dates[-1]

        return [new_series_cycle, new_series_trend]

    def cffilter(self,low=6,high=32):

        '''Computes the Christiano-Fitzgerald (CF) filter of the data. Returns a list of two fredpy.series
        instances containing the cyclical and trend components of the data:

            [new_series_cycle, new_series_trend]

        Returns:
            list of two fredpy.series instances
        '''

        new_series_cycle = self.copy()
        new_series_trend = self.copy()

        if low==6 and high==32 and self.t !=4:
            print('Warning: data frequency is not quarterly!')
        elif low==1.5 and high==8 and self.t !=4:
            print('Warning: data frequency is not quarterly!')

        actual = self.data
        cycle, trend = tsa.filters.cffilter(self.data,low=low, high=high, drift=False)

        new_series_cycle.data = cycle
        new_series_cycle.units = 'Deviation relative to trend'
        new_series_cycle.units_short = 'Dev. rel. to trend'
        new_series_cycle.title = self.title+' - deviation relative to trend (CF filtered)'

        new_series_trend.data = trend
        new_series_trend.title = self.title+' - trend (CF filtered)'

        return [new_series_cycle, new_series_trend]

    def copy(self):

        '''Returns a copy of a series object.

        Args:

        Returs:
            fredpy series
        '''

        new_series = series()


        new_series.data = self.data
        new_series.daterange = self.daterange
        new_series.dates = self.dates
        new_series.datetimes = self.datetimes
        new_series.frequency = self.frequency
        new_series.frequency_short = self.frequency_short
        new_series.last_updated = self.last_updated
        new_series.notes = self.notes
        new_series.release = self.release
        new_series.seasonal_adjustment = self.seasonal_adjustment
        new_series.seasonal_adjustment_short = self.seasonal_adjustment_short
        new_series.series_id = self.series_id
        new_series.source = self.source
        new_series.t = self.t
        new_series.title = self.title
        new_series.units = self.units
        new_series.units_short = self.units_short


        if hasattr(self, 'cycle'):
            new_series.cycle = self.cycle

        if hasattr(self, 'trend'):
            new_series.trend = self.trend

        return new_series

    def divide(self,series2):

        '''Divides the data from the current fredpy series by the data from series2.

        Args:
            series2 (fredpy series): A fredpy series

        Note::
            Both series must have exactly the same date attribute. You are 
            responsibile for making sure that adding the series makes sense.
            E.g., this function will not stop you from adding a series with 
            units in dollars to another with units with hours.

        Returns:
            fredpy series
        '''

        if self.dates != series2.dates:

            raise ValueError('Current series and series2 do not have the same observation dates')

        else:

            new_series = series()

            new_series.title = self.title +' divided by '+series2.title
            if self.source == series2.source:
                new_series.source = self.source
            else:
                new_series.source = self.source +' and '+series2.source
            new_series.frequency = self.frequency
            new_series.frequency_short = self.frequency_short
            new_series.units = self.units +' / '+series2.units
            new_series.units_short = self.units_short +' / '+series2.units_short
            new_series.t = self.t
            new_series.daterange = self.daterange

            if self.seasonal_adjustment == series2.seasonal_adjustment:
                new_series.seasonal_adjustment = self.seasonal_adjustment
                new_series.seasonal_adjustment_short = self.seasonal_adjustment_short
            else:
                new_series.seasonal_adjustment = self.seasonal_adjustment +' and '+series2.seasonal_adjustment
                new_series.seasonal_adjustment_short = self.seasonal_adjustment_short +' and '+series2.seasonal_adjustment_short

            if self.last_updated == series2.last_updated:
                new_series.last_updated = self.last_updated
            else:
                new_series.last_updated = self.last_updated +' and '+series2.last_updated

            if self.release == series2.release:
                new_series.release = self.release
            else:
                new_series.release = self.release +' and '+series2.release

            new_series.series_id = self.series_id +' and '+series2.series_id
            new_series.data  = self.data/series2.data
            new_series.dates = self.dates
            new_series.datetimes = self.datetimes


            return new_series

    def firstdiff(self):

        '''Computes the first difference filter of original series. Returns a list of two fredpy.series
        instances containing the cyclical and trend components of the data:

            [new_series_cycle, new_series_trend]

        Note:
            In computing the first difference filter, the first observation from the original series is
            lost so the attributes dates, datetimes, and data are 1 element shorter than their 
            counterparts in the original series.

        Args:

        Returns:
            list of two fredpy.series instances
        '''

        new_series_cycle = self.copy()
        new_series_trend = self.copy()

        dy    = self.data[1:] - self.data[0:-1]
        gam   = np.mean(dy)
        cycle = dy - gam
        actual  = self.data[1:]
        trend = self.data[0:-1]

        new_series_cycle.dates = self.dates[1:]
        new_series_cycle.datetimes = self.datetimes[1:]
        new_series_cycle.data = cycle
        new_series_cycle.units = 'Deviation relative to trend'
        new_series_cycle.units_short = 'Dev. rel. to trend'
        new_series_cycle.title = self.title+' - deviation relative to trend (first difference filtered)'
        new_series_cycle.daterange = 'Range: '+new_series_cycle.dates[0]+' to '+new_series_cycle.dates[-1]


        new_series_trend.dates = self.dates[1:]
        new_series_trend.datetimes = self.datetimes[1:]
        new_series_trend.data = trend
        new_series_trend.title = self.title+' - trend (first difference filtered)'
        new_series_trend.daterange = 'Range: '+new_series_trend.dates[0]+' to '+new_series_trend.dates[-1]

        return [new_series_cycle, new_series_trend]

    def hpfilter(self,lamb=1600):

        '''Computes the Hodrick-Prescott (HP) filter of the data. Returns a list of two fredpy.series
        instances containing the cyclical and trend components of the data:

            [new_series_cycle, new_series_trend]

        Args:
            lamb (int): The Hodrick-Prescott smoothing parameter. Select 129600 for monthly data,
                        1600 for quarterly data (default), and 6.25 for annual data.
            
        Returns:
            list of two fredpy.series instances
        '''

        new_series_cycle = self.copy()
        new_series_trend = self.copy()

        if lamb==1600 and self.t !=4:
            print('Warning: data frequency is not quarterly!')
        elif lamb==129600 and self.t !=12:
            print('Warning: data frequency is not monthly!')
        elif lamb==6.25 and self.t !=1:
            print('Warning: data frequency is not annual!')
            
        cycle, trend = tsa.filters.hpfilter(self.data,lamb=lamb)

        new_series_cycle.data = cycle
        new_series_cycle.units = 'Deviation relative to trend'
        new_series_cycle.units_short = 'Dev. rel. to trend'
        new_series_cycle.title = self.title+' - deviation relative to trend (HP filtered)'

        new_series_trend.title = self.title+' - trend (HP filtered)'
        new_series_trend.data = trend

        return [new_series_cycle, new_series_trend]

    def lintrend(self):

        '''Computes a simple linear filter of the data using OLS. Returns a list of two fredpy.series
        instances containing the cyclical and trend components of the data:

            [new_series_cycle, new_series_trend]

        Args:

        Returns:
            list of two fredpy.series instances
        '''

        new_series_cycle = self.copy()
        new_series_trend = self.copy()

        y = self.data
        time = np.arange(len(self.data))
        x = np.column_stack([time])
        x = sm.add_constant(x)
        model = sm.OLS(y,x)
        result= model.fit()
        pred  = result.predict(x)
        
        cycle= y-pred
        trend= pred

        new_series_cycle.data = cycle
        new_series_cycle.units = 'Deviation relative to trend'
        new_series_cycle.units_short = 'Dev. rel. to trend'
        new_series_cycle.title = self.title+' - deviation relative to trend (linearly filtered via OLS)'

        new_series_trend.title = self.title+' - trend (linearly filtered via OLS)'
        new_series_trend.data = trend


        return [new_series_cycle, new_series_trend]

    def log(self):
        
        '''Computes the natural log of the data

        Args:

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        new_series.data = np.log(new_series.data)
        new_series.units = 'log '+new_series.units
        new_series.units_short = 'log '+new_series.units_short
        new_series.title = 'Log '+new_series.title

        return new_series

    def ma1side(self,length):

        '''Computes a one-sided moving average with window equal to length

        Args:
            length (int): length of the one-sided moving average.

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        length=int(length)
        z = np.array([])
        for s in range(len(self.data)-length+1):
            z = np.append(z,np.mean(self.data[s+0:s+length]))

        new_series.data = z
        new_series.dates =self.dates[length-1:]
        new_series.datetimes = np.array([dateutil.parser.parse(s) for s in new_series.dates])
        new_series.daterange = 'Range: '+new_series.dates[0]+' to '+new_series.dates[-1]
        new_series.title = self.title+' (1-sided moving average)'

        return new_series

    def ma2side(self,length):

        '''Computes a two-sided moving average with window equal to 2x length

        Args:
            length (int): half of length of the two-sided moving average. For example, if length = 12,
                          then the moving average will contain 24 the 12 periods before and the 12 
                          periods after each observation.

        Returns:
            fredpy series
        '''

        new_series = self.copy()
        
        length=int(length)
        z = np.array([])
        for s in range(len(self.data)-2*length):
            z = np.append(z,np.mean(self.data[s+0:s+2*length]))
        
        new_series.data = z
        new_series.dates =self.dates[length:-length]
        new_series.datetimes = np.array([dateutil.parser.parse(s) for s in new_series.dates])
        new_series.daterange = 'Range: '+new_series.dates[0]+' to '+new_series.dates[-1]
        new_series.title = self.title+' (2-sided moving average)'

        return new_series

    def minus(self,series2):

        '''Subtracts the data from series2 from the data from the current fredpy series.

        Args:
            series2 (fredpy series): A fredpy series

        Note::
            Both series must have exactly the same date attribute. You are 
            responsibile for making sure that adding the series makes sense.
            E.g., this function will not stop you from adding a series with 
            units in dollars to another with units with hours.

        Returns:
            fredpy series
        '''

        if self.dates != series2.dates:

            raise ValueError('Current series and series2 do not have the same observation dates')

        else:

            new_series = series()

            new_series.title = self.title +' minus '+series2.title
            if self.source == series2.source:
                new_series.source = self.source
            else:
                new_series.source = self.source +' and '+series2.source
            new_series.frequency = self.frequency
            new_series.frequency_short = self.frequency_short
            new_series.units = self.units +' - '+series2.units
            new_series.units_short = self.units_short +' - '+series2.units_short
            new_series.t = self.t
            new_series.daterange = self.daterange

            if self.seasonal_adjustment == series2.seasonal_adjustment:
                new_series.seasonal_adjustment = self.seasonal_adjustment
                new_series.seasonal_adjustment_short = self.seasonal_adjustment_short
            else:
                new_series.seasonal_adjustment = self.seasonal_adjustment +' and '+series2.seasonal_adjustment
                new_series.seasonal_adjustment_short = self.seasonal_adjustment_short +' and '+series2.seasonal_adjustment_short

            if self.last_updated == series2.last_updated:
                new_series.last_updated = self.last_updated
            else:
                new_series.last_updated = self.last_updated +' and '+series2.last_updated

            if self.release == series2.release:
                new_series.release = self.release
            else:
                new_series.release = self.release +' and '+series2.release

            new_series.series_id = self.series_id +' and '+series2.series_id
            new_series.data  = self.data-series2.data
            new_series.dates = self.dates
            new_series.datetimes = self.datetimes


            return new_series

    def monthtoannual(self,method='average'):

        '''Converts monthly data to annual data.

        Args:
            method (sring): Three values accepted:

                'average': average of values for 12 months
                'sum':     sum of the values for 12 months
                'end':     value in twelfth month only.

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        if self.t !=12:
            print('Warning: data frequency is not monthly!')
        T = len(self.data)
        temp_data = self.data[0:0]
        temp_dates = self.datetimes[0:0]
        if method =='average':
            for k in range(0,T):
                '''Annual data is the average of monthly data'''
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>11):
                    temp_data = np.append(temp_data,(self.data[k]+self.data[k+1]+self.data[k+2]+ self.data[k+3] + self.data[k+4] + self.data[k+5]
                        + self.data[k+6] + self.data[k+7] + self.data[k+8] + self.data[k+9] + self.data[k+10] + self.data[k+11])/12)  
                    temp_dates = np.append(temp_dates,self.dates[k])
        elif method =='sum':
            for k in range(0,T):
                '''Annual data is the sum of monthly data'''
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>11):
                    temp_data = np.append(temp_data,(self.data[k]+self.data[k+1]+self.data[k+2]+ self.data[k+3] + self.data[k+4] + self.data[k+5]
                        + self.data[k+6] + self.data[k+7] + self.data[k+8] + self.data[k+9] + self.data[k+10] + self.data[k+11]))
                    temp_dates = np.append(temp_dates,self.dates[k])
        elif method=='end':
            for k in range(0,T):
                '''Annual data is the end of year value'''
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>11):
                    temp_data = np.append(temp_data,self.data[k+11])
                    temp_dates = np.append(temp_dates,self.dates[k])
        
        new_series.data = temp_data
        new_series.dates = temp_dates
        new_series.datetimes = np.array([dateutil.parser.parse(s) for s in temp_dates])
        new_series.t = 1
        new_series.frequency = 'Annual'
        new_series.frequency_short = 'A'
        new_series.daterange = 'Range: '+new_series.dates[0]+' to '+new_series.dates[-1]

        return new_series


    def monthtoquarter(self,method='average'):
        
        '''Converts monthly data to quarterly data.

        Args:
            method (sring): Three values accepted:

                'average': average of values for three months
                'sum':     sum of the values for three months
                'end':     value in third month only.

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        if self.t !=12:
            print('Warning: data frequency is not monthly!')
        T = len(self.data)
        temp_data = self.data[0:0]
        temp_dates = self.datetimes[0:0]
        if method == 'average':
            for k in range(1,T-1):
                if (self.datetimes[k].month == 2) or (self.datetimes[k].month == 5) or (self.datetimes[k].month == 8) or (self.datetimes[k].month == 11):
                    temp_data = np.append(temp_data,(self.data[k-1]+self.data[k]+self.data[k+1])/3)
                    temp_dates = np.append(temp_dates,self.dates[k-1])
        elif method == 'sum':
            for k in range(1,T-1):
                if (self.datetimes[k].month == 2) or (self.datetimes[k].month == 5) or (self.datetimes[k].month == 8) or (self.datetimes[k].month == 11):
                    temp_data = np.append(temp_data,(self.data[k-1]+self.data[k]+self.data[k+1]))
                    temp_dates = np.append(temp_dates,self.dates[k-1])
        elif method== 'end':
            for k in range(1,T-1):
                if (self.datetimes[k].month == 2) or (self.datetimes[k].month == 5) or (self.datetimes[k].month == 8) or (self.datetimes[k].month == 11):
                    temp_data = np.append(temp_data,self.data[k+1])
                    temp_dates = np.append(temp_dates,self.dates[k-1])

        
        new_series.data = temp_data
        new_series.dates = temp_dates
        new_series.datetimes = np.array([dateutil.parser.parse(s) for s in temp_dates])
        new_series.t = 4
        new_series.frequency = 'Quarterly'
        new_series.frequency_short = 'Q'
        new_series.daterange = 'Range: '+new_series.dates[0]+' to '+new_series.dates[-1]

        return new_series


    def pc(self,log=True,method='backward',annualized=False):

        '''Computes the percentage change in the data from the preceding period.

        Args:
            log (bool):        If True (default), computes the percentage change as 100⋅log[x(t)/x(t-1)]. 
                               If False, compute the percentage change as 100⋅[x(t)/x(t−1)−1].
            method (string):   If ‘backward’ (default), compute percentage change from the previous period. 
                               If ‘forward’, compute percentage change from current to subsequent period.
            annualized (bool): If True (default), percentage change is annualized by multipying the simple 
                               percentage change by the number of data observations per year. E.g., if the
                               data are monthly, then the annualized percentage change is 4⋅100⋅log[x(t)/x(t−1)].

        Returns:
            fredpy series
        '''

        new_series = self.copy()
        
        T = len(self.data)
        t = self.t
        if log==True:
            pct = 100*np.log(self.data[1:]/self.data[0:-1])
        else:
            pct = 100*(self.data[1:]/self.data[0:-1] - 1)
        if annualized==True:
            pct = np.array([t*x for x in pct])
        if method=='backward':
            dte = self.dates[1:]
        elif method=='forward':
            dte = self.dates[:-1]


        new_series.data  =pct
        new_series.dates =dte
        new_series.datetimes = np.array([dateutil.parser.parse(s) for s in dte])
        new_series.units = 'Percent'
        new_series.units_short = '%'
        new_series.title = 'Percentage Change in '+self.title
        new_series.daterange = 'Range: '+new_series.dates[0]+' to '+new_series.dates[-1]

        return new_series

    def percapita(self,civ_pop = True):

        '''Transforms the data into per capita terms (US) by dividing by a measure of the total population:

        Args:
            civ_pop (string): If civ_pop == True, use Civilian noninstitutional population defined as 
                                persons 16 years of age and older (Default). Else, use the toal population.

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        T = len(self.data)
        temp_data   = self.data[0:0]
        temp_dates  = self.dates[0:0]
        if civ_pop ==True:
            populate= series('CNP16OV')
        else:
            populate= series('POP')
        T2 = len(populate.data)

        # Generate quarterly population data.
        if self.t == 4:
            for k in range(1,T2-1):
                if (populate.datetimes[k].month == 2) or (populate.datetimes[k].month == 5) or (populate.datetimes[k].month == 8) or \
                (populate.datetimes[k].month == 11):
                    temp_data = np.append(temp_data,(populate.data[k-1]+populate.data[k]+populate.data[k+1])/3)
                    temp_dates.append(populate.dates[k])

        # Generate annual population data.
        if self.t == 1:
            for k in range(0,T2):
                if (populate.datetimes[k].month == 1) and (len(populate.datetimes[k:])>11):
                    temp_data = np.append(temp_data,(populate.data[k]+populate.data[k+1]+populate.data[k+2]+populate.data[k+3]+populate.data[k+4]+populate.data[k+5] \
                        +populate.data[k+6]+populate.data[k+7]+populate.data[k+8]+populate.data[k+9]+populate.data[k+10]+populate.data[k+11])/12) 
                    temp_dates.append(populate.dates[k])

        if self.t == 12:
            temp_data  = populate.data
            temp_dates = populate.dates
        
        # form the population objects.    
        populate.data     = temp_data
        populate.dates    = temp_dates
        populate.datetimes = np.array([dateutil.parser.parse(s) for s in populate.dates])


        # find the minimum of data window:
        if populate.datetimes[0].date() <= self.datetimes[0].date():
            win_min = self.datetimes[0].strftime('%Y-%m-%d')
        else:
            win_min = populate.datetimes[0].strftime('%Y-%m-%d')

        # find the maximum of data window:
        if populate.datetimes[-1].date() <= self.datetimes[-1].date():
            win_max = populate.datetimes[-1].strftime('%Y-%m-%d')
        else:
            win_max = self.datetimes[-1].strftime('%Y-%m-%d')

        # set data window
        windo = [win_min,win_max]

        populate = populate.window(windo)
        new_series = new_series.window(windo)
        new_series.data = new_series.data/populate.data
        new_series.title = new_series.title+' Per Capita'
        new_series.units = new_series.units+' Per Thousand People'
        new_series.units_short = new_series.units_short+' Per Thousand People'
        new_series.daterange = 'Range: '+new_series.dates[0]+' to '+new_series.dates[-1]

        return new_series

    def plus(self,series2):

        '''Adds the data from the current fredpy series to the data from series2.

        Args:
            series2 (fredpy series): A fredpy series

        Note::
            Both series must have exactly the same date attribute. You are 
            responsibile for making sure that adding the series makes sense.
            E.g., this function will not stop you from adding a series with 
            units in dollars to another with units with hours.

        Returns:
            fredpy series
        '''

        if self.dates != series2.dates:

            raise ValueError('Current series and series2 do not have the same observation dates')

        else:

            new_series = series()

            new_series.title = self.title +' plus '+series2.title
            if self.source == series2.source:
                new_series.source = self.source
            else:
                new_series.source = self.source +' and '+series2.source
            new_series.frequency = self.frequency
            new_series.frequency_short = self.frequency_short
            new_series.units = self.units +' + '+series2.units
            new_series.units_short = self.units_short +' + '+series2.units_short
            new_series.t = self.t
            new_series.daterange = self.daterange

            if self.seasonal_adjustment == series2.seasonal_adjustment:
                new_series.seasonal_adjustment = self.seasonal_adjustment
                new_series.seasonal_adjustment_short = self.seasonal_adjustment_short
            else:
                new_series.seasonal_adjustment = self.seasonal_adjustment +' and '+series2.seasonal_adjustment
                new_series.seasonal_adjustment_short = self.seasonal_adjustment_short +' and '+series2.seasonal_adjustment_short

            if self.last_updated == series2.last_updated:
                new_series.last_updated = self.last_updated
            else:
                new_series.last_updated = self.last_updated +' and '+series2.last_updated

            if self.release == series2.release:
                new_series.release = self.release
            else:
                new_series.release = self.release +' and '+series2.release
                
            new_series.series_id = self.series_id +' and '+series2.series_id
            new_series.data  = self.data+series2.data
            new_series.dates = self.dates
            new_series.datetimes = self.datetimes


            return new_series

    def quartertoannual(self,method='average'):

        '''Converts quarterly data to annual data.

        Args:
            method (sring): Three values accepted:

                'average': average of values for four quarters
                'sum':     sum of the values for four quarters
                'end':     value in fourth quarter only.

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        if self.t !=4:
            print('Warning: data frequency is not quarterly!')
        T = len(self.data)
        temp_data = self.data[0:0]
        temp_dates = self.datetimes[0:0]
        if method =='average':
            for k in range(0,T):
                '''Annual data is the average of monthly data'''
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>3):
                    temp_data = np.append(temp_data,(self.data[k]+self.data[k+1]+self.data[k+2]+self.data[k+3])/4)
                    temp_dates = np.append(temp_dates,self.dates[k])
        elif method=='sum':
            for k in range(0,T):
                '''Annual data is the sum of monthly data'''
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>3):
                    temp_data = np.append(temp_data,self.data[k]+self.data[k+1]+self.data[k+2]+self.data[k+3])
                    temp_dates = np.append(temp_dates,self.dates[k])
        elif method == 'end':
            for k in range(0,T):
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>3):
                    '''Annual data is the end of month value'''
                    temp_data = np.append(temp_data,self.data[k+3])
                    temp_dates = np.append(temp_dates,self.dates[k])
        
        new_series.data = temp_data
        new_series.dates = temp_dates
        new_series.datetimes = np.array([dateutil.parser.parse(s) for s in temp_dates])
        new_series.t = 1
        new_series.freq = 'Annual'
        new_series.freq_short = 'A'
        new_series.daterange = 'Range: '+new_series.dates[0]+' to '+new_series.dates[-1]

        return new_series

    def recent(self,N):

        '''Restrict the data to the most recent N observations.

        Args:
            N (int): Number of periods to include in the data window.

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        new_series.data  =new_series.data[-N:]
        new_series.dates =new_series.dates[-N:]
        new_series.datetimes = np.array([dateutil.parser.parse(s) for s in new_series.dates])
        new_series.daterange = 'Range: '+new_series.dates[0]+' to '+new_series.dates[-1]

        return new_series

    def recessions(self,color='0.5',alpha = 0.5):
        
        '''Creates recession bars for plots. Should be used after a plot has been made but
            before either (1) a new plot is created or (2) a show command is issued.

        Args:
            color (string): Color of the bars. Default: '0.5'
            alpha (float):  Transparency of the recession bars. Must be between 0 and 1
                            Default: 0.5

        Returns:
        '''

        peaks =[
        '1857-06-01',
        '1860-10-01',
        '1865-04-01',
        '1869-06-01',
        '1873-10-01',
        '1882-03-01',
        '1887-03-01',
        '1890-07-01',
        '1893-01-01',
        '1895-12-01',
        '1899-06-01',
        '1902-09-01',
        '1907-05-01',
        '1910-01-01',
        '1913-01-01',
        '1918-08-01',
        '1920-01-01',
        '1923-05-01',
        '1926-10-01',
        '1929-08-01',
        '1937-05-01',
        '1945-02-01',
        '1948-11-01',
        '1953-07-01',
        '1957-08-01',
        '1960-04-01',
        '1969-12-01',
        '1973-11-01',
        '1980-01-01',
        '1981-07-01',
        '1990-07-01',
        '2001-03-01',
        '2007-12-01']

        troughs =[
        '1858-12-01',
        '1861-06-01',
        '1867-12-01',
        '1870-12-01',
        '1879-03-01',
        '1885-05-01',
        '1888-04-01',
        '1891-05-01',
        '1894-06-01',
        '1897-06-01',
        '1900-12-01',
        '1904-08-01',
        '1908-06-01',
        '1912-01-01',
        '1914-12-01',
        '1919-03-01',
        '1921-07-01',
        '1924-07-01',
        '1927-11-01',
        '1933-03-01',
        '1938-06-01',
        '1945-10-01',
        '1949-10-01',
        '1954-05-01',
        '1958-04-01',
        '1961-02-01',
        '1970-11-01',
        '1975-03-01',
        '1980-07-01',
        '1982-11-01',
        '1991-03-01',
        '2001-11-01',
        '2009-06-01']

        if len(troughs) < len(peaks):
            today = datetime.date.today()
            troughs.append(str(today))

        T = len(self.data)
        S = len(peaks)

        date_num    = pylab.date2num([dateutil.parser.parse(s) for s in self.dates])
        peaks_num   = pylab.date2num([dateutil.parser.parse(s) for s in peaks])
        troughs_num = pylab.date2num([dateutil.parser.parse(s) for s in troughs])

        datesmin = min(date_num)
        datesmax = max(date_num)
        peaksmin = min(peaks_num)
        peaksax = max(peaks_num)
        troughsmin=min(troughs_num)
        troughsmax=max(troughs_num)
        
        if datesmin <= peaksmin:
            'Nothing to see here'
            min0 = 0
        else:
            'Or here'
            for k in range(S):
                if datesmin <= peaks_num[k]:
                    min0 = k
                    break
                                              
        if datesmax >= troughsmax:
            max0 = len(troughs)-1
        else:
            'Or here'
            for k in range(S):
                if datesmax < troughs_num[k]:
                    max0 = k
                    break

        if datesmax < troughsmax:
            if peaks_num[max0]<datesmax and troughs_num[min0-1]>datesmin:
                peaks2 = peaks[min0:max0]
                peaks2.append(peaks[max0])
                peaks2.insert(0,self.dates[0])
                troughs2 = troughs[min0:max0]
                troughs2.append(self.dates[-1])
                troughs2.insert(0,troughs[min0-1])
            
                peaks2num  = pylab.date2num([dateutil.parser.parse(s) for s in peaks2])
                troughs2num = pylab.date2num([dateutil.parser.parse(s) for s in troughs2])

            elif peaks_num[max0]<datesmax and troughs_num[min0-1]<datesmin:
                peaks2 = peaks[min0:max0]
                peaks2.append(peaks[max0])
                troughs2 = troughs[min0:max0]
                troughs2.append(self.dates[-1])
            
                peaks2num  = pylab.date2num([dateutil.parser.parse(s) for s in peaks2])
                troughs2num = pylab.date2num([dateutil.parser.parse(s) for s in troughs2])

            elif peaks_num[max0]>datesmax and troughs_num[min0]>datesmin:
                peaks2 = peaks[min0:max0]
                peaks2.insert(0,self.dates[0])
                
                troughs2 = troughs[min0:max0]
                troughs2.insert(0,troughs[min0-1])
                
                peaks2num  = pylab.date2num([dateutil.parser.parse(s) for s in peaks2])
                troughs2num = pylab.date2num([dateutil.parser.parse(s) for s in troughs2])


            else:
                peaks2 = peaks[min0:max0+1]
                troughs2 = troughs[min0:max0+1]
                peaks2num  = peaks_num[min0:max0+1]
                troughs2num= troughs_num[min0:max0+1]


        else:
            if peaks_num[max0]>datesmax and troughs_num[min0]>datesmin:
                peaks2 = peaks[min0:max0]
                peaks2.insert(0,self.dates[0])
                troughs2 = troughs[min0:max0]
                troughs2.insert(0,troughs[min0+1])
        
                peaks2num  = pylab.date2num([dateutil.parser.parse(s) for s in peaks2])
                troughs2num = pylab.date2num([dateutil.parser.parse(s) for s in troughs2])

            else:
                peaks2 = peaks[min0:max0+1]
                troughs2 = troughs[min0:max0+1]
                peaks2num  = peaks_num[min0:max0+1]
                troughs2num= troughs_num[min0:max0+1]

        self.pks = peaks2
        self.trs = troughs2
        self.recess_bars = pylab.plot()
        self.peaks = peaks
        
        for k in range(len(peaks2)):
            pylab.axvspan(peaks2num[k], troughs2num[k], edgecolor= color, facecolor=color, alpha=alpha)

    def times(self,series2):

        '''Multiplies the data from the current fredpy series with the data from series2.

        Args:
            series2 (fredpy series): A fredpy series

        Note::
            Both series must have exactly the same date attribute. You are 
            responsibile for making sure that adding the series makes sense.
            E.g., this function will not stop you from adding a series with 
            units in dollars to another with units with hours.

        Returns:
            fredpy series
        '''

        if self.dates != series2.dates:

            raise ValueError('Current series and series2 do not have the same observation dates')

        else:

            new_series = series()

            new_series.title = self.title +' times '+series2.title
            if self.source == series2.source:
                new_series.source = self.source
            else:
                new_series.source = self.source +' and '+series2.source
            new_series.frequency = self.frequency
            new_series.frequency_short = self.frequency_short
            new_series.units = self.units +' x '+series2.units
            new_series.units_short = self.units_short +' x '+series2.units_short
            new_series.t = self.t
            new_series.daterange = self.daterange

            if self.seasonal_adjustment == series2.seasonal_adjustment:
                new_series.seasonal_adjustment = self.seasonal_adjustment
                new_series.seasonal_adjustment_short = self.seasonal_adjustment_short
            else:
                new_series.seasonal_adjustment = self.seasonal_adjustment +' and '+series2.seasonal_adjustment
                new_series.seasonal_adjustment_short = self.seasonal_adjustment_short +' and '+series2.seasonal_adjustment_short

            if self.last_updated == series2.last_updated:
                new_series.last_updated = self.last_updated
            else:
                new_series.last_updated = self.last_updated +' and '+series2.last_updated

            if self.release == series2.release:
                new_series.release = self.release
            else:
                new_series.release = self.release +' and '+series2.release
                
            new_series.series_id = self.series_id +' and '+series2.series_id
            new_series.data  = self.data*series2.data
            new_series.dates = self.dates
            new_series.datetimes = self.datetimes


            return new_series


    def window(self,win):

        '''Restricts the data to a specified date window.

        Args:

            win (list): is an ordered pair: win = [win_min, win_max]

                            win_min is the date of the minimum date
                            win_max is the date of the maximum date
        
                        both are strings in either 'yyyy-mm-dd' or 'mm-dd-yyyy' format

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        T = len(self.data)
        win_min = win[0]
        win_max = win[1]
        win_min_num = pylab.date2num(dateutil.parser.parse(win_min))
        win_max_num = pylab.date2num(dateutil.parser.parse(win_max))
        date_num    = pylab.date2num([dateutil.parser.parse(s) for s in self.dates])
        dumpy       = date_num.tolist()
        min0 = 0
        max0 = T
        t = self.t

        if win_min_num > min(date_num):
            for k in range(T):
                if win_min_num <= dumpy[k]:
                    min0 = k
                    break
                                              
        if win_max_num < max(date_num):
            for k in range(T):
                if win_max_num < dumpy[k]:
                    max0 = k
                    break

        new_series.data = new_series.data[min0:max0]
        new_series.dates = new_series.dates[min0:max0]
        new_series.datetimes = np.array([dateutil.parser.parse(s) for s in new_series.dates])
        if len(self.dates)>0:
            new_series.daterange = 'Range: '+new_series.dates[0]+' to '+new_series.dates[-1]
        else:
            new_series.daterange = 'Range: Null'

        if hasattr(self, 'cycle'):
            new_series.cycle = self.cycle[min0:max0]

        if hasattr(self, 'trend'):
            new_series.trend = self.trend[min0:max0]

        return new_series

######################################################################################################
# Additional functions

def date_times(date_strings):

    '''Converts a list of date strings in 'yyyy-mm-dd' format to a list of datetime-formatted objects.

    Args:
        date_strings (list): a list of date strings formated as: 'yyyy-mm-dd'.

    Returns:
        numpy ndarray
    '''

    datetimes = np.array([dateutil.parser.parse(s) for s in date_strings])
    return datetimes

def divide(series1,series2):

    '''Divides the data from the series1 by the data from series2.

    Args:
        series2 (fredpy series): A fredpy series

    Note::
        Both series must have exactly the same date attribute. You are 
        responsibile for making sure that adding the series makes sense.
        E.g., this function will not stop you from adding a series with 
        units in dollars to another with units in hours.

    Returns:
        fredpy series
    '''

    if series1.dates != series2.dates:

        raise ValueError('series1 and series2 do not have the same observation dates')

    else:

        new_series = series()

        new_series.title = series1.title +' divided by '+series2.title
        if series1.source == series2.source:
            new_series.source = series1.source
        else:
            new_series.source = series1.source +' and '+series2.source
        new_series.frequency = series1.frequency
        new_series.frequency_short = series1.frequency_short
        new_series.units = series1.units +' / '+series2.units
        new_series.units_short = series1.units_short +' / '+series2.units_short
        new_series.t = series1.t
        new_series.daterange = series1.daterange

        if series1.seasonal_adjustment == series2.seasonal_adjustment:
            new_series.seasonal_adjustment = series1.seasonal_adjustment
            new_series.seasonal_adjustment_short = series1.seasonal_adjustment_short
        else:
            new_series.seasonal_adjustment = series1.seasonal_adjustment +' and '+series2.seasonal_adjustment
            new_series.seasonal_adjustment_short = series1.seasonal_adjustment_short +' and '+series2.seasonal_adjustment_short

        if series1.last_updated == series2.last_updated:
            new_series.last_updated = series1.last_updated
        else:
            new_series.last_updated = series1.last_updated +' and '+series2.last_updated

        if series1.release == series2.release:
            new_series.release = series1.release
        else:
            new_series.release = series1.release +' and '+series2.release
            
        new_series.series_id = series1.series_id +' and '+series2.series_id
        new_series.data  = series1.data/series2.data
        new_series.dates = series1.dates
        new_series.datetimes = series1.datetimes


        return new_series

def minus(series1,series2):

    '''Subtracts the data from series2 from the data from series1.

    Args:
        series2 (fredpy series): A fredpy series

    Note::
        Both series must have exactly the same date attribute. You are 
        responsibile for making sure that adding the series makes sense.
        E.g., this function will not stop you from adding a series with 
        units in dollars to another with units in hours.

    Returns:
        fredpy series
    '''

    if series1.dates != series2.dates:

        raise ValueError('series1 and series2 do not have the same observation dates')

    else:

        new_series = series()

        new_series.title = series1.title +' minus '+series2.title
        if series1.source == series2.source:
            new_series.source = series1.source
        else:
            new_series.source = series1.source +' and '+series2.source
        new_series.frequency = series1.frequency
        new_series.frequency_short = series1.frequency_short
        new_series.units = series1.units +' - '+series2.units
        new_series.units_short = series1.units_short +' - '+series2.units_short
        new_series.t = series1.t
        new_series.daterange = series1.daterange

        if series1.seasonal_adjustment == series2.seasonal_adjustment:
            new_series.seasonal_adjustment = series1.seasonal_adjustment
            new_series.seasonal_adjustment_short = series1.seasonal_adjustment_short
        else:
            new_series.seasonal_adjustment = series1.seasonal_adjustment +' and '+series2.seasonal_adjustment
            new_series.seasonal_adjustment_short = series1.seasonal_adjustment_short +' and '+series2.seasonal_adjustment_short

        if series1.last_updated == series2.last_updated:
            new_series.last_updated = series1.last_updated
        else:
            new_series.last_updated = series1.last_updated +' and '+series2.last_updated

        if series1.release == series2.release:
            new_series.release = series1.release
        else:
            new_series.release = series1.release +' and '+series2.release
            
        new_series.series_id = series1.series_id +' and '+series2.series_id
        new_series.data  = series1.data-series2.data
        new_series.dates = series1.dates
        new_series.datetimes = series1.datetimes


        return new_series


def plus(series1,series2):

    '''Adds the data from series1 to the data from series2.

    Args:
        series2 (fredpy series): A fredpy series

    Note::
        Both series must have exactly the same date attribute. You are 
        responsibile for making sure that adding the series makes sense.
        E.g., this function will not stop you from adding a series with 
        units in dollars to another with units in hours.

    Returns:
        fredpy series
    '''

    if series1.dates != series2.dates:

        raise ValueError('series1 and series2 do not have the same observation dates')

    else:

        new_series = series()

        new_series.title = series1.title +' plus '+series2.title
        if series1.source == series2.source:
            new_series.source = series1.source
        else:
            new_series.source = series1.source +' and '+series2.source
        new_series.frequency = series1.frequency
        new_series.frequency_short = series1.frequency_short
        new_series.units = series1.units +' + '+series2.units
        new_series.units_short = series1.units_short +' + '+series2.units_short
        new_series.t = series1.t
        new_series.daterange = series1.daterange

        if series1.seasonal_adjustment == series2.seasonal_adjustment:
            new_series.seasonal_adjustment = series1.seasonal_adjustment
            new_series.seasonal_adjustment_short = series1.seasonal_adjustment_short
        else:
            new_series.seasonal_adjustment = series1.seasonal_adjustment +' and '+series2.seasonal_adjustment
            new_series.seasonal_adjustment_short = series1.seasonal_adjustment_short +' and '+series2.seasonal_adjustment_short

        if series1.last_updated == series2.last_updated:
            new_series.last_updated = series1.last_updated
        else:
            new_series.last_updated = series1.last_updated +' and '+series2.last_updated

        if series1.release == series2.release:
            new_series.release = series1.release
        else:
            new_series.release = series1.release +' and '+series2.release
            
        new_series.series_id = series1.series_id +' and '+series2.series_id
        new_series.data  = series1.data+series2.data
        new_series.dates = series1.dates
        new_series.datetimes = series1.datetimes


        return new_series


def quickplot(fred_series,year_mult=10,show=True,recess=False,style='default',save=False,filename='file',linewidth=2,alpha = 0.7):

    '''Create a plot of a FRED data series.

    Args:
        fred_series (fredpy.series): A ``fredpy.series`` object.
        year_mult (integer):         Interval between year ticks on the x-axis. Default: 10.
        show (bool):                 Show the plot? Default: True.
        recess (bool):               Show recession bars in plot? Default: False.
        style (string):              Matplotlib style Default: 'default'.
        save (bool):                 Save the image to file? Default: False.
        filename (string):           Name of file to which image is saved *without an extension*.
                                     Default: ``'file'``.
        linewidth (float):           Width of plotted line. Default: 2.
        alpha (float):               Transparency of the recession bars. Must be between 0 and 1. 
                                     Default: 0.7

    Returns:
    '''

    pylab.style.use(style)

    fig = pylab.figure()

    years  = pylab.YearLocator(year_mult)
    ax = fig.add_subplot(111)
    ax.plot_date(fred_series.datetimes,fred_series.data,'b-',lw=linewidth,alpha = alpha)
    ax.xaxis.set_major_locator(years)
    ax.set_title(fred_series.title)
    ax.set_ylabel(fred_series.units)
    fig.autofmt_xdate()
    if recess != False:
        fred_series.recessions()
    ax.grid(True)
    if show==True:
        pylab.show()
    if save !=False:
        fullname = filename+'.png'
        fig.savefig(fullname,bbox_inches='tight')

def times(series1,series2):

    '''Multiplies the data from series1 with the data from series2.

    Args:
        series2 (fredpy series): A fredpy series

    Note::
        Both series must have exactly the same date attribute. You are 
        responsibile for making sure that adding the series makes sense.
        E.g., this function will not stop you from adding a series with 
        units in dollars to another with units in hours.

    Returns:
        fredpy series
    '''

    if series1.dates != series2.dates:

        raise ValueError('series1 and series2 do not have the same observation dates')

    else:

        new_series = series()

        new_series.title = series1.title +' times '+series2.title
        if series1.source == series2.source:
            new_series.source = series1.source
        else:
            new_series.source = series1.source +' and '+series2.source
        new_series.frequency = series1.frequency
        new_series.frequency_short = series1.frequency_short
        new_series.units = series1.units +' * '+series2.units
        new_series.units_short = series1.units_short +' * '+series2.units_short
        new_series.t = series1.t
        new_series.daterange = series1.daterange

        if series1.seasonal_adjustment == series2.seasonal_adjustment:
            new_series.seasonal_adjustment = series1.seasonal_adjustment
            new_series.seasonal_adjustment_short = series1.seasonal_adjustment_short
        else:
            new_series.seasonal_adjustment = series1.seasonal_adjustment +' and '+series2.seasonal_adjustment
            new_series.seasonal_adjustment_short = series1.seasonal_adjustment_short +' and '+series2.seasonal_adjustment_short

        if series1.last_updated == series2.last_updated:
            new_series.last_updated = series1.last_updated
        else:
            new_series.last_updated = series1.last_updated +' and '+series2.last_updated

        if series1.release == series2.release:
            new_series.release = series1.release
        else:
            new_series.release = series1.release +' and '+series2.release
            
        new_series.series_id = series1.series_id +' and '+series2.series_id
        new_series.data  = series1.data*series2.data
        new_series.dates = series1.dates
        new_series.datetimes = series1.datetimes


        return new_series

def toFredSeries(data,dates,frequency='',frequency_short='',last_updated='',notes='',release='',seasonal_adjustment='',seasonal_adjustment_short='',series_id='',source='',t=0,title='',units='',units_short=''):
    
    '''Create a FRED object from a set of data obtained from a different source.

    Args:
        data (numpy ndarray):                   Data
        dates (list or numpy ndarray):          Elements must be strings in 'MM-DD-YYYY' format
        frequency (string):                     Observation frequency. Options: '', 'Daily', 'Weekly', 'Monthly', 'Quarterly', or 'Annual'. Default: ''
        frequency_short (string):               Observation frequency abbreviated. Options: '', 'D', 'W', 'M', 'Q', or 'A'. Default: ''
        last_updated (string):                  Date data was last updated. Default = ''
        notes (string):                         Default: ''
        release (string):                       Notes about data. Default: ''
        seasonal_adjustment (string):           Default: ''
        seasonal_adjustment_short (string):     Default: ''
        series_id (string):                     FRED series ID. Default: ''
        source (string):                        Original source of data. Default: ''
        t (int):                                Number of observations per year. Default: 0
        title (string):                         Title of the data. Default: ''
        units (string):                         Default: ''
        units_short (string):                   Default: ''
        '''
    

    f = series()
    f.data = np.array(data)

    timestamps = pd.DatetimeIndex(dates)    
    f.dates = [ str(d.to_pydatetime())[0:10] for d in timestamps]
    f.datetimes = np.array([dateutil.parser.parse(s) for s in f.dates])



    if frequency in ['Daily','Weekly','Monthly','Quarterly','Annual']:

        if frequency == 'Daily':
            t=365
            frequency_short = 'D'
        elif frequency == 'Weekly':
            t=52
            frequency_short = 'W'
        elif frequency == 'Monthly':
            t=12
            frequency_short = 'M'
        elif frequency == 'Quarterly':
            t=4
            frequency_short = 'Q'
        else:
            t=1
            frequency_short = 'A'

    elif frequency_short in ['D','W','M','Q','A']:

        if frequency_short == 'D':
            t=365
            frequency = 'Daily'
        elif frequency_short == 'W':
            t=52
            frequency = 'Weekly'
        elif frequency_short == 'M':
            t=12
            frequency = 'Monthly'
        elif frequency_short == 'Q':
            t=4
            frequency = 'Quarterly'
        else:
            t=1
            frequency = 'Annual'



    f.frequency = frequency
    f.frequency_short = frequency_short
    f.last_updated = last_updated
    f.notes = notes
    f.release = release
    f.seasonal_adjustment = seasonal_adjustment
    f.seasonal_adjustment_short = seasonal_adjustment_short
    f.series_id = series_id
    f.source = source
    f.title = title
    f.units = units
    f.units_short = units_short
    f.t = t
    f.daterange = 'Range: '+f.dates[0]+' to '+f.dates[-1]
    return f


def window_equalize(series_list):

    '''Adjusts the date windows for a collection of fredpy.series objects to the smallest common window.

    Args:
        series_list (list): A list of fredpy.series objects

    Returns:
    '''

    new_list = []

    minimums = [ k.datetimes[0].date() for k in series_list]
    maximums = [ k.datetimes[-1].date() for k in series_list]
    win_min =  max(minimums).strftime('%Y-%m-%d')
    win_max =  min(maximums).strftime('%Y-%m-%d')
    windo = [win_min,win_max]
    for x in series_list:
        new_list.append(x.window(windo))

    return new_list