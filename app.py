from flask import Flask, redirect, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import requests
from urllib.parse import urlencode
from sqlalchemy import text
import xlsxwriter
import pandas as pd
from selenium import webdriver
from getpass import getpass
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

app = Flask(__name__)

ENV = "dev"

if ENV == "dev":
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@tawanda14@localhost/hangar49test'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ""


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api_key = "4e729c19-df8f-4f97-825d-2308b611075e"


class DataTableModel(db.Model):
    __tablename__ = "sheet_data"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    job_title_full = db.Column(db.String(200))
    job_title = db.Column(db.String(200))
    city = db.Column(db.String(200))
    country = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    company = db.Column(db.String(200))
    company_website = db.Column(db.String(200))
    company_industry = db.Column(db.String(200))
    company_founded = db.Column(db.String(200))
    company_size = db.Column(db.String(200))
    company_linkedin = db.Column(db.String(200))
    company_headquaters = db.Column(db.String(200))
    email_reliability_status = db.Column(db.String(200))
    receiving_email_server = db.Column(db.String(200))
    kind = db.Column(db.String(200))
    tag = db.Column(db.String(200))
    month = db.Column(db.String(200))

    def __init__(self, first_name, last_name, email, job_title_full, job_title, city, country, linkedin, company,
                 company_website, company_industry, company_founded, company_size, company_linkedin,
                 company_headquaters, email_reliability_status, receiving_email_server, kind, tag, month):
        # print("Hello")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.job_title = job_title
        self.job_title_full = job_title_full
        self.city = city
        self.company = company
        self.country = country
        self.linkedin = linkedin
        self.company_website = company_website
        self.company_industry = company_industry
        self.company_founded = company_founded
        self.company_size = company_size
        self.company_linkedin = company_linkedin
        self.company_headquaters = company_headquaters
        self.email_reliability_status = email_reliability_status
        self.receiving_email_server = receiving_email_server
        self.kind = kind
        self.tag = tag
        self.month = month





@app.route("/get_data")
def index():
    return "Hello Tawanda"


@app.route("/submit", methods=["Get", "POST"])
def submit():
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_cred.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Tech Test").sheet1  # get sheet 1 data

    sheet_data = sheet.get_all_records()
    k = []
    f_data = []
    for data in sheet_data:

        if db.session.query(DataTableModel).filter(DataTableModel.first_name == data["first_name"]).count() == 0:
            first_name = data["first_name"]
            last_name = data["last_name"]
            email = data["email"]
            job_title = data["job_title"]
            job_title_full = data["job_title_full"]
            city = data["city"]
            company = data["company"]
            country = data["country"]
            linkedin = data["linkedin"]
            company_website = data["company_website"]
            company_industry = data["company_industry"]
            company_founded = (data["company_founded"])
            company_size = data["company_size"]
            company_linkedin = data["company_linkedin"]
            company_headquaters = data["company_headquarters"]
            email_reliability_status = data["email_reliability_status"]
            receiving_email_server = data["receiving_email_server"]
            kind = data["kind"]
            tag = data["tag"]
            month = data["month"]
            # print(month)

            commit_data = DataTableModel(first_name, last_name, email, job_title_full, job_title, city, country,
                                         linkedin, company,
                                         company_website, company_industry, company_founded, company_size,
                                         company_linkedin,
                                         company_headquaters, email_reliability_status, receiving_email_server, kind,
                                         tag, month)

            db.session.add(commit_data)
            db.session.commit()

    post_data = db.session.query(DataTableModel).all()
            
    for data in post_data:
        f_data.append({"id": data.id, "first_name": data.first_name, "last_name": data.last_name, "email": data.email, "job_title": data.job_title,
                 "job_title_full": data.job_title_full, "city": data.city, "country":data.country, "linkedin": data.linkedin, "company": data.company,
                 "company_website": data.company_website, "company_industry": data.company_industry, "company_founded": data.company_founded,
                 "company_size": data.company_size, "company_linkedin": data.company_linkedin, "company_headquaters": data.company_headquaters,
                 "email_reliability_status": data.email_reliability_status, "receiving email server": data.receiving_email_server, "kind": data.kind, "tag": data.tag, "month": data.month})
    # print(f_data)           
    return jsonify(f_data)


