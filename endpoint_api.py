# -*- coding: utf-8 -*- 
'''
Created on Jan 1, 2015

@author: luanvu
'''
import endpoints
from protorpc import messages
from protorpc import remote
from models import TimeTable
from google.appengine.ext import ndb
from endpoint_messages import TimeTableRequest, TimeTableResponse
package = 'TimeTable'


@endpoints.api(name='timetable', version='v1')
class TimeTableApi(remote.Service):
    """TimeTable API v1."""
    @endpoints.method(TimeTableRequest, TimeTableResponse,
                      path='timetablesv/{rdkey}', http_method='GET',
                      name='timetable.getTimeTable')
    def get_timetable(self, request):
        random_key=request.rdkey
        res=TimeTable.query().filter(
                                     ndb.StringProperty("random_key")==random_key, 
                                     ndb.BooleanProperty("activated")==True)
        if res:
            timetable=res.get()
            timetable.used=True
            timetable.put()
            msg=timetable.to_message()
            
            return msg
        raise endpoints.NotFoundException('Random key is wrong')

APPLICATION = endpoints.api_server([TimeTableApi], restricted=False)