from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
import random
import string
from google.appengine.ext.webapp import template


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

        if user:
            random_key=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))
            template_values = {
            'user':user,
            'random_key':random_key,
            'nickname': user.nickname(),
            'login_url': users.create_logout_url("/"),
            'is_admin': users.is_current_user_admin()
            }

            path = os.path.join(os.path.dirname(__file__), 'upload.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))
class UploadHandler(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        self.response.out.write(self.request.get('file'));
application = webapp.WSGIApplication([
                                      ('/', MainPage),
                                      ('/upload', UploadPage),
                                      ('/upload-file', UploadHandler)
                                    ], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
