from enum import Enum
import os

user_list =[]


class Role(Enum):
    ENGINEER =0
    SENIOR_ENGINEER = 1
    MANAGER = 2
    CONTRIBUTER = 3



class ActionType(Enum):
    READ = 0
    WRITE = 1
    DELETE = 2


class User:
    def __init__(self, fname , lname ,password):
        self.f_name = fname
        self.l_name = lname
        self.pswd = password
        self.roles = []

    def view_roles(self):
        if self.roles:
            for role in self.roles:
                print(role)
        else:
            print("No role assigned")

    def access_resource(self,id):
        for element in Resource.resource_block:
            if element.chip_id == id:
                for role in self.roles:
                    if role in element.read:
                        print("READ ALLOWED ")
                    elif role in element.wrtie:
                        print("WRITE ALLOWED")
                    else:
                        pass


class Admin(User):
    def __init__(self, fname, lname, password):
        super().__init__(fname,lname,password)

    def create_user(self):
        pswd_flag = True
        global user_list
        fname , lname, password = None, None, None
        while pswd_flag:
            pswd_flag = False
            fname , lname , password = input("Enter fname, lname and password separated by space").split('')
            for element in user_list:
                if element.pswd == password:
                    print("Password exists , please try another")
                    pswd_flag = True
                    break

        user_obj = User(fname,lname,password)
        user_list.append(user_obj)

    def add_role(self,fname , lname ,role):
        if isinstance(role, Role):
            raise AttributeError("Not Role Enum Type")
        global user_list
        if user_list:
            for user in user_list:
                if user.f_name == fname and user.l_name == lname:
                    user.roles.append(role)
        else:
            print("No user exist")

    def delete_role(self,fname , lname ,role):
        if isinstance(role, Role):
            raise AttributeError("Not Role Enum Type")
        global user_list
        if user_list:
            for user in user_list:
                if user.f_name == fname and user.l_name == lname:
                    if role in user.roles:
                        user.roles.remove(role)
        else:
            print("No user exist")

    def add_resource(self,chip_id):
        Resource.add_resource(chip_id)

    def remove_resource(self,chip_id):
        Resource.remove_resource(chip_id)

    def view_resources(self):
        if Resource.resource_block:
            for element in Resource.resource_block:
                print(element)
        else:
            print("No resource available yet")

    def view_roles_user(self,obj):
        obj.view_roles()



class ConfidentialChipsetDoc:
    def __init__(self, id):
        self.chip_id = id
        self.read =[]
        self.write =[]

    def add_read_privilege(self,role):
        if isinstance(role, Role):
            raise AttributeError("Not Role Enum Type")
        else:
            if role not in self.read:
                self.read.append(role)
            else:
                print("Already provided access")

    def show_read_roles(self):
        return self.read

    def show_write_roles(self):
        return self.write

    def add_write_privilege(self,role):
        if isinstance(role, Role):
            raise AttributeError("Not Role Enum Type")
        else:
            if role not in self.read:
                self.write.append(role)
            else:
                print("Already provided access")

    def remove_read_privilege(self, role):
        if isinstance(role, Role):
            raise AttributeError("Not Role Enum Type")
        else:
            if role not in self.read:
                print("This role already doesnt exist")
            else:
                self.read.remove(role)

    def remove_write_privilege(self, role):
        if isinstance(role, Role):
            raise AttributeError("Not Role Enum Type")
        else:
            if role not in self.read:
                print("This role already doesnt exist")
            else:
                self.write.remove(role)

class Resource:
    resource_block =[]

    @classmethod
    def add_resource(cls,id):
        for element in cls.resource_block:
            if element.chip_id == id:
                print("this chipset doc already exists")
                return
        newobj = ConfidentialChipsetDoc(id)
        cls.resource_block.append(newobj)

    @classmethod
    def remove_resource(cls,id):
        for element in cls.resource_block:
            if element.chip_id == id:
                cls.resource_block.remove(element)

    @classmethod
    def view_resources(cls):
        for element in cls.resource_block:
            print(element.chip_id)

class Activity:
    login_type = None

    @classmethod
    def login(cls):
        fname = input("Enter fname for login: ")
        password = input("Enter password for login: ")
        for i, element in enumerate(user_list):
            if element.pswd == password and element.f_name == fname and i == 0:
                cls.login_type = 'admin'
                print("You are logged in as admin")
            elif element.pswd == password and element.f_name == fname:
                print("You are logged in as" + element.f_name)
                cls.login_type = 'user'

    @classmethod
    def show_options(cls):
        if cls.login_type == 'admin':
            choice = input("Press 1 to see resource\n"
                           "Press 2 to login as another user ")
            if choice == 1:
                print("here")
                Resource.view_resources()
            if choice ==2 :
                cls.login()

    @classmethod
    def start_activity(cls):
        global user_list
        print("Initialising system with some resource,admin account , user account")
        fname = input("Enter fname: ")
        lname = input("Enter lname: ")
        password = input("Enter pasword: ")
        Ad = Admin(fname,lname,password)
        user_list.append(Ad)
        fname = input("Enter fname: ")
        lname = input("Enter lname: ")
        password = input("Enter pasword: ")
        user1 = User(fname,lname,password)
        user_list.append(user1)
        print("Creating one resource with id 'MTK12477' ")
        Resource.add_resource('MTK12477')
        cls.login()
        cls.show_options()

Activity.start_activity()