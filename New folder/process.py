import datetime
import os
import sys
import smtplib
import requests

def check_system(): 
    
    if check_date:
        return True
    else:
        
        return False

file_path='D:/RAJA/my creation/backup/image encrypt & decrypt using aes styles/app.py'



start_date_str = "2023-06-10"  
end_date_str = "2024-06-30"    

start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

current_date = datetime.date.today()

def check(current_date,start_date,end_date):
    if current_date >= start_date and current_date <= end_date:        
        return True
    else:       
        return False


      
check_date=check(current_date,start_date,end_date)


system=check_system()

