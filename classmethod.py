# -*- coding: utf-8 -*-

class Person(object):
    def __init__(self, fname, lname, age, sex):
        self.fname = fname
        self.lname = lname
        self.age = age
        self.sex = sex

    @classmethod
    def from_string(cls, person_info):
        fname, lname, age, sex = 'john,smith,25,male'.split(',')
        person1 = cls(fname, lname, int(age), sex)
        return person1

    @classmethod
    def from_list(cls, person_info_list):
        #assume person_info_list is in the format of ['john','smith',25,'male']
        fname, lname, age, sex = person_info_list
        person = cls(fname, lname, age, sex)
        return person

    @staticmethod
    def welcome(message):
        print('Greetings: {}'.format(message))


class Senior(Person):
    def __init__(self, fname, lname, age, sex):
        super(self.__class__,self).__init__(fname, lname, age, sex)



person_string = 'john,smith,25,male'
#split string to 4 variables
fname, lname, age, sex =  person_string.split(',')
#initiate class
person = Person(fname, lname, age, sex)
print(person.fname, lname, age, sex)
#use classmethod to initiate class
person1 = Person.from_string('john,smith,25,male')
print(person.fname, lname, age, sex)
#use another classmethod to initiate
person2 = Person.from_list(['john','smith',25,'male'])
print(person.fname, lname, age, sex)
#static method
Person.welcome("hello world")

#another example with inheritance
senior = Senior.from_string('john,smith,70,male')
senior.welcome("hello there")