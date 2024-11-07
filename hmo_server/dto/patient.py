from dto.address import Address
class Patient:
    def __init__(self,
                 id, firstName, lastName, dateOfBirth, phone, mobilePhone,address):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.dateOfBirth = dateOfBirth
        self.phone = phone
        self.mobilePhone = mobilePhone

