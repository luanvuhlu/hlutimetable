# -*- coding: utf-8 -*- 
from data import TimeTableFile
import logging



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
