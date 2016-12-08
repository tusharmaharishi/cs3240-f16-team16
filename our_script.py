import django
import os
import sys
import requests
import json

def find_filename(file_name):
    return os.path.basename(file_name)

# Logging in ==============================================================
while True:
    session = requests.session()
    url = "http://localhost:8000/accounts/login/"
    print("\nPlease log in\n")
    username = input("Username: ")
    password = input("Password: ")
    session.get(url)
    token = session.cookies['csrftoken']
    payload = {'username': username, 'password': password, "csrfmiddlewaretoken": token}
    r = session.post(url, data=payload, headers=dict(Referer=url))

#AUTHENTICATING THE USER ================================================                                                                                            
    url2 = "http://localhost:8000/fda_authenticate/"
    session.get(url2)
    token2 = session.cookies['csrftoken']
    payload2 = {"csrfmiddlewaretoken": token2}
    rr2 = session.post(url2, data=payload2, headers=dict(Referer=url2))
    if rr2.text == "is logged in":
        break
    print("User does not exist or wrong credentials. Please try again.")

# obtaining a master list of reports to use                                                                                                                          
master_report_list = []
url = "http://localhost:8000/fetch_all/"
session.get(url)
token = session.cookies['csrftoken']
payload = {"csrfmiddlewaretoken": token}
rr = session.post(url, data=payload, headers=dict(Referer=url))

data = json.loads(rr.text)
if data == "No public reports":
    print("There seems to be no reports")
else:
    master_report_list = data

master = True
while master == True:
    decision = input("\n1: List all viewable reports"
                     "\n2: List specific report""\n3: Terminate\nPlease choose number option: ")

    # grabbing all public reports
    if decision == "1":
        print("\nHere are all viewable reports: ")
        for report in master_report_list:
            print("  ", report[0], "\n     - ", report[1], "\n")

        decision = "2"

    # retrieving the specific report and giving options to download files
    if decision == "2":
            # grabbing the report =====================================================
            t = True
            while t:
                title = input("Which existing report? ")
                for each in master_report_list:
                    if title != each[0]:
                        continue
                    else:
                        t = False
                        break
            url = "http://localhost:8000/fetch/"
            session.get(url)
            token = session.cookies['csrftoken']
            payload = {"title": title, "csrfmiddlewaretoken": token}
            rr = session.post(url, data=payload, headers=dict(Referer=url))
            data = json.loads(rr.text)
            if data == "nothing":
                print("There are no documents attached to this report")
                continue
            else:
                print("\nHere are the files in this report:\n ")
                dictionary = {}
                count = 1
                for document in data:
                    print("  ", count, os.path.basename(document))
                    dictionary[count] = document
                    count += 1

            # grabbing the file to download ===========================================
            go = True
            while go:
                key = input("\nDownload which file? (Choose number or no): ").lower()
                if key.isdigit():
                    file = dictionary[int(key)]
                elif key == "no":
                    print("\n  Returning back to menu")
                    break
                else:
                    continue
                url = "http://localhost:8000/download/"
                session.get(url)
                token = session.cookies['csrftoken']
                payload = {"title": title, "name": file, "csrfmiddlewaretoken": token}
                rr = session.post(url, data=payload, headers=dict(Referer=url))
                if rr.text == "File not found":
                    print("File not Found")
                else:
                    with open(find_filename(file), 'wb') as reader:
                        for chunk in rr:
                            reader.write(chunk)
                    print("\n  Downloaded", os.path.basename(dictionary[int(key)]))

                test = input("\nDownload another file? (Yes or No): ").lower()
                while test != "yes" or test != "no":
                    if test == "yes":
                        break
                    elif test == "no":
                        go = False
                        break
                    else:
                        test = input("  Yes or No please: ")
    if decision == "3":
        break
print("\nTerminated")
