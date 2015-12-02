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
from uploadhandler import CreateUploadUrl, UploadHandler

BASE_PATH = os.path.dirname(__file__)

class MainPage(webapp.RequestHandler): 
    def get(self):
        user = users.get_current_user()
        if user:
            # Hien tai cho redirect thang sang trnag upload page
#             self.redirect('/upload-page', True)
            random_key=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
            template_values = {
            'user':user,
            'random_key':random_key,
            'nickname': user.nickname(),
            'login_url': users.create_logout_url("/"),
            'is_admin': users.is_current_user_admin()
            }

            path = os.path.join(BASE_PATH, 'templates/index.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
class About(webapp.RequestHandler):
    def get(self, *args):
        path = os.path.join(BASE_PATH, 'templates/index.html')
        self.response.out.write(template.render(path, []))
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
            
            path = os.path.join(BASE_PATH, 'templates/upload.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
class ViewInfo(webapp.RequestHandler):
    def get(self):
        path =  os.path.join(BASE_PATH, 'templates/view_info.html')
        self.response.out.write(template.render(path, {}))
class Structure(webapp.RequestHandler):
    def get(self, *args):
        path =  os.path.join(BASE_PATH, 'templates/structure.html')
        self.response.out.write(template.render(path, {}))
class MarkTest(webapp.RequestHandler):
    def get(self, *args):
        filePath =  'templates/mark_test.html'
        if self.request.get('t') == "c":
            filePath = 'templates/condition_test.html'
        elif self.request.get('t') == "m":
            filePath = 'templates/mark_test.html'
        self.response.out.write(template.render(os.path.join(BASE_PATH, filePath), {}))
application = webapp.WSGIApplication([
                                    ('/', About),
                                      # Tạm thời ẩn đi
#                                       ('/upload-page', UploadPage),
                                      ('/ViewInfo', ViewInfo),
                                      ('/structure', Structure),
                                      ('/test', MarkTest),
                                      # Ajax
                                      ('/upload', UploadHandler),
                                      ('/upload-form-ajax', CreateUploadUrl)
                                    ], debug=True)
def main():
    run_wsgi_app(application)
if __name__ == "__main__":
    main()
