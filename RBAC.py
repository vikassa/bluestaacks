from enum import Enum

user_list =[]


class Role(Enum):
    ENGINEER =0
    SENIOR_ENGINEER = 1
    MANAGER = 2
    CONTRIBUTOR = 3



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
        #print("1")
        try:
            for element in Resource.resource_block:
                #print("2")
                if element.chip_id == id:
                    if self.roles:
                        for role in self.roles:
                            if role in element.read:
                                print("READ ALLOWED ")
                            elif role in element.write:
                                print("WRITE ALLOWED")
                            else:
                                print("No role assigned")
                    else:
                        print("No role assigned")
        except Exception as e:
            print("Exception " + str(e))


class Admin(User):
    def __init__(self, fname, lname, password):
        super().__init__(fname,lname,password)

    def create_user(self):
        try:
            pswd_flag = True
            global user_list
            fname , lname, password = None, None, None
            while pswd_flag:
                pswd_flag = False
                fname = input("Enter fname: ")
                lname = input("Enter lname: ")
                password = input("Enter password: ")
                for element in user_list:
                    if element.pswd == password:
                        print("Password exists , please try another")
                        pswd_flag = True
                        break

            user_obj = User(fname,lname,password)
            user_list.append(user_obj)
            print("user Added")
        except Exception as e:
            print("Exception " + str(e))

    def add_role(self,fname , lname ,role):
        try:
            if isinstance(role, Role):
                raise AttributeError("Not Role Enum Type")
            global user_list
            if user_list:
                for user in user_list:
                    if user.f_name == fname and user.l_name == lname:
                        user.roles.append(role)
            else:
                print("No user exist")
        except Exception as e:
            print("Exception " +str(e))

    def delete_role(self,fname , lname ,role):
        try:
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
        except Exception as e:
            print("Exception " + str(e))


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

    def view_roles_user(self, fname, lname):
        try:
            global user_list
            if user_list:
                for user in user_list:
                    if user.f_name == fname and user.l_name == lname:
                        user.view_roles()
        except Exception as e:
            print("Exception " +str(e))




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
        print("Read privileges")
        print(self.read)

    def show_write_roles(self):
        print("Write privileges")
        print(self.write)

    def add_write_privilege(self,role):
        if isinstance(role, Role):
            raise AttributeError("Not Role Enum Type")
        else:
            if role not in self.write:
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
        try:
            if cls.resource_block:
                for element in cls.resource_block:
                    if element.chip_id == id:
                        print("this chipset doc already exists")
                        return
            newobj = ConfidentialChipsetDoc(id)
            newobj.add_read_privilege("ENGINEER")
            newobj.add_read_privilege("MANAGER")
            newobj.add_write_privilege("MANAGER")
            cls.resource_block.append(newobj)
        except Exception as e:
            print("Exception "+str(e))

    @classmethod
    def remove_resource(cls,id):
        for element in cls.resource_block:
            if element.chip_id == id:
                cls.resource_block.remove(element)

    @classmethod
    def view_resources(cls):
        for element in cls.resource_block:
            print(element.chip_id)
            element.show_read_roles()
            element.show_write_roles()

class Activity:
    login_type = None
    admin = None
    user = None


    @classmethod
    def get_user_obj(cls, fname, password):
        global user_list
        if user_list:
            for user in user_list:
                if user.f_name == fname and user.pswd == password:
                    return user

        print("No such user exists")
        return None


    @classmethod
    def login(cls):
        try:
            fname = input("Enter fname for login: ")
            password = input("Enter password for login: ")
            for i, element in enumerate(user_list):
                if element.pswd == password and element.f_name == fname and i == 0:
                    cls.login_type = 'admin'
                    print("You are logged in as admin")
                elif element.pswd == password and element.f_name == fname:
                    print("You are logged in as: " + element.f_name)
                    cls.login_type = 'user'
                    cls.user = cls.get_user_obj(fname, password)
            cls.show_options()
        except Exception as e:
            print("Exception " + str(e))

    @classmethod
    def show_options(cls):
        try:
            if cls.login_type == 'admin':
                choice = 0
                while choice !=5:
                    print("---------------------\nPress 1 to see resource\nPress 2 to login as another user\n"
                          "Press 3 to create user\nPress 4 to edit role\nPress 5 to exit")
                    choice = int(input("Enter your choice:"))
                    if choice == 1:
                        Resource.view_resources()
                    elif choice == 2 :
                        cls.login()
                    elif choice == 3:
                        cls.admin.create_user()
                    elif choice == 4:
                        print("Enter details of user\n")
                        fname = input("Enter fname: ")
                        lname = input("Enter lname: ")
                        choice_edit = 0
                        while choice_edit !=5:
                            print("-------------------------------\nPress 1 to view roles\nPress 2 to add role"
                                  " \nPress 3 to delete role \nPress 5 to exit")
                            choice_edit = int(input("Enter your choice: "))
                            if choice_edit == 1:
                                cls.admin.view_roles_user(fname,lname)
                            elif choice_edit ==2:
                                role = input("Enter any one role from  ENGINEER/SENIOR_ENGINEER/MANAGER/CONTRIBUTOR: ")
                                cls.admin.add_role(fname, lname,role)


            elif cls.login_type == 'user':
                choice = 0
                while choice !=3:
                    print("-----------------------------\n"
                          "Press 1 to see access resources\nPress 2 to login as another user\nPress 3 to exit")
                    choice = int(input("Enter your choice:"))
                    if choice == 1:
                        id = input("enter resource id: ")
                        cls.user.access_resource(id)
                    elif choice == 2:
                        cls.login()
        except Exception as e:
            print("Exception as "+ str(e))

    @classmethod
    def start_activity(cls):
        try:
            global user_list
            print("Initialising system with some resource,admin account , user account")
            print("Enter Admin details")
            fname = input("Enter fname: ")
            lname = input("Enter lname: ")
            password = input("Enter pasword: ")
            cls.admin = Admin(fname,lname,password)
            cls.admin.roles=["ENGINEER", "SENIOR_ENGINEER", "MANAGER", "CONTRIBUTOR"]
            user_list.append(cls.admin)
            print("Enter user1 details,please enter different details other than admin")
            fname = input("Enter fname: ")
            lname = input("Enter lname: ")
            password = input("Enter pasword: ")
            user1 = User(fname,lname,password)
            user_list.append(user1)
            print("Creating one resource with id 'MTK12477' ")
            Resource.add_resource('MTK12477')
            Resource.view_resources()
            cls.login()
        except Exception as e:
            print("Exception " +str(e))


if __name__ == "__main__":
    Activity.start_activity()
