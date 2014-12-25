# -*- coding: utf-8 -*- 
from google.appengine.ext import ndb
from google.appengine.api import users

PUBLIC_YN=(('Y', 'Y'), ('N', 'N'))
YN=(('Y', 'Y'), ('N', 'N'))
CLASS_TYPE=(('Theory', 'T'), ('Seminar', 'S'))
HOURS=(('1,2', '1,2'), ('3,4', '3,4'), ('5,6', '5,6'), ('7,8', '7,8'), ('9,10', '9,10'), ('11,12', '11,12'), ('13,14,15', '13,14,15'))

class Student(ndb.Model):
    user=ndb.UserProperty(auto_current_user_add=True, required=True)
    name=ndb.StringProperty(required=False)
    student_class=ndb.StringProperty(required=True)
    course=ndb.StringProperty(required=False)
    alias=ndb.StringProperty(required=False)
    email=ndb.StringProperty(required=False)
    mobile_phone=ndb.StringProperty(required=False)
    telephone=ndb.StringProperty(required=False)
    code=ndb.StringProperty(required=True)
    birthday=ndb.DateProperty(required=False)
    block=ndb.BooleanProperty(default=False)
    activated=ndb.BooleanProperty(default=True)
    created_time=ndb.DateTimeProperty(auto_now_add=True, required=True)
    def __unicode__(self):
        return self.code
    @staticmethod
    def get_by_user():
        res= Student.query().filter(ndb.UserProperty("user")==users.get_current_user())
        if not res:
            return None
        return res.get()
    @staticmethod
    def get_or_create_by_user():
        res=Student.query().filter(ndb.UserProperty("user")==users.get_current_user())
        if not res or not res.get():
            student=Student()
            student.user=users.get_current_user()
            return student
        return res.get()
    @staticmethod
    def get_by_code(code):
        res=Student.query().filter(ndb.StringProperty("code")==code)
        if res==None:
            return None
        return res.get()
class Subject(ndb.Model):
    subject_code=ndb.StringProperty(required=False)
    subject_name=ndb.StringProperty(required=False)
    subject_short_name=ndb.StringProperty(required=False)
    created_time=ndb.DateTimeProperty(auto_now_add=True, required=True)
    public=ndb.StringProperty(default='Y')
    course_credit=ndb.IntegerProperty(default=2, required=False)
    speciality=ndb.StringProperty(required=False)
    description=ndb.StringProperty( required=False)
    activated=ndb.BooleanProperty(default=True)
    def __unicode__(self):
        if self.subject_short_name:
            return self.subject_short_name
        return self.subject_code
    def get_name(self):
        if self.subject_short_name:
            return self.subject_short_name
        return self.subject_name
    @staticmethod
    def get_by_code(code):
        res=Subject.query().filter(ndb.StringProperty("subject_code")==code)
        if not res or not res.get():
            return None
        return res.get()
    @staticmethod
    def get_or_create_by_code(code):
        res=Subject.query().filter(ndb.StringProperty("subject_code")==code)
        if not res or not res.get():
            subject=Subject()
            subject.subject_code=code
            return subject
        return res.get()   
class TimeTable(ndb.Model):
    random_key=ndb.StringProperty()
    student=ndb.KeyProperty(kind="Student")
    year=ndb.StringProperty(required=False)
    semester=ndb.StringProperty(required=False)
    used=ndb.BooleanProperty(default=False)
    created_time=ndb.DateTimeProperty(auto_now_add=True, required=False)
    activated=ndb.BooleanProperty(default=True)
    def __unicode__(self):
        return self.student.__str__()
class SubjectClass(ndb.Model):
    subject=ndb.KeyProperty(kind="Subject")
    timeTable=ndb.KeyProperty(kind="TimeTable")
    theory_class=ndb.StringProperty(required=True)
    seminar_class=ndb.StringProperty(required=False)
    start_date=ndb.DateTimeProperty(required=False)
    end_date=ndb.DateTimeProperty(required=False)
    def __unicode__(self):
        return self.subject.__str__()
class SubjectStudyDay(ndb.Model):
    subject_class=ndb.KeyProperty(kind="SubjectClass")
    day_name=ndb.StringProperty(required=False)
    day_hours=ndb.StringProperty(required=False)
    day_location=ndb.StringProperty(required=False)
    class_type=ndb.StringProperty(required=False)
