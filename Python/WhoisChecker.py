import subprocess
import time

# tested only on Ubuntu, requires 'whois' to work
#

# fully supported Domains:
#TLDs = ['.com', '.org', '.net']
# partially supported domains (checks if they are available):
#TLDs = ['.com', '.it', '.net', '.eu', '.nl', '.de', '.cz', '.io']
TLDs = ['.com']

# generate numeric domain names
def generate_names(min:int, max:int, prefix:str = '', suffix:str ='') -> list:
    if min > max:
        print("<min> must be smaller than <max>")
        exit(-1)

    result = []
    for i in range(min, max+1):
        result.append(prefix + str(i) + suffix)
    return result

# returns response from whois
def whois_request(domain: str) -> str:
    result = subprocess.run(['whois', domain], stdout=subprocess.PIPE)
    result = str(result.stdout)
    return result

# returns True when domain is available
def check_availability(whois_response: str, tld: str) -> bool:

    match tld:
        case '.com':
            if 'Name Server:' in whois_response:
                return False
            else:
                return True
        case '.pl':
            if 'nameservers:' in whois_response:
                return False
            else:
                return True

        case '.it':
            if 'Nameservers' in whois_response or 'UNASSIGNABLE' in whois_response:
                return False
            else:
                return True

        case '.cz':
            if 'nserver:' in whois_response:
                return False
            else:
                return True

        case '.io':
            if 'Name Server:' in whois_response or 'This platinum domain' in whois_response:
                return False
            else:
                return True
        case '.net':
            if 'Name Server:' in whois_response:
                return False
            else:
                return True

        case '.eu':
            if 'Name servers:' in whois_response:
                return False
            else:
                return True
        case '.nl':
            if "nameservers:" in whois_response:
                return False
            else:
                return True
        case '.de':
            if "Nserver:" in whois_response:
                return False
            else:
                return True
        case '.org':
            if "Creation Date:" in whois_response:
                return False
            else:
                return True
        case  _:
            print("TLD not implemented")
            exit(-1)

# only .com, .net and .org are implemented
def check_whois_for_dates(whois_response: str, name: str, tld: str) -> str:
    result = []
    result.append(name)
    result.append(tld)
    match tld:
        case '.com':
            idx = whois_response.find('Creation Date:')
            result.append(whois_response[idx+15:idx+25]+" "+whois_response[idx+26:idx+34])
            idx = whois_response.find('Updated Date:')
            result.append(whois_response[idx+14:idx+24]+" "+whois_response[idx+25:idx+33])
            if 'Expiration Date:' in whois_response:
                idx = whois_response.find('Expiration Date:')
                result.append(whois_response[idx+17:idx+27]+" "+whois_response[idx+28:idx+36])
            else:
                idx = whois_response.find('Expiry Date:')
                result.append(whois_response[idx+13:idx+23]+" "+whois_response[idx+24:idx+32])

        case '.net':
            idx = whois_response.find('Creation Date:')
            result.append(whois_response[idx+15:idx+25]+" "+whois_response[idx+26:idx+34])
            idx = whois_response.find('Updated Date:')
            result.append(whois_response[idx+14:idx+24]+" "+whois_response[idx+25:idx+33])
            if 'Expiration Date:' in whois_response:
                idx = whois_response.find('Expiration Date:')
                result.append(whois_response[idx+17:idx+27]+" "+whois_response[idx+28:idx+36])
            else:
                idx = whois_response.find('Expiry Date:')
                result.append(whois_response[idx+13:idx+23]+" "+whois_response[idx+24:idx+32])

        case '.org':
            idx = whois_response.find('Creation Date:')
            result.append(whois_response[idx+15:idx+25]+" "+whois_response[idx+26:idx+34])
            idx = whois_response.find('Updated Date:')
            result.append(whois_response[idx+14:idx+24]+" "+whois_response[idx+25:idx+33])
            if 'Expiration Date:' in whois_response:
                idx = whois_response.find('Expiration Date:')
                result.append(whois_response[idx+17:idx+27]+" "+whois_response[idx+28:idx+36])
            else:
                idx = whois_response.find('Expiry Date:')
                result.append(whois_response[idx+13:idx+23]+" "+whois_response[idx+24:idx+32])

        case _:
            print('TLD not implemented')
            exit()
    result = ';'.join(result)
    return result



# generating CSV entries with dates when domain:
# was egistered
# was updated
# is going to expire
# ;0;0;0 - available / deletion pending
def pretty_print_availability(name: str, tlds: list) -> str:
    result = []
    first_time = True
    for tld in tlds:
        whois_req = whois_request(name+tld)
        if check_availability(whois_req, tld):  ## appending empty columns
            result.append(name+';'+tld + ";0;0;0")
        else:
            result.append(check_whois_for_dates(whois_req,name,tld))

    return '\n'.join(result)

# writes availbility to file
def write_availability(names: list, tlds: list, filename:str = 'domains.txt'):
    file = open(filename, 'w')
    file.close()
    for name in names:
        print("checking "+name+".*")
        time.sleep(3)
        check = pretty_print_availability(name, tlds)
        if check != '':
            file = open(filename, 'a')
            file.write(check+"\n")
            file.close()


# ====================================================
#              \/ you can edit these \/


test_names = ['cloudmate', 'abc123qwererwrewrwerwe']
#write_availability(generate_names(<start>, <end>, <prefix(optional)>), TLDs, <output_file>)
write_availability(generate_names(10,999), TLDs,   'com-domains-10-999.csv')
write_availability(generate_names(1,99,'0'), TLDs, 'com-domains-01-099.csv')
write_availability(generate_names(1,9,'00'), TLDs, 'com-domains-001-009.csv')
