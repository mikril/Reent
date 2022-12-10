from main import *
import os, glob
from multiprocessing import Pool
import time
import csv

class DataSet2:
    """ Класс DataSet для обработки, филтрации, сортировки вакансий

        Attributes: 
            file_name(str): Название файла
            filterElements(list): Два элемента столбец по которому фильтровать, значение филтрации
            sortElements(str): Столбец который нужно сортировать
            reversVacancies(str): Отреверсировать сортировку Да, Нет?
            vacancies_objects(list): контейнер для измененых, отфильтрованных, отсортированных, вакансий
    """
    def __init__(self,file_name,filterElements,sortElements,reversVacancies,nameVacancy,vacancies_objects=[]):
        """ Иницилизирует DataSet 

        Args: 
            file_name(str): Название файла
            filterElements(list): Два элемента столбец по которому фильтровать, значение филтрации
            sortElements(str): Столбец который нужно сортировать
            reversVacancies(str): Отреверсировать сортировку Да, Нет?
            vacancies_objects(list): контейнер для измененых, отфильтрованных, отсортированных, вакансий
            countVacancyesYear(dict): динамика зарплат по годам
            salarysYear(dict): динамика количество вакансий по годам
            salaryTown(dict): динамика зарплат по городам
            VacanciesTown(dict): динамика количества вакансий по городам
            filterSalarysYear(dict): динамика зарплат по годам для конкретной вакансии
            filterCountVacancyesYear:(dict) динамика количество вакансий по годам для конкретной вакансии
            nameVacancy:название профессии для статистики
            
            >>> type(DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","")).__name__
            'DataSet'
            >>> DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").file_name 
            'vacancies.csv'
            >>> DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").filterElements[0] 
            'Дата публикации'
            >>> DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").filterElements[1] 
            '15.12.2022'
            >>> DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").sortElements 
            'Думайте'
            >>> DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").reversVacancies 
            ''
        """
        self.file_name=file_name
        self.vacancies_objects=vacancies_objects
        self.filterElements=filterElements
        self.sortElements=sortElements
        self.reversVacancies=reversVacancies
        self.countVacancyesYear={}
        self.salarysYear={}
        self.salaryTown={}
        self.VacanciesTown={}
        self.filterSalarysYear={}
        self.filterCountVacancyesYear={}
        self.nameVacancy=nameVacancy


    def potokDinamic(self,fileNames):
        """ Функция для потоковой динамики

            Args: 
                fileNames(list): названия файлов
        """
        p = Pool(10)
        a=p.map(self.yearDinamic,fileNames)
        for i in a:
            self.vacancies_objects+=i.vacancies_objects
            self.countVacancyesYear=dict(list(self.countVacancyesYear.items()) + list(i.countVacancyesYear.items()))
            self.salarysYear=dict(list(self.salarysYear.items()) + list(i.salarysYear.items()))
            self.filterSalarysYear=dict(list(self.filterSalarysYear.items()) + list(i.filterSalarysYear.items()))
            self.filterCountVacancyesYear=dict(list(self.filterCountVacancyesYear.items()) + list(i.filterCountVacancyesYear.items()))
            
        self.townDinamic()  

    def checkEmpty(self,filename): 
        """ Функция запуска чтения файла, проверки файла на пустоту вцелом
        """
        reader, list_naming=self.сsv_reader(filename)
        if len(list_naming)>0 and len(reader)>0:
            self.csv_ﬁler(reader,list_naming)
        elif len(list_naming)>0:
            print("Нет данных")
            exit()
        else:
            print("Пустой файл")  
            exit()  
        
    def сsv_reader(self,filename):
        """ Функция для чтения файла, разбитие его на массив вакансий, на масив названий столбцов

            Returns:
                list: список вакансий 
                list: список названий столбцов элементов вакансии
        """
        file_name=self.file_name
        list_naming=[]
        reader=[]
        with open(filename, encoding="utf-8-sig") as File: 
            for row in csv.reader(File, delimiter=',', quoting=csv.QUOTE_MINIMAL):
                if(not("" in row)):
                    if (len(list_naming) > 0  and len(list_naming)<=len(row)):
                        reader.append(row)
                    if (len(list_naming)==0):
                        list_naming = row
        return reader, list_naming   
    def csv_ﬁler( self, reader, list_naming):  
        """ Функция перезаписи двух списков в список словарей, для запуска функции форматирования элементов вакансии, фильтрации и сортировки этого словарая

            Args:
                reader: список вакансий 
                list_naming: список названий столбцов элементов вакансии


            >>> DataSet('vacancies.csv',["Дата публикации вакансии","15.12.2022"],"","").csv_ﬁler([['папич','быть величайшим','дота казик','moreThan6','Да','ютюб','Винница','2022-05-31T17:32:31+0300'],['monkey', 'asdaisfuiasd', 'banana', 'noExperience', 'Да', 'zoo', 'Moscow', '2022-12-15T17:32:31+0300']],["name","description","key_skills","experience_id","premium","employer_name","area_name","published_at"]).vacancies_objects[0].elements
            ['monkey', 'asdaisfuiasd', 'banana', 'Нет опыта', 'Да', 'zoo', '', 'Moscow', datetime.datetime(2022, 12, 15, 17, 32, 31, 30000)]
        """
        for element in reader:
            dictVacancy={}
            for i in range(len(element)):
                dictVacancy[list_naming[i]]=element[i]
            self.vacancies_objects.append(self.formatter(dictVacancy))
        #фильтрация
        if len(self.filterElements[0])>0:
            if filterToNames[self.filterElements[0]] in list(filterToNames.values()): 

                if filterToNames[self.filterElements[0]]=="salary_from":
                    self.vacancies_objects=list(filter(lambda x:   float(x.salary.salary_from.replace(" ",""))<=float(self.filterElements[1]) and float(x.salary.salary_to.replace(" ",""))>=float(self.filterElements[1]),self.vacancies_objects))
                elif self.filterElements[0]=="Навыки": 
                    self.vacancies_objects=list(filter(lambda x:   set(self.filterElements[1].split(", ")).issubset(x.key_skills),self.vacancies_objects))
                elif filterToNames[self.filterElements[0]]=="salary_currency":
                    self.vacancies_objects=list(filter(lambda x:   self.filterElements[1]==x.salary.salary_currency,self.vacancies_objects))
                elif filterToNames[self.filterElements[0]]=="published_at":
                    self.vacancies_objects=list(filter(lambda x:   self.filterElements[1]=="{:%d.%m.%Y}".format(x.published_at),self.vacancies_objects))
                else: 
                    self.vacancies_objects=list(filter(lambda x:  self.filterElements[1] in getattr(x, filterToNames[self.filterElements[0]]), self.vacancies_objects))
                    #self.vacancies_objects=list(filter(lambda x:  getattr(x, filterToNames[self.filterElements[0]]) == self.filterElements[1], self.vacancies_objects))    
        #сортировка
        if self.sortElements=="Название" or self.sortElements=="Описание" or  self.sortElements=="Компания" or self.sortElements=="Название региона" or self.sortElements=="Дата публикации вакансии" or self.sortElements=="Премиум-вакансия":
            self.vacancies_objects.sort( key=lambda x: getattr(x,list(fieldToRus.keys())[list(fieldToRus.values()).index(self.sortElements)]), reverse=self.reversVacancies)
        if self.sortElements=="Оклад":
            self.vacancies_objects.sort( key=lambda x: (float(x.salary.salary_from.replace(" ",""))+float(x.salary.salary_to.replace(" ","")))*currency_to_rub[x.salary.salary_currency], reverse=self.reversVacancies)
        if self.sortElements=="Навыки":
            
            self.vacancies_objects.sort(key=lambda x: len(x.key_skills) if type(x.key_skills)==list else 1, reverse=self.reversVacancies)
            
        if self.sortElements=="Опыт работы":
            self.vacancies_objects.sort( key=lambda x: list(expiriences.values()).index(x.experience_id), reverse=self.reversVacancies)

    '''
    def convertData1(self,value):
        return datetime.strptime(value.replace("+",".").replace("T"," "), '%Y-%m-%d %H:%M:%S.%f')
    def convertData2(self,value):
        date = value.split("T")[0].split("-")
        time = value.split("T")[1].split(":")
        year = int(date[0])
        month = int(date[1])
        day = int(date[2])
        hour = int(time[0])
        minute = int(time[1])
        second = int(time[2].split("+")[0])
        miliseconds=int(time[2].split("+")[1])*100
        return datetime(year, month, day, hour, minute, second,miliseconds)
    def convertData3(self,value):
        return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S+%f')
    '''
    def convertData4(self,value):
        """ Преврощает строку в дату

                Args:
                    value(str):строка даты

                Returns:
                    datetime.datetime: дата
        """
        year = int(value[0:4])
        month = int(value[5:7])
        day = int(value[8:10])
        hour = int(value[11:13])
        minute = int(value[14:16])
        second = int(value[17:19])
        miliseconds=int(value[20::])*100
        return datetime(year, month, day, hour, minute, second,miliseconds)
    def yearDinamic(self,filename):
        """ Функция создания динамики зарплат по годам, количество вакансий по годам, зарплат по годам для конкретной вакансии, количество вакансий по годам для конкретной вакансии

            Args:
                filename: потоковые файлы
                
            Returns:
                DataSet: возвращает потоковый DataSet
        """
        self.checkEmpty(filename)
        
        for vacancy in self.vacancies_objects: 
            date=int("{:%Y}".format(vacancy.published_at))
            if not(date in self.countVacancyesYear):
                self.countVacancyesYear[date]=1
                self.filterCountVacancyesYear[date]=0
            else:
                self.countVacancyesYear[date]+=1
            if not(date in self.salarysYear):
                self.filterSalarysYear[date]=0
                self.salarysYear[date]=(float(vacancy.salary.salary_to.replace(" ",""))+float(vacancy.salary.salary_from.replace(" ","")))/2*currency_to_rub[vacancy.salary.salary_currency]
            else:
                self.salarysYear[date]+=(float(vacancy.salary.salary_to.replace(" ",""))+float(vacancy.salary.salary_from.replace(" ","")))/2*currency_to_rub[vacancy.salary.salary_currency]
            if self.nameVacancy in vacancy.name:
                if (date in self.filterCountVacancyesYear):
                    self.filterCountVacancyesYear[date]+=1
                if (date in self.filterSalarysYear):
                    self.filterSalarysYear[date]+=(float(vacancy.salary.salary_to.replace(" ",""))+float(vacancy.salary.salary_from.replace(" ","")))/2*currency_to_rub[vacancy.salary.salary_currency]
            
            

        self.salarysYear=dict(sorted(self.salarysYear.items(), key=lambda x: x[0]))
        self.countVacancyesYear=dict(sorted(self.countVacancyesYear.items(), key=lambda x: x[0]))
        self.filterSalarysYear=dict(sorted(self.filterSalarysYear.items(), key=lambda x: x[0]))
        self.filterCountVacancyesYear=dict(sorted(self.filterCountVacancyesYear.items(), key=lambda x: x[0]))
        return self
    def townDinamic(self):
        """Функция создания динамики зарплат по городам, количества вакансий по городам
        """
        for vacancy in self.vacancies_objects: 
            if not(vacancy.area_name in self.VacanciesTown):
                self.VacanciesTown[vacancy.area_name]=1
            else:
                self.VacanciesTown[vacancy.area_name]+=1
            if not(vacancy.area_name in self.salaryTown):
                self.salaryTown[vacancy.area_name]=(float(vacancy.salary.salary_to.replace(" ",""))+float(vacancy.salary.salary_from.replace(" ","")))/2*currency_to_rub[vacancy.salary.salary_currency]
            else:
                self.salaryTown[vacancy.area_name]+=(float(vacancy.salary.salary_to.replace(" ",""))+float(vacancy.salary.salary_from.replace(" ","")))/2*currency_to_rub[vacancy.salary.salary_currency]
        self.VacanciesTown=dict(sorted(self.VacanciesTown.items(), key=lambda x: x[1], reverse=True))
        self.salaryTown=dict(sorted(self.salaryTown.items(), key=lambda x: x[1]/self.VacanciesTown[x[0]],reverse=True))
        self.salaryTown=dict(filter(lambda x: self.VacanciesTown[x[0]]/len(self.vacancies_objects) >=0.01, self.salaryTown.items()))
    def formatter(self,row): 
        """ Форматирует элемнты вакансии

            Args:
                row: словарь вакансии

            Returns:
                Vacancy: возвращает отформаттированную вакансию

            >>> DataSet('vacancies.csv',["Дата публикации","15.12.2022"],"Думайте","").formatter({"name":"monkey","description":"<p>asdaisfuiasd</p>","key_skills":"banana","experience_id":"noExperience","premium":"Да","employer_name":"zoo","area_name":"Moscow","published_at":"2022-05-31T17:32:31+0300"}).elements
            ['monkey', 'asdaisfuiasd', 'banana', 'Нет опыта', 'Да', 'zoo', '', 'Moscow', datetime.datetime(2022, 5, 31, 17, 32, 31, 30000)]
        """
        args=["","","","", "","","","",""]
        namesindex=["name","description","key_skills","experience_id","premium","employer_name","salary","area_name","published_at"]
        argsSalary=["","","",""]
        namessalary=["salary_from","salary_to","salary_gross","salary_currency"]
        keys=list(row.keys())
        if len(keys)>0:
            for i in range(len(keys)):
                value = row[keys[i]]
                
                if("\n" in value):
                    value = value.split("\n")
                    for index in range(len(value)):
                        value[index] = ' '.join(re.sub(r"<[^>]+>", '', value[index]).split())
                else:
                    value = ' '.join(re.sub(r"<[^>]+>", '', value).split())
                
                if(type(value) != list and value.upper()=="TRUE"):
                    value = "Да"
                if(type(value) != list and value.upper()=="FALSE"):
                    value = "Нет"
                if (keys[i]=="experience_id"):
                    value= expiriences[value]
                if (keys[i]=="published_at"):
                    '''
                    a=self.convertData1(value)
                    b=self.convertData2(value)
                    c=self.convertData3(value)
                    d=self.convertData4(value)
                    '''
                    value = self.convertData4(value)

                if(keys[i]=="salary_from"):
                    value='{:,}'.format(int(float(row[keys[i]]))).replace(',', ' ')
                    argsSalary[namessalary.index(keys[i])]=value
                elif(keys[i]=="salary_to"):
                    value='{:,}'.format(int(float(row[keys[i]]))).replace(',', ' ')
                    argsSalary[namessalary.index(keys[i])]=value
                elif(keys[i]=="salary_gross"):
                    value = (("С вычетом налогов") if (row[keys[i]].upper()=="FALSE") else ("Без вычета налогов"))
                    argsSalary[namessalary.index(keys[i])]=value
                elif(keys[i]=="salary_currency"):
                    value = currencies[row[keys[i]]]
                    argsSalary[namessalary.index(keys[i])]=value
                    args[namesindex.index("salary")]=Salary(*argsSalary)
                else:
                    args[namesindex.index(keys[i])]=value
        
        result=Vacancy(*args)
        return result
    






