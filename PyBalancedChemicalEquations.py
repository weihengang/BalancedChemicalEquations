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
def format_equation(equation):
    inputs_LHS = []
    inputs_RHS = []
    LHS_terms = []
    RHS_terms = []
    equation = equation.replace(" ", "")
    LHS, RHS = equation.split("→")
    for i in LHS.split("+"):
        inputs_LHS.append(i)
        LHS_terms.append(extract_element_data(i))
    for i in RHS.split("+"):
        inputs_RHS.append(i)
        RHS_terms.append(extract_element_data(i))
    return (inputs_LHS, inputs_RHS, LHS_terms, RHS_terms)
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
def find_connection():
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
    zero_num = 1000
    return_dict = None
    for j in range(0, len(LHS_terms)):
        dict_term_coefficient = {}
        for i in range(0, len(LHS_terms)):
            term = LHS_terms[i]
            if (i == j):
                dict_term_coefficient[term] = 1.0 #seed
            else:
                dict_term_coefficient[term] = 0 #set to zero at the start, changed after second step
        for i in RHS_terms:
            dict_term_coefficient[i] = 0
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
        list_coefficient = list(dict_term_coefficient.values())
        zero_count = list_coefficient.count(0)
        if (zero_count < zero_num):
            zero_num = zero_count
            return_dict = dict_term_coefficient
    assert type(return_dict) == dict
    return return_dict #value with the most solved terms (when there are unlinked connections)
def find_repeated_element(list_terms):
    dict_repeated = {} #element, term of element
    for term in list_terms:
        for element in term.list_Element:
            str_element = element.str_element
            if (str_element in dict_repeated):
                term_count = dict_repeated[str_element]
                term_count[0].append(term)
                term_count[1] += 1
                dict_repeated[str_element] = term_count
            else: 
                dict_repeated[str_element] = [[term], 1]
    list_remove = []
    for str_element in dict_repeated:
        term_count = dict_repeated[str_element]
        if (term_count[1] == 1):
            list_remove.append(str_element)
    for i in list_remove:
        del dict_repeated[i]
    for str_element in dict_repeated:
        term_count = dict_repeated[str_element]
        dict_repeated[str_element] = term_count[0]
    return dict_repeated
def create_linear_equations(dict_repeated): 
    dict_equations = {}
    for str_element in dict_repeated:
        list_term = dict_repeated[str_element]
        dict_equations[str_element] = []
        for term in list_term:
            assert type(term) == Term
            list_Element = term.list_Element
            subscript = None
            for element in list_Element:
                if (element.str_element == str_element):
                    subscript = element.amount
                    break
            else:
                raise Exception("ERROR: str_element CANNOT BE FOUND (u fked up)")
            if (term.num_molecules != 0): #solved previously with the unique element algorithm
                dict_equations[str_element].append(str(term.num_molecules * subscript))
            else: #unsolved coefficient, ggs
                dict_equations[str_element].append((f"{subscript}x", term))
    return dict_equations
def solve_linear_equation(equation): 
    #NOT MY CODE - solve_linear_equation() TAKEN FROM GEEKSFORGEEKS
    s1 = equation.replace('x', 'j') 
    s2 = s1.replace('=', '-(') 
    s = s2 + ')'
    z = eval(s, {'j': 1j}) 
    real, imag = z.real, -z.imag 
    if imag: 
        return real / imag
def format_linear_equations(dict_A, dict_B):
    #solve element by element
    list_solutions = []
    for str_element in dict_A:
        list_LHS = dict_A[str_element]
        list_RHS = dict_B[str_element]
        str_equation = ""
        x_count = 0
        term_value = None
        for i in range(0, len(list_LHS)):
            tuple_str = list_LHS[i]
            equation_term = ""
            if (type(tuple_str) == tuple):
                term_value = tuple_str[1]
                x_count += 1
                equation_term = tuple_str[0]
            else:
                equation_term = tuple_str
            if (i == len(list_LHS) - 1):
                str_equation += equation_term
            else:
                str_equation += f"{equation_term}+"
        str_equation += "="
        for i in range(0, len(list_RHS)):
            tuple_str = list_RHS[i]
            equation_term = ""
            if (type(tuple_str) == tuple):
                term_value = tuple_str[1]
                x_count += 1
                equation_term = tuple_str[0]
            else:
                equation_term = tuple_str
            if (i == len(list_RHS) - 1):
                str_equation += equation_term
            else:
                str_equation += f"{equation_term}+"
        if (not x_count == 1):
            continue
        coefficient_value = solve_linear_equation(str_equation)
        list_solutions.append((coefficient_value, term_value))
    return list_solutions
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
def same_term(term_1, term_2):
    if (term_1.list_Element == term_2.list_Element):
        return True
    return False
