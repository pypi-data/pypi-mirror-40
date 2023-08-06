import requests, html, json
from bs4 import BeautifulSoup

s = requests.Session()
root_url = None
previous_url = None

def login(root, sid, pin, security_answer):
    global root_url
    root_url = root
    url = root_url + "/PRODCartridge/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu"
    r = s.get(url)
    cookies = dict(r.cookies)

    referer = url
    url = root_url + "/PRODCartridge/twbkwbis.P_ValLogin"
    headers = {
        "Referer": referer
    }
    data = {
        "sid": sid,
        "PIN": pin
    }
    r = s.post(url, headers=headers, data=data, cookies=cookies)

    referer = url
    url = root_url + "/PRODCartridge/twbkwbis.P_ProcSecurityAnswer"
    headers = {
        "Referer": referer
    }
    data = {
        "RET_CODE": "",
        "SID": sid,
        "QSTN_NUM": 1,
        "answer": security_answer
    }
    r = s.post(url, headers=headers, data=data, cookies=cookies)

    index_of_url = r.text.find("url")
    url = r.text[index_of_url+4:]
    index_of_end = url.find("\"")
    url = url[:index_of_end]
    url = root_url + "" + html.unescape(url)
    r = s.get(url)
    global previous_url
    previous_url = url

def navigate_to(url, headers=None, data=None, cookies=None, method="GET"):
    global previous_url
    referer = previous_url
    s.headers.update({"Referer": referer})
    if method is "GET":
        r = s.get(url, headers=headers, data=data)
    elif method is "POST":
        r = s.post(url, headers=headers, data=data, cookies=cookies)

    previous_url = url
    return r

def get_courses(year, term):
    term_code = year
    if term.strip().lower() == "spring":
        term_code += "01"
    elif term.strip().lower() == "summer":
        term_code += "02"
    else:
        term_code += "03"

    r = navigate_to(root_url + "/PRODCartridge/bwskfshd.P_CrseSchdDetl", method="POST", data={"term_in": term_code})
    soup = BeautifulSoup(r.text, "html.parser")
    return_data = {}

    return_data['total_credits'] = int(float(r.text[r.text.find("Total Credit Hours: ")+len("Total Credit Hours: "):r.text.find("Total Credit Hours: ")+len("Total Credit Hours: ")+6]))

    return_data['courses'] = []
    course_divs = soup.find_all("table", summary="This layout table is used to present the schedule course detail")
    for course_div in course_divs:
        course = {}
        course['title'] = course_div.find("caption").string.split(" - ")[0]
        course['subject'] = course_div.find("caption").string.split(" - ")[1].split(" ")[0]
        course['number'] = course_div.find("caption").string.split(" - ")[1].split(" ")[1]
        course['section'] = course_div.find("caption").string.split(" - ")[2]

        for row in course_div.find_all("th"):
            attribute_name = ""
            for string in row.stripped_strings:
                attribute_name += string
            attribute_name = attribute_name.lower().replace(":","").replace(" ","_")
            
            attribute_desc = ""
            for string in row.find_next("td").stripped_strings:
                attribute_desc += string
            
            course[attribute_name] = attribute_desc
        course['crn'] = int(float(course['crn']))
        course['credits'] = int(float(course['credits']))
        
        return_data['courses'].append(course)

    return return_data

def get_awards(year):
    data = {
        "tab_type": "A0",
        "aidy_in": year,
        "calling_proc_name": ""
    }
    r = navigate_to(root_url + "/PRODCartridge/bwrkrhst.P_DisplayTabs?tab_type=AO&aidy_in=1718&calling_proc_name=", data=data)
    soup = BeautifulSoup(r.text, "html.parser")
    return_data = {}

    return_data['awards'] = []
    award_table = soup.find("table", summary="This table lists the award information.")
    table_rows = award_table.find_all("tr")
    table_rows.pop(0)
    table_rows.pop(0)
    for table_row in table_rows:
        award = {}
        row = table_row.find_all("td")
        award['fund'] = combine_strings(row[0].stripped_strings)
        award['fall'] = {
            "status": combine_strings(row[1].stripped_strings),
            "amount": combine_strings(row[2].stripped_strings)
        }
        award['spring'] = {
            "status": combine_strings(row[3].stripped_strings),
            "amount": combine_strings(row[4].stripped_strings)
        }
        award['total'] = combine_strings(row[5].stripped_strings)
        return_data['awards'].append(award)
    return_data['awards'].pop()
    
    return return_data

def get_grades(year, term):
    term_code = year
    if term.strip().lower() == "spring":
        term_code += "01"
    elif term.strip().lower() == "summer":
        term_code += "02"
    else:
        term_code += "03"

    r = navigate_to(root_url + "/PRODCartridge/bwskogrd.P_ViewGrde", method="POST", data={"term_in": term_code})
    soup = BeautifulSoup(r.text, "html.parser")
    return_data = {}

    return_data['grades'] = []
    grades_div = soup.find_all("table", "datadisplaytable")[1]

    table_rows = grades_div.find_all("tr")
    table_rows.pop(0)
    for table_row in table_rows:
        grade = {}
        row = table_row.find_all("td")
        grade['title'] = combine_strings(row[4].stripped_strings)
        grade['subject'] = combine_strings(row[1].stripped_strings)
        grade['number'] = combine_strings(row[2].stripped_strings)
        grade['section'] = combine_strings(row[3].stripped_strings)
        grade['crn'] = int(float(combine_strings(row[0].stripped_strings)))
        grade['final_grade'] = combine_strings(row[6].stripped_strings)
        grade['credits'] = int(float(combine_strings(row[9].stripped_strings)))
        grade['quality_points'] = float(combine_strings(row[10].stripped_strings))
        return_data['grades'].append(grade)

    return return_data

def combine_strings(strings):
    return_string = ""
    for string in strings:
        return_string += string
    return return_string

def write_file(text, file_name):
    f = open(file_name, 'w')
    f.write(text)