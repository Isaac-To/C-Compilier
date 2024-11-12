import re
import logging

# logging.basicConfig(level=logging.DEBUG)

# perform the local value numbering optimization
def LVN(program):

    # returns 3 items:
    
    # 1. a new program (list of classier instructions)
    # with the LVN optimization applied

    # 2. a list of new variables required (e.g. numbered virtual
    # registers and program variables)

    # 3. a number with how many instructions were replaced

    new_program = []
    new_variables = []
    num_replaced = 0

    equiv = {}
    table = {}
    new_vr_index = 0

    for line in program:
        match = re.match(r"(\S+) = (\S+)\((\S+),(\S+)\);", line)
        if match:
            # Reduce arithmetic instructions
            dest, op, arg1, arg2 = match.groups()
            logging.debug("ARITH: dest: %s, op: %s, arg1: %s, arg2: %s", dest, op, arg1, arg2)
            if (op, arg1, arg2) in table:
                if dest != table[(op, arg1, arg2)]:
                    new_program.append("%s = %s;" % (dest, table[(op, arg1, arg2)]))
                num_replaced += 1
            else:
                if dest in table.values():
                    dest = "nvr%d" % new_vr_index
                    new_vr_index += 1
                    new_variables.append(dest)
                new_program.append(f"{dest} = {op}({arg1},{arg2});")
                table[(op, arg1, arg2)] = dest
        else:
            new_program.append(line)
        # else:
        #     # Reduce conversion instructions
        #     match = re.match(r"(\S+) = (\S+)\((\S+)\);", line)
        #     if match:
        #         dest, op, arg = match.groups()
        #         logging.debug("CONV: dest: %s, op: %s, arg: %s", dest, op, arg)
        #         if (op, arg) in table:
        #             if dest != table[(op, arg)]:
        #                 new_program.append("%s = %s;" % (dest, table[(op, arg)]))
        #             num_replaced += 1
        #         else:
        #             if re.match(r"vr\d+", dest) and dest in table.values():
        #                 dest = "nvr%d" % new_vr_index
        #                 new_vr_index += 1
        #                 new_variables.append(dest)
        #             new_program.append(f"{dest} = {op}({arg});")
        #             table[(op, arg)] = dest
        #     else:
        #         new_program.append(line)
        # Line Reduction - remove redundant assignments
        # match = re.match(r"(vr\d+) = (vr\d+);", new_program[-1])
        # if match:
        #     dest, src = match.groups()
        #     if equiv.get(dest) == src:
        #         new_program.pop()
        #         num_replaced += 1
        #     else:
        #         equiv[dest] = src
        

    return new_program,new_variables,num_replaced
