# -*- coding: utf-8 -*- 
from data import TimeTableFile
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.api import users
from google.appengine.ext import webapp
from models import Student, TimeTable, Subject, SubjectClass, SubjectStudyDay
import os
import random
import string
import logging


class CreateUploadUrl(webapp.RequestHandler):
    def get(self):
        self.response.out.write(blobstore.create_upload_url('/upload'))
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        timetable_ett=parse_timetable(upload_files[0])
        if not timetable_ett:
            self.response.out.write("Không đọc được dữ liệu")
            return
        random_key=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
        student=Student.get_or_create_by_user()
        if not student.key:
            student.populate(code=timetable_ett.student_code, 
                         name=timetable_ett.student_name, 
                         student_class=timetable_ett.student_class)
            student.put()
        timetable=TimeTable()
        timetable.populate(random_key=random_key,
                           student=student.key)
        list_subject_class=[]
        for sub in timetable_ett.subjects:
            list_day=[]
            subject=Subject.get_or_create_by_code(sub['code'])
            if not subject.key:
                subject.populate(subject_name=sub['name'])
                subject.put()
            subject_class=SubjectClass()
            subject_class.populate(subject=subject.key,
#                                   timeTable=timetable.key,
                                  theory_class=sub['theory'],
                                  seminar_class=sub['seminar'],
                                  start_date=sub['start'],
                                  end_date=sub['end']
                                  
                                  )
            if sub['day_theories']:
                for d in sub['day_theories']:
                    day=SubjectStudyDay()
                    day.populate(
#                                  subject_class=subject_class.key,
                                 day_name=d['number'],
                                 day_hours="%s-%s" % (d['start'], d['end']),
                                 day_location="%s-%s" % (d['location'], d['room']),
                                 class_type='T')
                    day.put()
                    list_day.append(day.key)
            if sub['day_seminars']:
                for d in sub['day_seminars']:
                    day=SubjectStudyDay()
                    day.populate(
#                                  subject_class=subject_class.key,
                                 day_name=d['number'],
                                 day_hours="%s-%s" % (d['start'], d['end']),
                                 day_location="%s-%s" % (d['location'], d['room']),
                                 class_type='S')
                    day.put()
                    list_day.append(day.key)
            subject_class.subject_study_day=list_day
            subject_class.put()
            list_subject_class.append(subject_class.key)
        timetable.subject_class=list_subject_class
        timetable.put()
        self.response.out.write(random_key);

def parse_timetable(blob_info):
    f=blob_info.open()
    timetable=TimeTableFile(f.read())
    f.close()
    blob_info.delete()
    if not timetable:
        logging.error("Không đọc được dữ liệu")
        return None
    if not timetable.student_class:
        logging.error("Không tìm thấy lớp")
        return None
    if not timetable.student_code:
        logging.error("Không tìm thấy mã sinh viên")
        return None
    if not timetable.student_name:
        logging.error("Không tìm thấy tên sinh viên")
        return None
    if not timetable.subjects:
        logging.error("Không tìm thấy môn nào cả")
        return None
    return timetable
