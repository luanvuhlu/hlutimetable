# -*- coding: utf-8 -*- 
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
import random
import string
from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from uploadhandler import parse_timetable
from models import Student, TimeTable, Subject, SubjectClass, SubjectStudyDay
import rest



class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            random_key=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
            template_values = {
            'user':user,
            'random_key':random_key,
            'nickname': user.nickname(),
            'login_url': users.create_logout_url("/"),
            'is_admin': users.is_current_user_admin()
            }

            path = os.path.join(os.path.dirname(__file__), 'index.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
class UploadPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        random_key=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
        if user:
            upload_url = blobstore.create_upload_url('/upload')
            template_values = {
            'user':user,
            'random_key':random_key,
            'upload_url':upload_url,
            'nickname': user.nickname(),
            'login_url': users.create_logout_url("/"),
            'is_admin': users.is_current_user_admin()
            }
            
            path = os.path.join(os.path.dirname(__file__), 'upload.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
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
        timetable.put()
        for sub in timetable_ett.subjects:
            subject=Subject.get_or_create_by_code(sub['code'])
            if not subject.key:
                subject.populate(subject_name=sub['name'])
                subject.put()
            subject_class=SubjectClass()
            subject_class.populate(subject=subject.key,
                                  timeTable=timetable.key,
                                  theory_class=sub['theory'],
                                  seminar_class=sub['seminar']
                                  )
            subject_class.put()
            if sub['day_theories']:
                for d in sub['day_theories']:
                    day=SubjectStudyDay()
                    day.populate(subject_class=subject_class.key,
                                 day_name=d['number'],
                                 day_hours="%s-%s" % (d['start'], d['end']),
                                 day_location="%s-%s" % (d['location'], d['room']),
                                 class_type='T')
                    day.put()
            if sub['day_seminars']:
                for d in sub['day_seminars']:
                    day=SubjectStudyDay()
                    day.populate(subject_class=subject_class.key,
                                 day_name=d['number'],
                                 day_hours="%s-%s" % (d['start'], d['end']),
                                 day_location="%s-%s" % (d['location'], d['room']),
                                 class_type='S')
                    day.put()
        self.response.out.write(random_key);
application = webapp.WSGIApplication([
                                      ('/', MainPage),
                                      ('/upload-form-ajax', CreateUploadUrl),
                                      ('/upload-page', UploadPage),
                                      ('/upload', UploadHandler),
                                      ('/rest/.*', rest.Dispatcher)
                                    ], debug=True)

# configure the rest dispatcher to know what prefix to expect on request urls
rest.Dispatcher.base_url = "/rest"

# add specific models (with given names) and restrict the supported methods
rest.Dispatcher.add_models({
  'student' : (Student, rest.READ_ONLY_MODEL_METHODS),
  'timetable' : (TimeTable, ['GET_METADATA', 'GET', 'POST', 'PUT']),
  'subject' : (Subject, rest.READ_ONLY_MODEL_METHODS),
  'subject_study_day' : (SubjectStudyDay, rest.READ_ONLY_MODEL_METHODS),
  'subject_class' : (SubjectClass, rest.READ_ONLY_MODEL_METHODS)
             })
def main():
    run_wsgi_app(application)
if __name__ == "__main__":
    main()
