
class Register:
    def __init__(self, location):
        self.location = location

    def make_transaction(self):
        return


class Transaction:
    def __init__(self, transaction_id, date, location, type, payment):  ##type = payment or return
        self.transaction_id = transaction_id
        self.date = date
        self.location = location
        self.type = type
        self.payment = payment


    def manage(self):
        return

    def maintain(self):
        return


class Items:
    def __init__(self, id, name):
        self.id = id
        self.Name = name



class admin_Account:
    def __init__(self):

    def RecoverPassword(self):
        return
    def ExportHistory(self):
        return
    def AccessTransaction(self):
        return
    ##transaction

class General_account:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def VerifyPassword(self):
        return
    def AccessRegister(self):
        return
    ##register


##class History:
