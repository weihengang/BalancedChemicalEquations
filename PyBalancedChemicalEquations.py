import random as r
class Element:
    def __init__(self, str_element, amount):
        self.str_element = str_element
        self.amount = int(amount)
    def __repr__(self):
        return f"|{self.str_element}, {self.amount}|"
class Term:
    def __init__(self, num_molecules, list_Element):
        self.num_molecules = int(num_molecules)
        self.list_Element = list_Element
    def __repr__(self):
        return f"({self.num_molecules}, {self.list_Element})"
class Connection:
    def __init__(self, Term_1, Term_2, ratio):
        assert type(Term_1) == Term
        assert type(Term_2) == Term
        self.Term_1 = Term_1
        self.Term_2 = Term_2
        self.ratio = ratio
    def __repr__(self):
        return f"{self.Term_1}, {self.Term_2} = [{self.ratio}]"
class Number:
        def __init__(self, number, start_ind, stop_ind):
            self.number = number
            self.start_ind = start_ind
            self.stop_ind = stop_ind
        def __repr__(self):
            return f"({self.number}, {self.start_ind}, {self.stop_ind})"
def format_str(str_term):
    if (not str_term[0].isnumeric()):
        str_term = "0" + str_term
    for j in range(0, 100): #will break out early
        for i in range(0, len(str_term)):
            char = str_term[i]
            if (i == len(str_term) - 1):
                if (char.isalpha()):
                    str_term += "1"
                break
            next_char = str_term[i + 1]
            if (char.isalpha()):
                if (next_char.isalpha() and next_char.isupper()): #insert 1 
                    str_front = str_term[:i + 1]
                    str_end = str_term[i + 1:]
                    str_term = str_front + "1" + str_end
                    break
        else:
            break
    return str_term
def extract_number(str_term):
    list_Number = []
    search_flag = False
    number = ""
    start_index = 0
    for i in range(0, len(str_term)):
        char = str_term[i]
        is_number = char.isnumeric()
        if (is_number and not search_flag):
            if (i == len(str_term) - 1): #edge case when the last char is a number, but not the one before -> H1
                list_Number.append(Number(char, i, i))
                break
            search_flag = True
            number = char
            start_index = i
            continue
        if (search_flag):
            if (is_number):
                number += char
                if (i == len(str_term) - 1):
                    list_Number.append(Number(number, start_index, i)) #edge case where last few chars are numbers
                continue
            else:
                search_flag = False
                list_Number.append(Number(number, start_index, i - 1))
                number = ""
    return list_Number
def extract_element_data(str_term):
    str_term = format_str(str_term) 
    list_Element = []
    list_Number = extract_number(str_term)
    list_element = []
    for i in range(0, len(list_Number) - 1): #ignore the last number
        class_number = list_Number[i]
        next_class_number = list_Number[i + 1]
        element_str = str_term[class_number.stop_ind + 1:next_class_number.start_ind]
        list_element.append(element_str)
    for i in range(1, len(list_Number)):
        list_Element.append(Element(list_element[i - 1], list_Number[i].number))
    return Term(list_Number[0].number, list_Element)
def compare_lists(list_1, list_2):
    similar_values = []
    for i in list_1:
        if (i in list_2):
            similar_values.append(i)
    return similar_values
def find_different_elements(list_term):
    list_different_elements = []
    dictionary_different_elements = {}
    for i in list_term:
        assert type(i) == Term
        list_Element = i.list_Element
        for j in list_Element:
            assert type(j) == Element
            element = j.str_element   
            if (element in list_different_elements):
                dictionary_different_elements.pop(element)
                list_different_elements.remove(element)
            else:
                list_different_elements.append(element)
                dictionary_different_elements[element] = i
    return (list_different_elements, dictionary_different_elements)
