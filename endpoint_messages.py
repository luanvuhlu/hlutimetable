# -*- coding: utf-8 -*- 
'''
Created on Jan 1, 2015

@author: luanvu
'''
from protorpc import messages, message_types
package = 'TimeTable'

class StudentResponse(messages.Message):
    name=messages.StringField(1)
    student_class=messages.StringField(2)
    course=messages.StringField(3)
    alias=messages.StringField(4)
    email=messages.StringField(5)
    mobile_phone=messages.StringField(6)
    telephone=messages.StringField(7)
    code=messages.StringField(8)
class SubjectStudyDayResponse(messages.Message):
    day_name=messages.StringField(1)
    day_hours=messages.StringField(2)
    day_location=messages.StringField(3)
    class_type=messages.StringField(4)
class SubjectResponse(messages.Message):
    subject_code=messages.StringField(1)
    subject_name=messages.StringField(2)
    subject_short_name=messages.StringField(3)
    course_credit=messages.IntegerField(6, default=2)
    speciality=messages.StringField(7)
class SubjectClassResponse(messages.Message):
    subject=messages.MessageField(SubjectResponse, 1)
    subject_study_day=messages.MessageField(SubjectStudyDayResponse,2, repeated=True)
    theory_class=messages.StringField(3)
    seminar_class=messages.StringField(4)
    start_date=message_types.DateTimeField(5)
    end_date=message_types.DateTimeField(6)

class TimeTableResponse(messages.Message):
    student=messages.MessageField(StudentResponse, 1)
    year = messages.StringField(2)
    semester = messages.StringField(3)
    subject_class=messages.MessageField(SubjectClassResponse, 4, repeated=True)
class TimeTableRequest(messages.Message):
    rdkey = messages.StringField(1)