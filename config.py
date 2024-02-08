import os

basepath=r"C:\Users\c1049033\PycharmProjects\meerkatApp"

tmppath=os.path.join(basepath, "temp")
logpath=os.path.join(basepath, "log")
logofile=os.path.join(basepath, "images", "logo.png")
pngfile=os.path.join(basepath, "images", "geometriclight.jpg")
welcomefile=os.path.join(basepath, "images", "welcome.JPG")
studylog=os.path.join(basepath, "log", "log_studies.txt")
tablelog=os.path.join(basepath, "log", "log_tables.txt")
raptorlog=os.path.join(basepath, "log", "log_raptor.txt")

if not os.path.exists(logpath):
    os.mkdir(logpath)
if not os.path.exists(tmppath):
    os.mkdir(tmppath)

# tmppath=r"C:\Users\c1049033\PycharmProjects\meerkatApp\temp"
# logofile="C:/Users/c1049033/PycharmProjects/meerkatApp/images/logo.png"
# pngfile="C:/Users/c1049033/PycharmProjects/meerkatApp/images/geometriclight.jpg"
# welcomefile="C:/Users/c1049033/PycharmProjects/meerkatApp/images/welcome.JPG"
# logfile="C:\Users\c1049033\PycharmProjects\meerkatApp\log\log.csv"

outcomefields=["OutcomeID",	"OutcomeDescription"]
interventionfields=["InterventionID",	"InterventionDescription"]
conditionfields=["HealthCareConditionID",	"HealthCareConditionDescription"]
studyfields=["CENTRALStudyID","CRGStudyID","ShortName","StatusofStudy","TrialistContactDetails","CENTRALSubmissionStatus","Notes","DateEntered","DateToCENTRAL","DateEdited","Search_Tagged","UDef1","UDef2","UDef3","UDef4","UDef5","ISRCTN","UDef6","UDef7","UDef8","UDef9","UDef10"]
reportfields=["Abstract","Authors","CENTRALReportID","CENTRALSubmissionStatus","CRGReportID","City","CopyStatus","DateEdited","Dateentered","DatetoCENTRAL","DupString","Edition","Editors","Issue","Journal","Language","Medium","Notes","OriginalTitle","Pages","PublicationTypeID","Publisher","ReportNumber","Title","TypeofReportID","UDef1","UDef10","UDef2","UDef3","UDef4","UDef5","UDef6","UDef7","UDef8","UDef9","Volume","Year"]