@app.route("/push_hub", methods=["GET", "POST"])
def push_hub():
    api_key = "55c2950d-1177-4b52-a78b-3fbf8fd142b8"
    endpoint = f'https://api.hubapi.com/contacts/v1/contact/?hapikey={api_key}'
    headers = {"Content-Type": "application/json"}
    database_data = db.session.query(DataTableModel).all()
    for db_data in database_data:
        # print(db_data.month)
        data = json.dumps({
            "properties": [
                {
                    "property": "email",
                    "value": db_data.email
                },
                {
                    "property": "firstname",
                    "value": db_data.first_name
                },
                {
                    "property": "lastname",
                    "value": db_data.last_name
                },
                {
                    "property": "job_title_full",
                    "value": db_data.job_title_full
                },
                {
                    "property": "Jobtitle",
                    "value": db_data.job_title
                },
                {
                    "property": "city",
                    "value": db_data.city
                },
                {
                    "property": "country",
                    "value": db_data.country
                },
                {
                    "property": "linkedin",
                    "value": db_data.linkedin
                },
                {
                    "property": "company",
                    "value": db_data.company
                },
                {
                    "property": "website",
                    "value": db_data.company_website
                },
                {
                    "property": "industry",
                    "value": db_data.company_industry
                },
                {
                    "property": "company_founded",
                    "value": db_data.company_founded
                },
                {
                    "property": "company_size",
                    "value": db_data.company_size
                }
                , {
                    "property": "month_value",
                    "value": db_data.month
                },
                {
                    "property": "company_linkedin",
                    "value": db_data.company_linkedin
                },
                {
                    "property": "email_reliability_status",
                    "value": db_data.email_reliability_status
                },
                {
                    "property": "receiving_email_server",
                    "value": db_data.receiving_email_server
                },
                {
                    "property": "kind",
                    "value": db_data.kind
                },
                {
                    "property": "tag",
                    "value": db_data.tag
                }, {
                    "property": "company_headquarters",
                    "value": db_data.company_headquaters
                }
                
            ]
            
        })


        f = open("demofile2.txt", "a")
        
        r = requests.post(url=endpoint, data=data, headers=headers)
        # print(r.text)
        f.write(r.text)
        f.close()
    return jsonify("successfully posted to hub")


@app.route("/hub_pull", methods=["GET", "POST"])
def hub_pull():
    
    def get_others(other, dict):
        get_all_contacts_url = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all?"
        parameter_dict = {'hapikey': api_key}
        headers = {}
        has_more = True
        parameter_dict = {'hapikey': api_key, "property": f"{other}"}
        others = []
        while has_more:
            parameters = urlencode(parameter_dict)
            get_url = get_all_contacts_url + parameters
            r = requests.get(url=get_url, headers=headers)
            response_dict = json.loads(r.text)
            for i in range(len(response_dict["contacts"])):
                # print(response_dict["contacts"][i]["properties"])
                try:
                    other_col = response_dict["contacts"][i]["properties"][f"{other}"]["value"]
                    others.append(other_col)

                except:
                    other_col = response_dict
                    others.append(other_col)

                dict.update({f"{other}": others})
            has_more = response_dict['has-more']
        return dict

    contact_list = []
    property_list = []

    get_all_contacts_url = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all?"
    parameter_dict = {'hapikey': api_key}
    headers = {}
    dictionery = {}
    values = ["city", "email", "country", "industry", "jobtitle", "company_founded", "kind", "company_size", "tag", "website",
              "firstname", "lastname", "company", "job_title_full", "email_reliability_status", "linkedin", "company_linkedin", "company_headquarters", "receiving_email_server","month_value", "industry" ]
    city= email= country= industry= job_title= founded= kind= size= tag= company_website= first_name= last_name= company=job_title_full=email_reliability_status=linkedin= company_linkedin= company_headquaters= receiving_email_server=month = ""

    for value in values:
        dict_values = get_others(value, dictionery)
        
        for i in range(6):
            for key, values in dict_values.items():
 
                if key == "city":
                    city = values[i]
                elif key == "email":
                    email = values[i]
                elif key == "country":
                    country = values[i]
                elif key == "industry":
                    industry = values[i]
                elif key == "jobtitle":
                    job_title = values[i]
                elif key == "company_founded":
                    founded = ""
                elif key == "kind":
                    kind = values[i]
                elif key == "company_size":
                    size = values[i]
                elif key == "tag":
                    tag = values[i]
                elif key == "website":
                    company_website = values[i]
                elif key == "firstname":
                    first_name = values[i]
                elif key == "lastname":
                    last_name = values[i]
                elif key == "company":
                    company = values[i]
                elif key == "job_title_full":
                    job_title_full = values[i]
                elif key == "email_reliability_status":
                    email_reliability_status = values[i]
                elif key == "month_value":
                    month = values[i]
                elif key == "linkedin":
                    try:
                        linkedin = values[i]
                    except:
                        linkedin = ""

                elif key == "compay_linkedin":
                    try:
                        company_linkedin = values[i]
                    except:
                        company_linkedin = ""
                elif key == "company_headquarters":
                    company_headquaters =  values[i]
                elif  key == "receiving_email_server":
                    try:
                        receiving_email_server = values[i]
                    except:
                        receiving_email_server = ""
                
                    if db.session.query(DataTableModel).filter(DataTableModel.first_name == first_name,
                                                            DataTableModel.last_name == last_name,
                                                            DataTableModel.email == email,
                                                            DataTableModel.job_title == job_title,
                                                            DataTableModel.city == city,
                                                            DataTableModel.country == country,
                                                            DataTableModel.job_title_full == job_title_full,
                                                            DataTableModel.company == company,
                                                            DataTableModel.tag == tag).count() == 0:
                                                            
                        add_data = DataTableModel(first_name, last_name, email, job_title_full, job_title, city, country,
                                                linkedin, company,
                                                company_website, industry, founded, size,
                                                company_linkedin,
                                                company_headquaters, email_reliability_status, receiving_email_server,
                                                kind,
                                                tag, month)
                        db.session.add(add_data)
                        db.session.commit()
                    
    return jsonify("successfully posted to hub")

