# banweb-python
Interface with the banner website to access academic information in your programs.

Requires the requests library and BeautifulSoup4
```
pip install requests
pip instal beautifulsoup4
```
### Table of contents
  * [Examples](#examples)
    * [Getting a list of registered courses](#getting-a-list-of-registered-courses)
    * [Getting a list of financial awards](#getting-a-list-of-financial-awards)
    * [Getting a list of grades](#getting-a-list-of-grades)
  * [Documentation](#documentation)
    * [login](#loginroot-sid-pin-security_answer)
    * [navigate_to](#navigate_tourl-headersnone-datanone-cookiesnone-methodget)
    * [get_courses](#get_coursesyear-term)
    * [get_awards](#get_awardsyear)
    * [get_grades](#get_gradesyear-term)
## Examples
### Getting a list of registered courses
```python
from banweb import login, get_courses
import json

login("https://banweb.example.edu", "ABC123456", "12345", "Answer")
courses = get_courses("2018", "fall")

print(json.dumps(courses, indent=4))
```
This code would output:
```
{
    "total_credits": 16,
    "courses": [
        {
            "title": "Example Course",
            "subject": "EX",
            "number": "3000",
            "section": "10",
            "associated_term": "Fall 2018",
            "crn": 24567,
            "status": "**Web Registered** on 04/19/18",
            "assigned_instructor": "Jim A. Bob",
            "grade_mode": "Letter Grade",
            "credits": 3,
            "level": "Undergraduate",
            "campus": "Main Campus"
        },
        {
            "title": "Example Discussion",
            "subject": "EX",
            "number": "3000",
            "section": "30",
            "associated_term": "Fall 2018",
            "crn": 24568,
            "status": "**Web Registered** on 04/19/18",
            "assigned_instructor": "Jim A. Bob",
            "grade_mode": "Letter Grade",
            "credits": 0,
            "level": "Undergraduate",
            "campus": "Main Campus"
        },
        ...
    ]
}
```
### Getting a list of financial awards
```python
from banweb import login, get_awards
import json

login("https://banweb.example.edu", "ABC123456", "12345", "Answer")
awards = get_awards("1718")

print(json.dumps(awards, indent=4))
```
This code would output:
```
{
    "awards": [
        {
            "fund": "Honors Scholarship",
            "fall": {
                "status": "Accepted",
                "amount": "$7,500.00"
            },
            "spring": {
                "status": "Accepted",
                "amount": "$7,500.00"
            },
            "total": "$15,000.00"
        },
        {
            "fund": "Federal Work-Study",
            "fall": {
                "status": "Web Accept",
                "amount": "$1,250.00"
            },
            "spring": {
                "status": "Web Accept",
                "amount": "$1,250.00"
            },
            "total": "$2,500.00"
        },
        ...
    ]
}
```
### Getting a list of grades
```python
from banweb import login, get_grades
import json

login("https://banweb.example.edu", "ABC123456", "12345", "Answer")
grades = get_grades("2018", "spring")

print(json.dumps(grades, indent=4))
```
This code would output:
```
{
    "grades": [
        {
            "title": "Intro To Python",
            "subject": "CSCI",
            "number": "1000",
            "section": "10",
            "crn": 20345,
            "final_grade": "A",
            "credits": 3,
            "quality_points": 12.0
        },
        {
            "title": "Programming Ethics",
            "subject": "CSCI",
            "number": "1030",
            "section": "10",
            "crn": 29634,
            "final_grade": "F",
            "credits": 3,
            "quality_points": 0.0
        },
        ...
    ]
}
```

## Documentation
### login(root, sid, pin, security_answer)
Starts a banner session with the given credentials. Required in order to use any methods that access the banner site.
  * **root:** The root url for user's banner site
  * **sid:** The user's sid used to log into banner
  * **pin:** The user's pin used to log into banner
  * **security_answer:** The answer to the user's security question

Example usage:
```python
>>> from banweb import login

>>> login("https://banweb.example.edu", "ABC123456", "12345", "Answer")
```

### navigate_to(url, headers=None, data=None, cookies=None, method="GET")
Loads the given url using the banner session and returns a response object
  * **url:** The url to load
  * **headers:** Optional HTTP headers
  * **cookies:** Optional Session cookies
  * **method:** Optional HTTP method (defaults to GET)
  * **returns:** A response object containing HTTP response data

Example usage:
```python
>>> from banweb import login, navigate_to, root_url

>>> login("https://banweb.example.edu", "ABC123456", "12345", "Answer")
>>> # Use root_url to use the root specified on login
>>> response = navigate_to(root_url + "/PRODCartridge/bwskfshd.P_CrseSchd?start_date_in=08/27/2018", method="GET", data={"start_date_in": "08/27/2018"})
>>> response.status_code
200
>>> response.text
'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML...'
```

### get_courses(year, term)
Returns a list of the user's registered courses for the given term
  * **year:** Year in which the courses are registered for
  * **term:** Term in which the courses are registered for (Spring, Summer, or Fall)
  * **returns:** An object containing overall course information and a list of courses

Example usage:
```python
>>> from banweb import login, get_courses

>>> login("https://banweb.example.edu", "ABC123456", "12345", "Answer")
>>> course_info = get_courses("2018", "Spring")
>>> course_info.total_credits
15
>>> course_info.courses.length
5
>>> course_info
{
    "total_credits": 15,
    "courses": [
        {...},
        {...},
        {...},
        {...},
        {...}
    ]
}
```

### get_awards(year)
Returns a list of the user's financial awards
  * **year:** Year in which the awards are offered
  * **returns:** An object containing a list of awards offered to the user for the given academic year

Example usage:
```python
>>> from banweb import login, get_awards

>>> login("https://banweb.example.edu", "ABC123456", "12345", "Answer")
>>> award_info = get_awards("1718")
>>> award_info.awards.length
2
>>> award_info.awards[0].total
'$15,000.00'
>>> award_info
{
    "awards": [
        {...},
        {...}
    ]
}
```

### get_grades(year, term)
Returns a list of the user's registered courses for the given term
  * **year:** Year in which the courses were registered for
  * **term:** Term in which the courses were registered for (Spring, Summer, or Fall)
  * **returns:** An object containing a list of all course grades for the given term

Example usage:
```python
>>> from banweb import login, get_grades

>>> login("https://banweb.example.edu", "ABC123456", "12345", "Answer")
>>> grade_info = get_grades("2018", "Spring")
>>> grade_info.grades.length
5
>>> grade_info.grades[0].final_grade
'A'
>>> grade_info.grades[0].credits
3
>>> grade_info
{
    "grades": [
        {...},
        {...},
        {...},
        {...},
        {...}
    ]
}
```