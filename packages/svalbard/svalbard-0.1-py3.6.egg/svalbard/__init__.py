name='svalbard'

from datetime import datetime,timedelta

somedatetimeformats=[
    '%Y%m%d%H',
    '%Y%m%d%H',
    '%Y%m%d %H',
    '%Y%m%d%H%M',
    '%Y%m%d%H%M%S',
    '%Y-%m-%d %H',
    '%Y-%m-%d',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%d %H%M%SZ',
    '%m-%d-%Y %H:%M:%S'
]

def guess_forecast_datetime_from_string(s,datetimeformats=somedatetimeformats,verbose=False):
  from datetime import datetime
  results=[]
  for i,fmt in enumerate(datetimeformats):
    if verbose:
      print("Trying",fmt)
    try:
      dt=datetime.strptime(s,fmt)
      results.append((i,fmt,dt))
    except Exception as e:
      if verbose:
        print (e)
  return results

class ForecastTime(object):
  """
    ForecastTime integrates the concept of two central notions of time in a weather forecasting scenario.
    anatime is the time when a numerical weather prediction model is initialized.
    validtime is the time when the weather forecast is to be validated towards observations.
    Between these times is a time interval which ForecastTime keeps track of in seconds, but
    since hours is a more common time unit the interface of this time interval is given in hours
    fchours denotes that time interval.
    The time stamps are time zone naive.
  """
  def __init__(self,anatime=False,validtime=False,fchours=False,fcminutes=False,datetimeformats=somedatetimeformats):
    self._datetimeformats=datetimeformats
    if type(anatime) is not bool:
      self.set_anatime(anatime)
    if type(validtime) is not bool:
      self.set_validtime(validtime)
    if type(fchours) is not bool:
      self.set_fchours(int(fchours))
  def get_anatime(self):
    return self._anatime
  def set_anatime(self,value,keep_validtime=True):
    if type(value) == str:
      dt = guess_forecast_datetime_from_string(value,self._datetimeformats)[0][2]
    elif type(value) == datetime:
      dt=value
    self._anatime=dt
    if keep_validtime:
      if hasattr(self,'_validtime'):
        self._fc_seconds = ( self._validtime - self._anatime ).total_seconds()
    else:
      if hasattr(self._fc_seconds):
        self._validtime = self._anatime + self._fc_seconds
  anatime = property(get_anatime,set_anatime)
  def get_validtime(self):
    if hasattr(self,'_validtime'):
      return self._validtime
    elif hasattr(self,'_anatime') and hasattr(self,'_fc_seconds'):
      self._validtime = self._anatime + timedelta(seconds=self._fc_seconds)
      return self._validtime
    else:
      raise Exception('validtime is undetermined')
  def set_validtime(self,value,keep_anatime=True):
    if type(value) == str:
      dt = guess_forecast_datetime_from_string(value,self._datetimeformats)[0][2]
    elif type(value) == datetime:
      dt=value
    self._validtime=dt
    if keep_anatime:
      if hasattr(self,'_anatime'):
        self._fc_seconds = (self._validtime - self._anatime ).total_seconds()
    else:
      if hasattr(self,'_fc_seconds'):
        self._anatime = self._validtime - self._fc_seconds
  validtime = property(get_validtime,set_validtime)
  def get_fchours(self):
    if hasattr(self,'_fc_seconds'):
      return int( self._fc_seconds / 3600 )
    elif hasattr(self,'_anatime') and hasattr(self,'_validtime'):
      self._fc_seconds=int((self._validtime - self._anatime).total_seconds())
      return int(self._fc_seconds / 3600)
  def set_fchours(self,value,keep_anatime=True):
    self._fc_seconds = int(value * 3600)
    if keep_anatime:  
      if hasattr(self,'_anatime'):
        self._validtime = self._anatime + timedelta(seconds=self._fc_seconds)
    else:
      if hasattr(self,'_validtime'):
        self._anatime = self._validtime - timedelta(seconds=self._fc_seconds)
  fchours = property(get_fchours,set_fchours)
  def get_dict(self):
    return {'anatime':self.get_anatime(),'validtime':self.get_validtime(),'fchours':self.get_fchours()}
  def __repr__(self):
    pretty=['ForecastTime']
    if hasattr(self,'_anatime'):
      pretty.append(f'anatime:{self.get_anatime()}')
    if hasattr(self,'_validtime'):
      pretty.append(f'validtime:{self.get_validtime()}')
    if hasattr(self,'_fc_seconds'):
      pretty.append(f'fchours:{self.get_fchours()}')
    return ','.join(pretty)
