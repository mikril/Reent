from unittest import TestCase
from main import Salary, Vacancy, DataSet, Report
from datetime import datetime
class DataSetTests(TestCase):
    def test_dataSet_type(self):
        self.assertEqual(type(DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","")).__name__,'DataSet')
    def test_dataSet_file_name(self):
        self.assertEqual(DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").file_name, 'vacancies.csv')
    def test_dataSet_filterElements1(self):
        self.assertEqual(DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").filterElements[0],'Дата публикации')
    def test_dataSet_filterElements2(self):
        self.assertEqual(DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").filterElements[1],'15.12.2022')
    def test_dataSet_sortElements(self):
        self.assertEqual(DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").sortElements,'Думайте' )
    def test_dataSet_reversVacancies(self):
        self.assertEqual(DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").reversVacancies,'' )
    def test_dataSet_formatter(self):
        self.assertEqual(DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").formatter({"name":"monkey","description":"<p>asdaisfuiasd</p>","key_skills":"banana","experience_id":"noExperience","premium":"Да","employer_name":"zoo","area_name":"Moscow","published_at":"2022-05-31T17:32:31+0300"}).elements,['monkey', 'asdaisfuiasd', 'banana', 'Нет опыта', 'Да', 'zoo', '', 'Moscow', datetime(2022, 5, 31, 17, 32, 31, 30000)])
    def test_dataSet_csv_ﬁle(self):
        self.assertEqual(DataSet('vacancies.csv',["Дата публикации вакансии","15.12.2022"],"","").csv_ﬁler([['папич','быть величайшим','дота казик','moreThan6','Да','ютюб','Винница','2022-05-31T17:32:31+0300'],['monkey', 'asdaisfuiasd', 'banana', 'noExperience', 'Да', 'zoo', 'Moscow', '2022-12-15T17:32:31+0300']],["name","description","key_skills","experience_id","premium","employer_name","area_name","published_at"]).vacancies_objects[0].elements , ['monkey', 'asdaisfuiasd', 'banana', 'Нет опыта', 'Да', 'zoo', '', 'Moscow', datetime(2022, 12, 15, 17, 32, 31, 30000)])

class VacancyTests(TestCase):
    def test_vacancy_type(self):
        self.assertEqual(type(Vacancy()).__name__ ,'Vacancy')
    def test_vacancy_name(self):
        self.assertEqual(Vacancy('папич','быть величайшим',['дота','казик'],'всю жизнь','ДЫА','ютуб',Salary('1000000','infinity','Нет','RUB'),'Винница','07.07.777').name,'папич')
    def test_vacancy_description(self):
        self.assertEqual(Vacancy('папич','быть величайшим',['дота','казик'],'всю жизнь','ДЫА','ютуб',Salary('1000000','infinity','Нет','RUB'),'Винница','07.07.777').description ,'быть величайшим')
    def test_vacancy_key_skills(self):
        self.assertEqual(Vacancy('папич','быть величайшим',['дота','казик'],'всю жизнь','ДЫА','ютуб',Salary('1000000','infinity','Нет','RUB'),'Винница','07.07.777').key_skills,['дота', 'казик'])
    def test_vacancy_experience_id(self):
        self.assertEqual(Vacancy('папич','быть величайшим',['дота','казик'],'всю жизнь','ДЫА','ютуб',Salary('1000000','infinity','Нет','RUB'),'Винница','07.07.777').experience_id,'всю жизнь')
    def test_vacancy_premium(self):
        self.assertEqual(Vacancy('папич','быть величайшим',['дота','казик'],'всю жизнь','ДЫА','ютуб',Salary('1000000','infinity','Нет','RUB'),'Винница','07.07.777').premium,'ДЫА')
    def test_vacancy_employer_name(self):
        self.assertEqual(Vacancy('папич','быть величайшим',['дота','казик'],'всю жизнь','ДЫА','ютуб',Salary('1000000','infinity','Нет','RUB'),'Винница','07.07.777').employer_name,'ютуб')
    def test_vacancy_area_name(self):
        self.assertEqual(Vacancy('папич','быть величайшим',['дота','казик'],'всю жизнь','ДЫА','ютуб',Salary('1000000','infinity','Нет','RUB'),'Винница','07.07.777').area_name,'Винница')
    def test_vacancy_published_at(self):
        self.assertEqual(Vacancy('папич','быть величайшим',['дота','казик'],'всю жизнь','ДЫА','ютуб',Salary('1000000','infinity','Нет','RUB'),'Винница','07.07.777').published_at,'07.07.777')
    def test_vacancy_elements(self):
        self.assertEqual(len(Vacancy('папич','быть величайшим',['дота','казик'],'всю жизнь','ДЫА','ютуб',Salary('1000000','infinity','Нет','RUB'),'Винница','07.07.777').elements),9)

class SalaryTests(TestCase):
    def test_Salary_type(self):
        self.assertEqual(type(Salary()).__name__,'Salary')
    def test_Salary_salary_from(self):
        self.assertEqual(Salary('1000000','infinity','Нет','RUB').salary_from,'1000000')
    def test_Salary_salary_to(self):
        self.assertEqual(Salary('1000000','infinity','Нет','RUB').salary_to,'infinity')
    def test_Salary_salary_gross(self):
        self.assertEqual(Salary('1000000','infinity','Нет','RUB').salary_gross,'Нет')
    def test_Salary_salary_currency(self):
        self.assertEqual(Salary('1000000','infinity','Нет','RUB').salary_currency,'RUB')

class ReportTests(TestCase):
    def test_Report_type(self):
        self.assertEqual(type(Report('программист',[{2022:1000000}],[{2022:1}],[{"Винница":1000000}],[{"Винница":1}],[{2022:1000000}],[{2022:1}])).__name__,'Report')

    def test_Report_name(self):
        self.assertEqual( Report('программист',[{2022:1000000}],[{2022:1}],[{"Винница":1000000}],[{"Винница":1}],[{2022:1000000}],[{2022:1}]).name,'программист')
    def test_Report_salarysYear(self):
        self.assertEqual(Report('программист',[{2022:1000000}],[{2022:1}],[{"Винница":1000000}],[{"Винница":1}],[{2022:1000000}],[{2022:1}]).salarysYear[0],{2022: 1000000})
    def test_Report_countVacancyesYear(self):
        self.assertEqual(Report('программист',[{2022:1000000}],[{2022:1}],[{"Винница":1000000}],[{"Винница":1}],[{2022:1000000}],[{2022:1}]).countVacancyesYear[0][2022],1)
    def test_Report_filterSalarysYear(self):
        self.assertEqual(Report('программист',[{2022:1000000}],[{2022:1}],[{"Винница":1000000}],[{"Винница":1}],[{2022:1000000}],[{2022:1}]).filterSalarysYear[0]["Винница"],1000000)
    def test_Report_filterCountVacancyesYear(self):
        self.assertEqual(list(Report('программист',[{2022:1000000}],[{2022:1}],[{"Винница":1000000}],[{"Винница":1}],[{2022:1000000}],[{2022:1}]).filterCountVacancyesYear[0].keys())[0],'Винница')
    def test_Report_salaryTown(self):
        self.assertEqual(Report('программист',[{2022:1000000}],[{2022:1}],[{"Винница":1000000}],[{"Винница":1}],[{2022:1000000}],[{2022:1}]).salaryTown,[{2022: 1000000}])
    def test_Report_upgradeVacanciesTown(self):
        self.assertEqual(Report('программист',[{2022:1000000}],[{2022:1}],[{"Винница":1000000}],[{"Винница":1}],[{2022:1000000}],[{2022:1}]).upgradeVacanciesTown,[{2022: 1}])