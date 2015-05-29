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

            path = os.path.join(os.path.dirname(__file__), 'templates/index-beta.html')
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
            
            path = os.path.join(os.path.dirname(__file__), 'templates/upload.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
application = webapp.WSGIApplication([
                                      ('/', MainPage),
                                      ('/upload-form-ajax', CreateUploadUrl),
                                      ('/upload-page', UploadPage),
                                      ('/upload', UploadHandler)
                                    ], debug=True)
def main():
    run_wsgi_app(application)
if __name__ == "__main__":
    main()