resultList = []
names = []
path = 'datas/'
alll = []
for filename in glob.glob(os.path.join(path, '*.csv')):
    alll.append(filename)


   
    

if __name__ == '__main__':
    name=input()
    dinamik=DataSet2(alll,[""], "","",name)
    
    dinamik.potokDinamic(alll)
    

    salarysYearKey=list(dinamik.salarysYear.keys())
    VacanciesTownKey=list(dinamik.VacanciesTown.keys())
    salaryTownKey=list(dinamik.salaryTown.keys())

    upgradeVacanciesTown={}

    filterSalarysYearKey=list(dinamik.filterSalarysYear.keys())
    i=0
    while(i<len(salarysYearKey)):
        if i<len(salarysYearKey):
            dinamik.salarysYear[salarysYearKey[i]]=int(dinamik.salarysYear[salarysYearKey[i]]/dinamik.countVacancyesYear[salarysYearKey[i]])
        if i<len(salaryTownKey) and i<10:
            dinamik.salaryTown[salaryTownKey[i]]=int(dinamik.salaryTown[salaryTownKey[i]]/dinamik.VacanciesTown[salaryTownKey[i]])
        if i<len(filterSalarysYearKey) and dinamik.filterCountVacancyesYear[filterSalarysYearKey[i]]!=0:
            dinamik.filterSalarysYear[filterSalarysYearKey[i]]=int(dinamik.filterSalarysYear[filterSalarysYearKey[i]]/dinamik.filterCountVacancyesYear[filterSalarysYearKey[i]])
        if i<len(VacanciesTownKey) and i<10:
            proc=round(dinamik.VacanciesTown[VacanciesTownKey[i]]/len(dinamik.vacancies_objects),4)
            if proc>=0.01:
                upgradeVacanciesTown[VacanciesTownKey[i]]=proc
        i+=1
    dinamik.salarysYear=dict(list(dinamik.salarysYear.items()))
    dinamik.countVacancyesYear=   dict(list(dinamik.countVacancyesYear.items()))
    dinamik.filterSalarysYear=dict(list(dinamik.filterSalarysYear.items()))
    dinamik.filterCountVacancyesYear=dict(list(dinamik.filterCountVacancyesYear.items()))
    dinamik.salaryTown=dict(list(dinamik.salaryTown.items())[0:10])
    upgradeVacanciesTown=dict(list(upgradeVacanciesTown.items())[0:10])
    print("Динамика уровня зарплат по годам: ",end="")
    print(dinamik.salarysYear)
    print("Динамика количества вакансий по годам: ",end="")
    print(dinamik.countVacancyesYear)
    print("Динамика уровня зарплат по годам для выбранной профессии: ",end="")
    print(dinamik.filterSalarysYear)
    print("Динамика количества вакансий по годам для выбранной профессии: ",end="")
    print(dinamik.filterCountVacancyesYear)
    print("Уровень зарплат по городам (в порядке убывания): ",end="")
    print(dinamik.salaryTown)
    print("Доля вакансий по городам (в порядке убывания): ",end="")
    print(upgradeVacanciesTown)

    exel = Report(name,dinamik.salarysYear,dinamik.countVacancyesYear,dinamik.filterSalarysYear,dinamik.filterCountVacancyesYear,dinamik.salaryTown,upgradeVacanciesTown)
    exel.generate_excel()
    exel.generate_diagrams()
    exel.createPdf()

