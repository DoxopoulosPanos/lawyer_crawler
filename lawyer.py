class Lawyer:
    def __init__(self):
        self.company_name = ""
        self.city = ""
        self.state = ""
        self.phone = ""
        self.website = ""
        self.profile_url = ""

    def __str__(self):
        string = "company_name: {}".format(self.company_name)
        string += "\n"
        string += "city: {}".format(self.city)
        string += "\n"
        string += "state: {}".format(self.state)
        string += "\n"
        string += "phone: {}".format(self.phone)
        string += "\n"
        string += "website: {}".format(self.website)
        string += "\n"
        string += "profile_url: {}".format(self.profile_url)

        return string