def find_correlation():
    #find the unique elements on each side, then make a connection between the terms
    LHS_different_elements, LHS_different_elements_terms = find_different_elements(LHS_terms)
    RHS_different_elements, RHS_different_elements_terms = find_different_elements(RHS_terms)
    connection = compare_lists(LHS_different_elements, RHS_different_elements)
    list_connection = []
    for i in connection:
        Term_1 = LHS_different_elements_terms[i]
        Term_2 = RHS_different_elements_terms[i]
        assert type(Term_1) == Term and type(Term_2) == Term
        Term1_list_Element = Term_1.list_Element
        Term2_list_Element = Term_2.list_Element
        ratio_1 = None
        ratio_2 = None
        for element in Term1_list_Element: #Element class
            if (element.str_element == i):
                ratio_1 = element.amount
        for element in Term2_list_Element:
            if (element.str_element == i):
                ratio_2 = element.amount
        list_connection.append(Connection(Term_1, Term_2, (ratio_1, ratio_2)))
    return list_connection
def set_value(list_connection):
    dict_term_coefficient = {}
    for i in range(0, len(LHS_terms)):
        term = LHS_terms[i]
        if (i != 0):
            dict_term_coefficient[term] = 0
        else:
            dict_term_coefficient[term] = 1 #seed
    for i in RHS_terms:
        dict_term_coefficient[i] = 0
    for j in range(0, 100):
        for i in list_connection: #Connection class
            term_1 = i.Term_1
            term_2 = i.Term_2
            ratio = i.ratio
            term_1_coefficient = dict_term_coefficient[term_1]
            term_2_coefficient = dict_term_coefficient[term_2]
            if (term_1_coefficient != 0 and term_2_coefficient == 0):
                term_2_coefficient = term_1_coefficient / ratio[1] * ratio[0]
            if (term_2_coefficient != 0 and term_1_coefficient == 0):
                term_1_coefficient = term_2_coefficient / ratio[0] * ratio[1]
            dict_term_coefficient[term_1] = term_1_coefficient
            dict_term_coefficient[term_2] = term_2_coefficient
        #randomize dict_term_coefficient item order
        r.shuffle(list_connection)
    return dict_term_coefficient
def convert_int(number, return_boolean = False):
    str_number = str(number)
    flag = False
    for chr in str_number:
        if (chr == "."):
            flag = True
            continue
        if (flag == True and chr != "0"):
            #cannot convert to integer
            #if (return_boolean):
            #    return True
            return number
    #if (return_boolean):
    #    return False
    return int(number)
def format_coefficients(list_coefficients):
    multiply_data = []
    for i in list_coefficients:
        if (i < 1):
            multiply_data.append(i)
    for data in multiply_data:
        for i in range(0, len(list_coefficients)):
            value = list_coefficients[i]
            list_coefficients.pop(i)
            list_coefficients.insert(i, value / data)
    for i in range(0, len(list_coefficients)):
        value = list_coefficients[i]
        list_coefficients.pop(i)
        list_coefficients.insert(i, convert_int(value))
    return list_coefficients
LHS_terms = []
RHS_terms = []
inputs_LHS = []
inputs_RHS = []
for i in range(0, int(input("Enter number of terms in LHS: "))):
    str_term = input(f"Enter term at position {i + 1}: ")
    inputs_LHS.append(str_term)
    LHS_terms.append(extract_element_data(str_term))
for i in range(0, int(input("Enter number of terms in RHS: "))):
    str_term = input(f"Enter term at position {i + 1}: ")
    inputs_RHS.append(str_term)
    RHS_terms.append(extract_element_data(str_term))
coefficients = set_value(find_correlation())
list_coefficients = format_coefficients(list(coefficients.values()))
str_return = ""
for i in range(0, len(inputs_LHS)):
    term = inputs_LHS[i]
    coefficient = list_coefficients[i]
    if (i == len(inputs_LHS) - 1):
        str_return += f"{coefficient}{term} "
    else:
        str_return += f"{coefficient}{term} + "
str_return += "-> "
for i in range(0, len(inputs_RHS)):
    term = inputs_RHS[i]
    coefficient = list_coefficients[len(inputs_LHS) + i]
    if (i == len(inputs_RHS) - 1):
        str_return += f"{coefficient}{term} "
    else:
        str_return += f"{coefficient}{term} + "
print(str_return)