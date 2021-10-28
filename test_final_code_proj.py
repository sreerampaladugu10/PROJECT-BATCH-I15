import unittest
from intelxapi import intelx
import requests
import json
import hashlib
from tinydb import TinyDB, Query

db_checkemail = TinyDB('testcase_dbs/checkemail.json')
db_checkpassword = TinyDB('testcase_dbs/checkpassword.json')
db_generatepassword = TinyDB('testcase_dbs\generatepassword.json')

test_hashes = ['d00f5d5217896fb7fd601412cb890830', 'dc647eb65e6711e155375218212b3964']
test_emails = ['test@gmail.com', 'password@password.com', 'thisisatestemail@gmail.com', 'legituser123@yahoo.com', 'umimis@emvil.com']

crx = 0
option_selected = 0
intelx_api_key = ''
pass_lst = [8,'true','true','true']
intelx = intelx(intelx_api_key)


def check_email(mail):
    total_leaked = 0
    results = intelx.search(mail)
    stats = json.loads(intelx.stats(results))
    
    for stat_key in stats:
        #print(stat_key)
        total_leaked += stats[stat_key]
    return total_leaked


def check_password(passw):
    params = {'search' : passw, 
              'json' : 1}
    r = requests.get("https://api.dehash.lt/api.php?", params=params)
    results = json.loads(r.text)
    return results


def generatePassword(params_main):
    params_temp = {'len' : params_main[0],
              'num' : params_main[1],
              'char': params_main[2],
              'caps': params_main[3]}
    params = {k:v for k,v in params_temp.items() if v != 'false'}
    
    r = requests.get("https://passwordinator.herokuapp.com/generate?", params=params)
    results = json.loads(r.text)
    return results

# ─── TESTING MODULES ───────────────────────────────────────────────

class MainMethods(unittest.TestCase):
    
    def test_default_params_value(self):
        print("--------------------------------------------------------")
        print("testing globals")
        self.assertEqual (pass_lst, [8,'true','true','true'])
        self.assertEqual (intelx_api_key, '56aab44f-bfda-46a7-8c58-ae8294729394')
        
    def test_check_password(self):
        print("--------------------------------------------------------")
        print("testing check_password")
        temp_lst = db_checkpassword.all()
        output = check_password(test_hashes[0])
        self.assertEqual (output, temp_lst[0])
        output = check_password(test_hashes[1])
        self.assertEqual (output, temp_lst[1])

    def test_check_email(self):
        print("--------------------------------------------------------")
        print("testing check_email")
        temp_lst = db_checkemail.all()
        
        tester = list(temp_lst[0].keys())[0]
        output = check_email(test_emails[0])
        self.assertEqual (output, temp_lst[0][tester])
        
        tester = list(temp_lst[1].keys())[0]
        output = check_email(test_emails[1])
        self.assertEqual (output, temp_lst[1][tester])
        
        tester = list(temp_lst[2].keys())[0]
        output = check_email(test_emails[2])
        self.assertEqual (output, temp_lst[2][tester])
        
        tester = list(temp_lst[3].keys())[0]
        output = check_email(test_emails[3])
        self.assertEqual (output, temp_lst[3][tester])
        
        tester = list(temp_lst[4].keys())[0]
        output = check_email(test_emails[4])
        self.assertEqual (output, temp_lst[4][tester])                              

if __name__ == '__main__':
    unittest.main()
