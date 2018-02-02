'''
------------------------------- LICENSE ---------------------------------------
hardware_scripts; Basic scripts to validate my work in my hardware class
Copyright (C) 2018, Thomas Kercheval

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-------------------------------------------------------------------------------
'''
        # TODO: add testing framework
        # TODO: restructure to generate solution matrix (help test)
        # TODO: generate formatted result from solution matrix
class BooleanExpr(object):
    '''
    Class to parse boolean expressions and generate truth tables from them.
    Currently does not parse expressions of more than 6 variables
    (as on 1/Feb), due to its initial pupose of being a utility for a
    discord bot. This will probably change after some refactoring.

    From an expression, we translate it into postfix. This translation
    uses the shunting yard algorithm. After we have the postfix
    expression we cycle through every combination of inputs (2^n for n
    variables). The results are stored in a 2D-array, which then
    can be processed into a formatted form for display. The reason we
    need the intermediate 2D-array is because we need a way to write
    automated tests that doesn't depend on the formatted results.
    '''
    # Expression with whitespace stripped
    orig_exp = "empty"
    # How the expression will be displayed
    disp_exp = "empty"
    # Post-fix version of the original expression
    post_exp = ""
    # Set of all the variables
    var_set = set()
    # Stack needed to verify correctness of expr
    var_stack = []
    # Stack to manage operator precedence
    op_stack = []
    # The formatted truth table to be sent on discord
    result_formatted = ""
    # Flag and message in case an error occurs
    error = False
    error_msg = ""

    # Lists all the valid boolean operators
    boolean_ops = ['+', '^', '*', '!', '~']

    # Defines operator precedence
    prec_dict = {
        '!' : 0, # NOT
        '~' : 0, # NOT alias
        '*' : 1, # AND
        '^' : 2, # XOR
        '+' : 3, # OR
        '(' : 8,
        ')' : 9,
        -1  : 10 # op_stack is empty, skip
    }

    def __init__(self, exp):
        '''Initialize all values'''
        # Reset some stuff
        self.var_set.clear()
        self.op_stack[:] = []
        self.var_stack[:] = []
        self.error = False
        self.error_msg = ""

        # Process boolean expression, save original
        self.disp_exp = exp
        # Get rid of whitespace
        self.orig_exp = "".join(exp.split())
        self.get_rid_of_double_negation()
        # Create post-fix expression
        self.process_exp(self.orig_exp)

    def get_rid_of_double_negation(self):
        '''
        Remove any two adjacent negation operators. The function
        name really says it all.
        '''
        self.orig_exp = self.orig_exp.replace('!!', '')
        self.orig_exp = self.orig_exp.replace('~~', '')
        self.orig_exp = self.orig_exp.replace('~!', '')
        self.orig_exp = self.orig_exp.replace('!~', '')
        # Take care of `!~~!` edge case, maybe there's more?
        self.orig_exp = self.orig_exp.replace('!!', '')

    ######################################################################
    ####### Parse in-fix expression into post-fix ########################
    ######################################################################

    def process_exp(self, exp):
        """
        Processes an in-fix expression and saves a post-fix version
        of the expression on the class level. The post-fix expression
        is easier to evaluate in code and makes creating the truth
        table more efficient.
        """
        self.post_exp = ""
        # Step through chars of booelean expression
        for char in exp:
            if self.error:
                return
            if char == ' ':
                continue
            # Alphas are variables
            elif char.isalpha():
                self.var_set.add(char)
                self.var_stack.append(char)
                self.post_exp += char
            # Start parens
            elif char == '(':
                self.op_stack.append(char)
            # End parens
            elif char == ')':
                # Return if error processing parenthesis
                if not self.process_parenthesis():
                    return
            # If the char is a valid operator then process it
            elif self.is_valid_op(char):
                self.process_char(char)
            else:
                # we have found an invalid char
                self.error = True
                self.error_msg = "{} is not a valid symbol!".format(char)
        if self.error:
            return
        # Process remaining operators
        while self.op_stack and self.var_stack:
            if get_top(self.op_stack) == '(':
                self.error = True
                self.error_msg = "Unbalanced paren: ("
            self.process_an_op()

    def process_parenthesis(self):
        '''
        Processes all operators that occurs before a `)` parenthesis
        Stops once it hits a `(`, else results in error and returns False
        '''
        while get_top(self.op_stack) != '(':
            self.process_an_op()
            if get_top(self.op_stack) == -1:
                self.error = True
                self.error_msg = "Unbalanced paren: )"
                return False
        # Pop start paren
        if self.op_stack:
            self.op_stack.pop()
        return True

    def is_valid_op(self, char):
        '''True if char is a valid boolean operator'''
        return char in self.boolean_ops

    def process_char(self, char):
        '''Processes a single operator'''
        # Get the precedence of the operator
        prec = self.prec_dict[char]
        # Process all operators with higher precedence
        # (high precedence is indicated with a lower number, sorry)
        while prec >= self.prec_dict[get_top(self.op_stack)]:
            self.process_an_op()
        self.op_stack.append(char)

    def process_an_op(self):
        '''
        Processes a single operator. Adds thise operator to the postfix
        expression and modify the variable stack accordingly.
        Checks for errors dealing with the size of these stacks.
        '''
        # I don't know if this would happen...
        if not self.op_stack:
            self.error = True
            self.error_msg = "Op stack is empty while trying to process op"
            return
        # Add operator to postfix expression
        operator = get_top(self.op_stack)
        self.post_exp += operator
        self.op_stack.pop()
        # If the operator is unary, then there will be no change in var_stack
        if operator != '!' and operator != '~':
            if len(self.var_stack) < 2:
                self.error = True
                self.error_msg = "Too many operators!"
                return
            self.var_stack.pop()
            self.var_stack.pop()
            self.var_stack.append("NUL")

    ######################################################################
    ####### Process all input permutations using the post-fix expr #######
    ######################################################################

    def process_all_exps(self):
        '''
        Process every possible permutation of inputs. Creates the final
        formatted result by recursively considering every possible
        combination of True and False for every variable and processing
        the postfix expression with those inputs.
        '''
        self.result_formatted = ""
        # Get all variables, sort them to ensure consistent tables between runs
        var_list = []
        for elem in self.var_set:
            var_list.append(elem)
        var_list.sort()
        var_num = 0
        # This dictionary will keep track of the value of each variable
        var_dict = {}
        self.format_header(var_list)

        # Begin recursion
        var_dict[var_list[var_num]] = False
        self.recurse_through_var(var_list, var_dict, var_num + 1)
        var_dict[var_list[var_num]] = True
        self.recurse_through_var(var_list, var_dict, var_num + 1)

        # Add bottom line of formatted result
        self.result_formatted += "+" + "---+" * len(var_list)
        self.result_formatted += "-" * len(self.disp_exp) + "--+\n"

    def recurse_through_var(self, var_list, var_dict, depth):
        '''
        Recurse until every variable has been set to True or False, then
        once the recursion depth is equal to the number of variables
        process the expression by passing in the dictionary which is
        keeping track of the value of each variable
        '''
        if depth >= len(self.var_set):
            # Process expression for a single permutation of input
            self.process_single_exp(var_dict, var_list)
        else:
            # Continue recursion
            var_dict[var_list[depth]] = False
            self.recurse_through_var(var_list, var_dict, depth + 1)
            var_dict[var_list[depth]] = True
            self.recurse_through_var(var_list, var_dict, depth + 1)

    def process_single_exp(self, dict_bool, var_list):
        '''
        Processes a post-fix expression with the values of each variable
        stroed in `dict_bool`.
        '''
        post_stack = []
        for char in self.post_exp:
            if char.isalpha():
                # Append value of that variable to the stack
                post_stack.append(dict_bool[char])
            elif char in self.prec_dict:
                # Compute result and add it back to stack
                if char == '!' or char == '~':
                    one = not post_stack.pop()
                    post_stack.append(one)
                if char == '*':
                    one = post_stack.pop()
                    two = post_stack.pop()
                    result = one and two
                    post_stack.append(result)
                if char == '+':
                    one = post_stack.pop()
                    two = post_stack.pop()
                    result = one or two
                    post_stack.append(result)
                if char == '^':
                    one = post_stack.pop()
                    two = post_stack.pop()
                    result = bool(one) ^ bool(two)
                    post_stack.append(result)
        # Save result in a formatted fashion, will be single line in table
        self.format_result(post_stack.pop(), dict_bool, var_list)

    def format_header(self, var_list):
        '''Creates the header to the truth table'''
        self.result_formatted += "+" + "---+" * len(var_list)
        self.result_formatted += "-" * len(self.disp_exp) + "--+\n"
        for var in var_list:
            self.result_formatted += "| {} ".format(var)
        self.result_formatted += "| {} |\n".format(self.disp_exp)
        self.result_formatted += "+---" * len(var_list)
        self.result_formatted += "+" + "-" * len(self.disp_exp) + "--+\n"

    def format_result(self, result, dict_bool, var_list):
        '''Creates single line in the truth table'''
        for var in var_list:
            booly = int(dict_bool[var])
            self.result_formatted += "| {} ".format(booly)
        res = int(result)
        self.result_formatted += "| {}".format(res)
        self.result_formatted += " " * len(self.disp_exp) + "|\n"

    def valid_vars(self):
        '''False if there are two vars right next to each other'''
        for i in range(1, len(self.orig_exp)):
            if self.orig_exp[i].isalpha() and self.orig_exp[i - 1].isalpha():
                return False
        return True

    def valid_negation(self):
        '''False if operator! is placed incorrectly'''
        not_list = ['!', '~']
        for i in range(1, len(self.orig_exp)):
            if self.orig_exp[i] in not_list and self.orig_exp[i - 1].isalpha():
                self.error_msg = "! should come before a variable, not after."
                return False
            if self.orig_exp[i] in not_list and self.orig_exp[i - 1] == ')':
                self.error_msg = "'!' should not follow a ')'"
                return False
        return True

    def get_truth_table(self):
        '''Returns formatted version of the truth table for a boolean expr'''
        if not self.valid_vars():
            self.error = True
            self.error_msg = "Cannot have two variables in a row..."
        if not self.valid_negation():
            self.error = True
        if self.error:
            return "The expression: {}, is invalid!\n{}".format(self.disp_exp,
                                                                self.error_msg)
        if len(set(self.var_set)) > 5:
            return "Too many variables! Will result in spam..."
        # print("Variable set: {}".format(self.var_set))
        # # print(self.op_stack)
        # print("\nIn-fix:   {}".format(self.orig_exp))
        # print("Post-fix: {}".format(self.post_exp))
        self.process_all_exps()
        return self.result_formatted

def get_top(arr):
    '''
    If there are elements in the stack, return the top of the stack,
    else return -1 to signify that the stack is empty
    '''
    if not arr:
        return -1
    return arr[-1]

# Run some basic tests
if __name__ == '__main__':
    EXP = "A+C"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "A*C"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "A^C+!(A * C)"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "A+!B*C+!A*C*!D"
    EXP_OBJ_2 = BooleanExpr(EXP)
    print(EXP_OBJ_2.get_truth_table())

    EXP = "A^C++!(A * C)"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "A^C+!((A * C)"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "A^C)++!(A * C))"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "A^C++!(A * C))"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "ABCD"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "!(x + y)"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "(x!y + y)"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "(x + y)!"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "(!!x + y)"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "(!+!x + y)"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "!(!(!x + y))"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())

    EXP = "!   !   !x + y"
    EXP_OBJ = BooleanExpr(EXP)
    print(EXP_OBJ.get_truth_table())