def solutions_link(list_connections):
    import copy as c
    combined_terms = c.deepcopy(LHS_terms)
    combined_terms.extend(RHS_terms)
    term_coefficient = {}
    for term in combined_terms:
        if (not term.num_molecules == 0):
            continue
        LHS_RHS = (combined_terms.index(term) < len(LHS_terms)) #if LHS, True else RHS, False
        for connection in list_connections:
            assert type(connection) == Connection
            if (same_term(term, connection.Term_1) or same_term(term, connection.Term_2)):
                if (LHS_RHS):
                    Term_2 = connection.Term_2
                    RHS_term = None
                    for RHS_term_loop in RHS_terms: #updated RHS_terms are no longer equal to connection.Term_2
                        if (same_term(Term_2, RHS_term_loop)):
                            RHS_term = RHS_term_loop
                            break
                    assert RHS_term != None
                    num_molecules = RHS_term.num_molecules
                    if (num_molecules == 0): #cannot solve
                        continue
                    coefficient = num_molecules / connection.ratio[0] * connection.ratio[1]
                    term_coefficient[term] = coefficient #solved
                    break
                else:
                    Term_1 = connection.Term_1
                    LHS_term = None
                    for LHS_term_loop in LHS_terms: #updated RHS_terms are no longer equal to connection.Term_2
                        if (same_term(Term_1, LHS_term_loop)):
                            LHS_term = LHS_term_loop
                            break
                    assert LHS_term != None
                    num_molecules = LHS_term.num_molecules
                    if (num_molecules == 0): #cannot solve
                        continue
                    coefficient = num_molecules / connection.ratio[1] * connection.ratio[0]
                    term_coefficient[term] = coefficient #solved
                    break
        #cannot solve, skip to next term
    return term_coefficient
"""
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
"""
equation = input("Enter equation: ")
inputs_LHS, inputs_RHS, LHS_terms, RHS_terms = format_equation(equation)
list_connections = find_connection()
coefficients = set_value(list_connections)
list_coefficients = list(coefficients.values())
print(f"list_coefficients (STEP ONE APPLIED): {list_coefficients}")
for j in range(0, 10):
    if (not 0 in list_coefficients):
        break
    #update num_molecules after each iteration
    for i in range(0, len(list_coefficients)):
        if (i >= len(LHS_terms)):
            RHS_terms[i - len(LHS_terms)].num_molecules = list_coefficients[i]
        else:
            LHS_terms[i].num_molecules = list_coefficients[i]
    LHS_equations = create_linear_equations(find_repeated_element(LHS_terms))
    RHS_equations = create_linear_equations(find_repeated_element(RHS_terms))
    list_solutions = format_linear_equations(LHS_equations, RHS_equations)
    for i in list_solutions:
        coefficient_value, term_value = i
        term_value.num_molecules = coefficient_value
        list_coefficients[list(coefficients.keys()).index(term_value)] = coefficient_value   
else: #still not solved
    print(f"list_coefficients (STEP TWO APPLIED): {list_coefficients}")
    #step three, applying step one on the data from step two
    term_coefficient = solutions_link(list_connections)
    for i in term_coefficient:
        coefficient = term_coefficient[i]
        if (i in LHS_terms):
            index = LHS_terms.index(i)
            LHS_terms[index].num_molecules = coefficient
            list_coefficients[index] = coefficient
        if (i in RHS_terms):
            index = RHS_terms.index(i)
            RHS_terms[RHS_terms.index(i)].num_molecules = coefficient
            list_coefficients[len(LHS_terms) + index] = coefficient
    print(f"list_coefficients (STEP THREE APPLIED): {list_coefficients}")
    if (0 in list_coefficients):
        print("Program is unable to balance the chemical equation.")
        quit()
list_coefficients = format_coefficients(list_coefficients)
str_return = ""
for i in range(0, len(inputs_LHS)):
    term = inputs_LHS[i]
    coefficient = list_coefficients[i]
    if (i == len(inputs_LHS) - 1):
        str_return += f"{coefficient}_{term} "
    else:
        str_return += f"{coefficient}_{term} + "
str_return += "-> "
for i in range(0, len(inputs_RHS)):
    term = inputs_RHS[i]
    coefficient = list_coefficients[len(inputs_LHS) + i]
    if (i == len(inputs_RHS) - 1):
        str_return += f"{coefficient}_{term} "
    else:
        str_return += f"{coefficient}_{term} + "
print(f"Balanced chemical equation: {str_return}")