@app.route("/pull_dB", methods= ["GET", "POST"])
def pull_db():

    post_data = db.session.query(DataTableModel).all()
    f_data = []
            
    for data in post_data:
        f_data.append({"id": data.id, "first_name": data.first_name, "last_name": data.last_name, "email": data.email, "job_title": data.job_title,
                 "job_title_full": data.job_title_full, "city": data.city, "country":data.country, "linkedin": data.linkedin, "company": data.company,
                 "company_website": data.company_website, "company_industry": data.company_industry, "company_founded": data.company_founded,
                 "company_size": data.company_size, "company_linkedin": data.company_linkedin, "company_headquaters": data.company_headquaters,
                 "email_reliability_status": data.email_reliability_status, "receiving email server": data.receiving_email_server, "kind": data.kind, "tag": data.tag, "month": data.month})
    # print(f_data)           
    return jsonify(f_data)


@app.route("/update/<int:id>", methods=["PUT"])
def update(id):

    data = DataTableModel.query.filter_by(id=id).first()
    if data:
        latest = request.get_json()
        data.email_reliability_status = latest["value"]
        db.session.commit()
        

        return jsonify("Was updated")
    else:
        return jsonify("ID not found")

@app.route("/push_woodpecker", methods=["GET", "POST"])
def push_woodpecker():

    sql = text("select * from sheet_data " )
    res = db.engine.execute(sql)
    # workbook = xlsxwriter.Workbook('hello.xlsx') 
    # worksheet = workbook.add_worksheet()
    # book.close()
    i = 0 
    dic, arr = {}, []
    m = []

    for col in res:
        for key, val in col.items():
            m.append(key)
            dic = {**dic, **{key: val}}
        arr.append(dic)
    d = open("m.txt", "w")
    d.write(json.dumps(arr))
    print(arr)
    df = pd.DataFrame(columns=[m])
    for i in arr:
        # df.append(i, ignore_index=True)
        d = open("l.txt", "w")
        d.write(json.dumps(i))
        # print(i)

    # print(df)

    df.to_excel('dict1.xlsx')

        

    email = "tawasdev@gmail.com"
    password = "@Tawanda14"

    driver = webdriver.Chrome("C:\\Dev\\ChromeDriver\\chromedriver.exe")
    driver.get("https://app.woodpecker.co/login")

    email_textbox = driver.find_element_by_name("login")
    email_textbox.send_keys(email)
    password_textbox = driver.find_element_by_name("password")
    password_textbox.send_keys(password)

    login_button = driver.find_element_by_class_name("w-button")
    login_button.submit()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#prospects?r=t')]")))
    element.click()


    span =wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Add prospects']")))
    span.click()

    el2 = wait.until(EC.element_to_be_clickable((By.XPATH, ("(//div[@class='MenuItem-value'])[position()=1]"))))
    el2.click()

    file_upload = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "gwt-FileUpload")))
    file_upload.send_keys('C:\\Users\\tmuza\\Downloads\\HNGTASK\\Tech Test.xlsx')

    el3 = wait.until(EC.element_to_be_clickable((By.XPATH, ("(//div[@class='gwt-Label inLineLeft fontBook16 clientAddML'])[position()=2]"))))
    el3.click()

    el4 = wait.until(EC.element_to_be_clickable((By.XPATH, ("(//div[@class='gwt-Label buttonGreen hand GOU11VWDI'])"))))
    el4.click()

    el5= wait.until(EC.element_to_be_clickable((By.XPATH, ("(//div[@class='gwt-Label buttonGreen hand GOU11VWDD'])"))))
    el5.click()

    el6= wait.until(EC.element_to_be_clickable((By.XPATH, ("(//div[@class='gwt-Label buttonGreen goProsBtn'])"))))
    el6.click()

    return jsonify("Pushed to Woodpecker")







if __name__ == "__main":
    app.run(debug=True)
