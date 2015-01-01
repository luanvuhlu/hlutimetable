# -*- coding: utf-8 -*- 
from google.appengine.ext import ndb
from google.appengine.api import users
from endpoint_messages import TimeTableResponse, StudentResponse, SubjectResponse, SubjectClassResponse, SubjectStudyDayResponse
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
    def to_message(self):
        student=StudentResponse(name=self.name,
                                student_class=self.student_class,
                                course=self.course,
                                alias=self.alias,
                                email=self.email,
                                mobile_phone=self.mobile_phone,
                                telephone=self.telephone,
                                code=self.code
                                )
        return student
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
    def to_message(self):
        subject=SubjectResponse(
                                subject_code=self.subject_code,
                                subject_name=self.subject_name,
                                subject_short_name=self.subject_short_name,
                                course_credit=self.course_credit,
                                speciality=self.speciality
                                )
        return subject
class TimeTable(ndb.Model):
    random_key=ndb.StringProperty()
    student=ndb.KeyProperty(kind="Student")
    subject_class=ndb.KeyProperty(kind="SubjectClass", repeated=True)
    year=ndb.StringProperty(required=False)
    semester=ndb.StringProperty(required=False)
    used=ndb.BooleanProperty(default=False)
    created_time=ndb.DateTimeProperty(auto_now_add=True, required=False)
    activated=ndb.BooleanProperty(default=True)
    def __unicode__(self):
        return self.student.__str__()
    def get_subject_messages(self):
        list_subject_classes=[]
        for sub in self.subject_class:
            list_subject_classes.append(sub.get().to_message())
        return list_subject_classes
    def to_message(self):
        student=self.student.get()
        timetable=TimeTableResponse(student=student.to_message(),
                              year=self.year, 
                              semester=self.semester,
                              subject_class=self.get_subject_messages()
                              )
        return timetable
class SubjectClass(ndb.Model):
    subject=ndb.KeyProperty(kind="Subject")
    subject_study_day=ndb.KeyProperty(kind="SubjectStudyDay", repeated=True)
    theory_class=ndb.StringProperty(required=True)
    seminar_class=ndb.StringProperty(required=False)
    start_date=ndb.DateTimeProperty(required=False)
    end_date=ndb.DateTimeProperty(required=False)
    def __unicode__(self):
        return self.subject.__str__()
    def get_day_messages(self):
        list_days=[]
        for day in self.subject_study_day:
            list_days.append(day.get().to_message())
        return list_days
    def to_message(self):
        subject_class=SubjectClassResponse(
                                           subject=self.subject.get().to_message(),
                                           subject_study_day=self.get_day_messages(),
                                           theory_class=self.theory_class,
                                           seminar_class=self.seminar_class,
                                           start_date=self.start_date,
                                           end_date=self.end_date
                                           )
        return subject_class
class SubjectStudyDay(ndb.Model):
    day_name=ndb.StringProperty(required=False)
    day_hours=ndb.StringProperty(required=False)
    day_location=ndb.StringProperty(required=False)
    class_type=ndb.StringProperty(required=False)
    def __unicode__(self):
        return self.day_name
    def to_message(self):
        subject_study_day=SubjectStudyDayResponse(
                                                  day_name=self.day_name,
                                                  day_hours=self.day_location,
                                                  day_location=self.day_location,
                                                  class_type=self.class_type
                                                  )
        return subject_study_day
