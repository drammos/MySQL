# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys,os
sys.path.append(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'lib'))
import pymysql #as db

import gensim
from gensim.parsing.preprocessing import remove_stopwords, STOPWORDS
from gensim.parsing.preprocessing import strip_punctuation


def connection():
    ''' User this function to create your connections '''
    # con = db.connect(
    #     settings.mysql_host, 
    #     settings.mysql_user, 
    #     settings.mysql_passwd, 
    #     settings.mysql_schema)

    con = pymysql.connect(host='localhost', user='root', password='', db = 'sys') 
    return con

# Python3 code to convert tuple 
# into string
def convertTuple(tup):
    str =  ''.join(tup)
    return str
  

def create_ngrams( text, num):
    res = text.split()
    if num == 1:
        return res
    elif num == 2:
        result = []

        for r in range(len(res)-1):
            result.append(res[r] + " " + res[r+1])

        return result
    else:
        result = []
        
        for r in range(len(res)-2):
            result.append(res[r] + " " + res[r+1] + " " + res[r+2])

        return result
    
class Word:
    
    def __init__(self, str, num):
        self.str = str
        self.num = num


def get( w):
    return w.num

def mostcommonsymptoms(vax_name):
    
    # Create a new connection
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()

    cur.execute(f"SELECT v.symptoms FROM vaccination v WHERE (v.vaccines_vax_name = '{vax_name}')")

    #num ngrams for fuctions create_ngrams
    num_ngrams = 1
    #rows where return the cur.execute from select 
    rows = cur.fetchall()
    #list with words
    result = []

    for row in rows:

        #we take the string and all character change in lower after we remove punct and stopwards and finally call 
        #create_ngrams where she create one list with words
        text = convertTuple(row)
        new_text = text.lower()
        new_text = strip_punctuation(new_text)
        new_text = remove_stopwords(new_text)
        res = create_ngrams( new_text, num_ngrams)
        
        #forloop for list res where return the function create_ngrams
        for j in range(len(res)):
            
            i = -1
            for k in range(len(result)):
                if result[k].str == res[j]:
                   i = k 

            if i == -1:
                w = Word( res[j], 1)
                result.append(w)
            else:
                w = result[i]
                w.num +=1
        
    result = sorted( result, key = get)
    result_finally = []
    for i in range(len(result)):
        if i >=15:
            break
        word = result[i]
        result_finally.append(word.str)
    
    print([vax_name] + result_finally)

    return [vax_name] + result_finally


def buildnewblock(blockfloor):
    
   # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    
 
    return [("result",),]

def findnurse(x,y):

    # Create a new connection
    
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    cur.execute(f"SELECT N.Name, N.EmployeeID, (SELECT count( distinct v.patient_SSN) AS num FROM vaccination v WHERE( v.nurse_EmployeeID = N.EmployeeID)) AS NUM_PATIENT_VACCINATION FROM nurse N WHERE( N.EmployeeID IN ( SELECT oc.Nurse FROM on_call oc WHERE (oc.BlockFloor = {x}) GROUP BY oc.Nurse HAVING ( count( distinct oc.BlockCode) = (	SELECT count(*) FROM block bl WHERE (bl.BlockFloor = {x}) ) ) ) AND {y} <= ( SELECT count(distinct ap.Patient) FROM appointment ap WHERE (ap.PrepNurse = N.EmployeeID) ) ) GROUP BY N.Name, N.EmployeeID")

    
    table = cur.fetchall()
    #print because with have ERROR 500

    print([("Nurse", "ID", "Number of patients"),] + list(table) )
    #return
    return [("Nurse", "ID", "Number of patients"),] + list(table)

def patientreport(patientName):
    # Create a new connection
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()
    cur.execute(f"SELECT s.StayEnd, t.Name, t.Cost, ph.Name, n.Name, r.BlockFloor, r.BlockCode FROM patient p,room r,stay s,undergoes u ,treatment t ,physician ph , nurse n WHERE (u.Physician = ph.EmployeeID AND u.AssistingNurse = n.EmployeeID AND u.stay = s.StayID AND u.Treatment = t.Code AND s.Room = r.RoomNumber AND s.Patient = p.SSN AND p.Name = '{patientName}')")
    
    table = cur.fetchall()
    print([("Patient","Physician", "Nurse", "Date of release", "Treatement going on", "Cost", "Room", "Floor", "Block"),] + list(table))
    return [("Patient","Physician", "Nurse", "Date of release", "Treatement going on", "Cost", "Room", "Floor", "Block"),]

<<<<<<< HEAD
# findnurse(1,2)
# patientreport("Nicolas Craig")
mostcommonsymptoms('PFIZER')
=======
findnurse(1,2)
>>>>>>> 1789c8afdbf0d550a2837259773c288f2fa697d5