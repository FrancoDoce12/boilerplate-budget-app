all_categorys = []


class Category:
    str_aligned: int = 30

    def __init__(self, name: str):
        self.name: str = name.capitalize()
        self.ledger: list = []
        all_categorys.append(self)

    def __str__(self):

        def add_spaces(number_of_spaces: int):
            spaces = ""
            for iterable in range(number_of_spaces):
                spaces = spaces.__add__(" ")
            return spaces

        line_of_name = ""
        simbol: chr = "*"
        how_many_simbols: int = int((self.str_aligned - self.name.__len__()) / 2)
        total_simbols_to_add: str = ""

        for i in range(how_many_simbols):
            total_simbols_to_add = total_simbols_to_add.__add__(simbol)

        line_of_name = line_of_name.__add__(total_simbols_to_add)
        line_of_name = line_of_name.__add__(self.name)
        line_of_name = line_of_name.__add__(total_simbols_to_add)
        line_of_name = line_of_name.__add__("\n")

        lines_of_deposits: str = ""
        for deposit in self.ledger:

            deposit_amount = deposit['amount']
            if type(deposit["amount"]) == int:
                deposit_amount = f"{deposit['amount']}.00"

            description_length: int = deposit["description"].__len__()
            amount_length: int = (str(deposit_amount)).__len__()

            if amount_length > 7:
                amount_to_display = (str(deposit_amount))[0:7]
            else:
                amount_to_display = str(deposit_amount)

            if description_length <= 23:
                description_to_display = deposit["description"]
            else:
                description_to_display = deposit["description"][0:23]

            spaces_to_display = add_spaces(30 - (amount_to_display.__len__()) - (description_to_display.__len__()))

            lines_of_deposits = lines_of_deposits.__add__(
                f"{description_to_display}{spaces_to_display}{amount_to_display}\n")

        return f"{line_of_name}{lines_of_deposits}Total: {self.get_balance()}"

    def deposit(self, amount, description: str = ""):
        self.ledger.append({"amount": amount, "description": description})

    def get_balance(self):
        balance: int = 0
        for deposit in self.ledger:
            balance = balance + deposit["amount"]
        return balance

    def withdraw(self, amount, description: str = ""):
        if self.get_balance() >= amount:
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        return True

    def get_total_spend(self):
        total = 0
        for deposit in self.ledger:
            if deposit["amount"] < 0:
                total = total + (-(deposit["amount"]))
        return total

    def transfer(self, amount, transfer_to):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {transfer_to.name}")
            transfer_to.deposit(amount, f"Transfer from {self.name}")
            return True
        else:
            return False


def create_spend_chart(categories: list):
    CategoryToShow.total = 0

    categories_classes = []

    for categorie in categories:
        categories_classes.append(CategoryToShow(categorie.name, categorie.get_total_spend()))

    for categori in categories_classes:
        categori.get_percentages()

    print(f"total spend = {CategoryToShow.total}\n")

    top_line = "Percentage spent by category"
    percentages_to_display = []
    percentages_to_display.append("100|")
    percentages_to_display.append(" 90|")
    percentages_to_display.append(" 80|")
    percentages_to_display.append(" 70|")
    percentages_to_display.append(" 60|")
    percentages_to_display.append(" 50|")
    percentages_to_display.append(" 40|")
    percentages_to_display.append(" 30|")
    percentages_to_display.append(" 20|")
    percentages_to_display.append(" 10|")
    percentages_to_display.append("  0|")

    middel_line = "    -"

    for i in categories:
        middel_line = middel_line + "---"



    for categories in categories_classes:
        for line in range(0, (percentages_to_display.__len__())):
            if int(percentages_to_display[line][0:3]) <= categories.percentage:
                percentages_to_display[line] = percentages_to_display[line] + " o "
            else:
                percentages_to_display[line] = percentages_to_display[line] + "   "


    max_length = 0
    for category in categories_classes:
        if category.name.__len__() > max_length:
            max_length = category.name.__len__()

    lines_of_the_name: list = []

    for i in range(max_length):
        lines_of_the_name.append("    ")

    for i in range(0, categories_classes.__len__()):
        for f in range(0, lines_of_the_name.__len__()):
            try:
                lines_of_the_name[f] += f" {categories_classes[i].name[f]} "
            except IndexError:
                lines_of_the_name[f] += "   "

    separation = " \n"

    result = f"{top_line}\n"
    result += separation.join(percentages_to_display)
    result += " "
    result += f"\n{middel_line}\n"
    result += separation.join(lines_of_the_name)
    result += " "

    #for line in percentages_to_display:
        #result = result + f"{line} \n"

    #result += f"{middel_line}\n"

    #for line in lines_of_the_name:
        #result = result + f"{line} \n"



    CategoryToShow.total = 0
    return result



class CategoryToShow:
    total: int = 0

    def __init__(self, name: str, total_spend: int):
        self.name = name
        self.total_spend = total_spend
        CategoryToShow.total += total_spend
        self.percentage = 0

    def get_percentages(self):
        print(f"{self.name}, total spend: {self.total_spend}")
        result = ((self.total_spend * 100) / CategoryToShow.total).__round__()
        self.percentage = result
        print(f"{self.name}, percentage: {self.percentage}")
        return result
