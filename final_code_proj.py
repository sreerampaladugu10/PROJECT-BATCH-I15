import json
import requests 
import subprocess 
import hashlib 
from rich import print, box
from rich.progress import track, Progress
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
import animation
import time 
import re 
from os import system, name, path 
from intelxapi import intelx 
import pyhibp 
from pyhibp import pwnedpasswords as pw
#Needs holehe and sherlock to be installed

# ─── DEFINING CRX RATING FOR EACH PARAMETER WE TEST ─────────────────────────────


'''
1. 0 < CrX < 1
2. If CrX >= 1; CrX = 1;
3. 0 < CrX < 0.4 = Good; CrX = 0.4 (Still suggest update)
    0.4 < CrX < 0.6 = Fair; CrX = 0.6 (Suggest lookin into passwords)
    0.6 < CrX < 0.8 = Unfair; CrX = 0.8 (Major breachs, change immediately)
    0.8 < CrX < 1 || CrX >= 1 = Bad; CrX = 1 (Change immediately, suggest using password generator and manager)
4. Found in leaks = +0.6
    No Special Chars = +0.4
    Same name as email/username = +0.8
    Password Cracked = 1
'''


# ─── GLOBAL VARIABLES ───────────────────────────────────────────────────────────


crx = 0
#wait = animation.Wait()
option_selected = 0
intelx_api_key = ''
buffer = 0
SPECIAL_CHARS = '[@_!#$%^&*()<>?/\|}{~:]'
cmd = 'python cupp.py -i'
pass_lst = [8,'true','true','true']
pyhibp.set_user_agent(ua="OSINT_MINI_PROJ/0.0.1 (Sample Test OSINT APP)")
check_char = '[+]'
count_reg = 0

# ─── DEFINING NECESARY FUNCTIONS AND CLASSES ────────────────────────────────────


intelx = intelx(intelx_api_key)

def consoleClear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def check_email(mail):
    total_leaked = 0
    results = intelx.search(mail)
    stats = json.loads(intelx.stats(results))
    
    for stat_key in stats:
        #print(stat_key)
        total_leaked += stats[stat_key]
    return total_leaked

def check_password(password):
    params = {'search' : password, 
              'json' : 1}
    r = requests.get("https://api.dehash.lt/api.php?", params=params)
    results = json.loads(r.text)
    return results

def generatePassword(param_lst):
    params_temp = {'len' : param_lst[0],
              'num' : param_lst[1],
              'char': param_lst[2],
              'caps': param_lst[3]}
    params = {k:v for k,v in params_temp.items() if v != 'false'}
    
    r = requests.get("https://passwordinator.herokuapp.com/generate?", params=params)
    results = json.loads(r.text)
    return results


# ────────────────────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────
# ─── WELCOME SCREEN AND OPTIONS MENU ────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────


print("\n----------------------------------------------------------------")
print("[magenta]Welcome to the sample script, Here are your [bold]options[/bold]: \n[aquamarine]1. Check online presence strength :muscle:[/aquamarine]\n[red]2. Suggest a random strong password :closed_lock_with_key:[/red]\n3. INTERNAL TESTING\n")
option_selected = int(input())
consoleClear()


# ────────────────────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────
# ─── CHECKING PASSWORD STRENGTH ─────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────


if option_selected == 1:

    print("\n----------------------------------------------------------------")
    print("-- Questionnaire to get to get know you better! -- \n")
    input("Press Enter to Continue...")
    consoleClear()
    
    print("\n----------------------------------------------------------------")
    print("--Enter Your [magenta][bold]E-Mail[/bold][/magenta]-- ")
    email_inp = str(input())
    print("--Enter Your [blue][bold]Password[/bold][/blue]-- ")
    password_inp = str(input())
    print("--Enter Your [green][bold]First Name[/bold][/green]-- (To verify with later questions)")
    username_inp = str(input()).lower()
    print("--Enter Your [green][bold]Username[/bold][/green]--")
    sherlock_inp = str(input())
    print("\n----------------------------------------------------------------")
    
    print("Continuing with the user profiling...")
    print("You can skip any question by not inputting any value, We suggest not skipping the initial 4 questions")
    input("Press Enter to Continue...")
    
    consoleClear()
    
    p = subprocess.run(cmd, shell=True)
    
    consoleClear()    
    
    if path.exists(f"{username_inp}.txt"):
        pass
    else:
        print("\n----------------------------------------------------------------")
        print("You messed up the questionaire, Restart the application again")
        input("Press Enter to Continue...")
        exit()
        
    cmd_sherlock = f'python sherlock/sherlock/sherlock.py --timeout 10 {sherlock_inp}'
    cmd_holehe = f'holehe {email_inp}'
    
    # ─── PARAM1: CHECKING FOR EMAIL-PASSWORD LEAKS ──────────────────────────────────────────
    
    
    print("[red]Checking for E-Mail/Password in Leaks[/red]")
    
    with Progress() as progress:

        task2 = progress.add_task("[red]Checking...", total=1000)
    
        while not progress.finished:
            progress.update(task2, advance=9)
            time.sleep(0.02)
    total_leaked = check_email(email_inp)
    resp = pw.is_password_breached(password_inp)
    time.sleep(2)
    print(f"\nYour E-Mail was found in [bold][red]{total_leaked}[/red][/bold] leaked Pastes and Databases.")
    if resp:
        param11 = f"This password was used {resp} time(s) before."
        print("Password breached!")
        print("This password was used [red][bold]{0} time(s)[/red][/bold] before.".format(resp))
    else:
        param11 = f"This password was used [bright_green]0[/bright_green] time(s) before."
        print("Password breached!")
        print("This password was used [bright_green][bold]{0} time(s)[/bright_green][/bold] before.".format(resp))        
    
    f = open(f"{sherlock_inp}.txt", "w")
    g = open(f"{email_inp}.txt", "w")  
    
    p = subprocess.run(cmd_sherlock, stdout=f)
    q = subprocess.run(cmd_holehe, stdout=g) 
    
    f.close()
    g.close()
    
    f = open(f"{sherlock_inp}.txt", "r")
    total_sherlock = f.readlines()
    total_val_sherlock = total_sherlock[-2]
    
    g = open(f"{email_inp}.txt", "r")
    for line in g:
        line = line.strip("\n")
        if check_char in line:
            count_reg += 1
    
    print(f"\n[red][bold]{total_val_sherlock}[/red][/bold]")
    print(f"\n[orange3][bold]Your E-Mail was found registered in {count_reg} common websites.[/orange3][/bold]\n")
    
    param_last = f"[orange3][bold]Your E-Mail was found registered in {count_reg} common websites.[/orange3][/bold]"
    
    if total_leaked >= 10:
        print("|| We suggest you change your passwords immediately ||")
        param1 = f"Your E-Mail was found in [bold][red]{total_leaked}[/red][/bold] leaked Pastes and Databases."
        crx += 0.6
    else:
        param1 = f"Your E-Mail was found in [bold][red]{total_leaked}[/red][/bold] leaked Pastes and Databases."
    
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    
    
    # ─── PARAM2: CHECKING IF PASSWORD CAN BE CRACKED ────────────────────────────────────────
    
    
    print("[red]Checking if password can be cracked[/red]")
    time.sleep(10)
    if len(password_inp) <= 8:
        print(":warning: Length of password is less than 8 characters, This can be easily cracked given a time-frame.\n We Suggest you [bold][red]change your password[/red][/bold] immediately.")
    #wait.start()
    
    with Progress() as progress:

        task2 = progress.add_task("[red]Dehashing...", total=1000)
    
        while not progress.finished:
            progress.update(task2, advance=9)
            time.sleep(0.02)
            
    md5sum = (hashlib.md5(password_inp.encode())).hexdigest()
    results_json = check_password(md5sum)
    
    try:
        source = list(results_json.keys())[0]
        main_result = results_json[source]['results'][0].split(':')
        print(f"Cracked easily.\nSource: {source}\nHash: {main_result[0]}\nPassword Cracked: {main_result[1]}")
        crx += 1
        param2 = f"Cracked easily.\nSource: {source}\nHash: {main_result[0]}"
    except Exception as e:
        print("Your password was not crackable in the given small time-frame.")
        param2 = "Your password was not crackable in the given small time-frame."
        
        
    # ─── PARAM3: CHECKING IF PASSWORD HAS SPECIAL CHARACTERS ────────────────────────
    
    
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("[green]Checking for special characters in your password[/green]")
    time.sleep(10)
    
    with Progress() as progress:

        task2 = progress.add_task("[green]Checking...", total=1000)
    
        while not progress.finished:
            progress.update(task2, advance=15)
            time.sleep(0.02)

    
    char_check = re.compile(SPECIAL_CHARS)
    
    if(char_check.search(password_inp) == None):
        print("Contains NO Special Characters.")
        crx += 0.4
        param3 = "Contains NO Special Characters."
    else:
        print("Contains Special Characters.")
        param3 = "Contains Special Characters."
        #print(char_check.search(password_inp)) #print the special chars
       
        
    # ─── PARAM4: CHECKING IF PASSWORD IS A COMMON VARIATION OF INPUTS ───────────────
    
    
    print("----------------------------------------------------------------")
    print("----------------------------------------------------------------")
    print("[deep_pink4][bold]Checking if the passsword is a common variant of input data[/bold][/deep_pink4]")
    time.sleep(10)
    
    with Progress() as progress:

        task2 = progress.add_task("[deep_pink4]Checking...", total=1000)
    
        while not progress.finished:
            progress.update(task2, advance=15)
            time.sleep(0.02)
    
    
    with open(f'{username_inp}.txt') as file:
        contents = file.read()
        search_word = password_inp
        if search_word in contents:
            print (':warning: Your password is easily crackable.\nThis password can be cracked faster than the time it takes to get back from a short walk.')
            param4 = ':warning: Your password is easily crackable.'
            crx += 0.8
        else:
            print (":sweat_smile: Password not found within common variations, Does'nt mean its not crackable")
            param4 = ":sweat_smile: Password not found within common variations"
            crx += 0.1
    time.sleep(5)
    
    
    # ─── FINALIZING AND MAKING FINAL REPORT ─────────────────────────────────────────
    
    
    consoleClear()
    time.sleep(5)
    
    with Progress() as progress:

        task2 = progress.add_task("[green]Generating Report...", total=1000)
    
        while not progress.finished:
            progress.update(task2, advance=5)
            time.sleep(0.02)
    
    time.sleep(2)
    consoleClear()
    
    if 0.8 < crx < 1 or crx >= 1:
        
        table = Table(title="Final Result", box=box.MINIMAL_DOUBLE_HEAD)
        
        table.add_column("Parameters", style="cyan", no_wrap=True)
        table.add_column("Review", style="magenta")
        table.add_column("Criteria Base Score", style="green")   
        
        table.add_row("CHECKING FOR EMAIL-PASSWORD LEAKS", param1, '0.6')
        table.add_row("CHECKING FOR EMAIL USAGE", param_last, '0.1')
        table.add_row("CHECKING FOR PASSWORD BREACHES", param11, '1')
        table.add_row("CHECKING IF PASSWORD CAN BE CRACKED", param2, '1')
        table.add_row("CHECKING IF PASSWORD HAS SPECIAL CHARACTERS", param3, '0.4')
        table.add_row("CHECKING IF PASSWORD IS A COMMON VARIATION OF INPUTS", param4, '0.8')
        print(table)
        print("----------------------------------------------------------------")
        print(f"Final Criteria Score (CrX): {crx}")
        print("----------------------------------------------------------------")
        print("\n")
        print("Since the CrX value is near extreme or extreme, We suggest you change the password with the one suggested below: ")
        print("\n")
        
        print("----------------------------------------------------------------")
        results = generatePassword(pass_lst)
        print(f"Generated :lock: [red]Secure[/red] Password: {results['data']}")
        print("----------------------------------------------------------------")
        input("Press enter to continue.....")
        
    if 0.6 < crx < 0.8:
        
        table = Table(title="Final Result", box=box.MINIMAL_DOUBLE_HEAD)
        
        table.add_column("Parameters", style="cyan", no_wrap=True)
        table.add_column("Review", style="magenta")
        table.add_column("Criteria Base Score", style="green")   
        
        table.add_row("CHECKING FOR EMAIL-PASSWORD LEAKS", param1, '0.6')
        table.add_row("CHECKING FOR EMAIL USAGE", param_last, '0.1')
        table.add_row("CHECKING FOR PASSWORD BREACHES", param11, '1')
        table.add_row("CHECKING IF PASSWORD CAN BE CRACKED", param2, '1')
        table.add_row("CHECKING IF PASSWORD HAS SPECIAL CHARACTERS", param3, '0.4')
        table.add_row("CHECKING IF PASSWORD IS A COMMON VARIATION OF INPUTS", param4, '0.8')
        print(table)
        print("----------------------------------------------------------------")
        print(f"Final Criteria Score (CrX): {crx}")
        print("----------------------------------------------------------------")
        print("\n")
        print("Since the CrX value is close to the top, We suggest you change the password with the once suggest below: ")
        print("\n")
        
        print("----------------------------------------------------------------")
        results = generatePassword(pass_lst)
        print(f"Generated :lock: [red]Secure[/red] Password: {results['data']}")
        print("----------------------------------------------------------------")
        input("Press enter to continue.....")
        
    if 0.4 < crx < 0.6:
        
        table = Table(title="Final Result", box=box.MINIMAL_DOUBLE_HEAD)
        
        table.add_column("Parameters", style="cyan", no_wrap=True)
        table.add_column("Review", style="magenta")
        table.add_column("Criteria Base Score", style="green")   
        
        table.add_row("CHECKING FOR EMAIL-PASSWORD LEAKS", param1, '0.6')
        table.add_row("CHECKING FOR EMAIL USAGE", param_last, '0.1')
        table.add_row("CHECKING FOR PASSWORD BREACHES", param11, '1')
        table.add_row("CHECKING IF PASSWORD CAN BE CRACKED", param2, '1')
        table.add_row("CHECKING IF PASSWORD HAS SPECIAL CHARACTERS", param3, '0.4')
        table.add_row("CHECKING IF PASSWORD IS A COMMON VARIATION OF INPUTS", param4, '0.8')
        print(table)
        print("----------------------------------------------------------------")
        print(f"Final Criteria Score (CrX): {crx}")
        print("----------------------------------------------------------------")
        print("\n")
        print("Your password is pretty secure for now but we suggest you change it for additional safety: ")
        print("\n")
        
        print("----------------------------------------------------------------")
        results = generatePassword(pass_lst)
        print(f"Generated :lock: [red]Secure[/red] Password: {results['data']}")
        print("----------------------------------------------------------------")
        input("Press enter to continue.....")

    if 0 < crx < 0.4 or crx <= 0:
        
        table = Table(title="Final Result", box=box.MINIMAL_DOUBLE_HEAD)
        
        table.add_column("Parameters", style="cyan", no_wrap=True)
        table.add_column("Review", style="magenta")
        table.add_column("Criteria Base Score", style="green")   
        
        table.add_row("CHECKING FOR EMAIL-PASSWORD LEAKS", param1, '0.6')
        table.add_row("CHECKING FOR EMAIL USAGE", param_last, '0.1')
        table.add_row("CHECKING FOR PASSWORD BREACHES", param11, '1')
        table.add_row("CHECKING IF PASSWORD CAN BE CRACKED", param2, '1')
        table.add_row("CHECKING IF PASSWORD HAS SPECIAL CHARACTERS", param3, '0.4')
        table.add_row("CHECKING IF PASSWORD IS A COMMON VARIATION OF INPUTS", param4, '0.8')
        print(table)
        print("----------------------------------------------------------------")
        print(f"Final Criteria Score (CrX): {crx}")
        print("----------------------------------------------------------------")
        print("\n")
        print("Good job using a secure password :heart:, Stay safe online.")
        print("\n")     
    

# ────────────────────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────
# ─── GENERATING SECURE PASSWORD BASED ON GIVEN PARAMETERS ───────────────────────
# ────────────────────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────

if option_selected == 2:
    
    pass_lst = []
    consoleClear()
    print("----------------------------------------------------------------")
    print("[green][bold] Passwordinator [/bold][/green]")
    print("----------------------------------------------------------------")
    print()

    length = IntPrompt.ask("Enter the Length of the password you need")
    pass_lst.append(length)
    num = Prompt.ask("Enter if you want numbers in your Password (True/False)").lower()
    pass_lst.append(num)
    chars = Prompt.ask("Enter if you want special characters in your Password (True/False)").lower()
    pass_lst.append(chars)
    caps = Prompt.ask("Enter if you want uppercase alphabets in your Password (True/False)").lower()
    pass_lst.append(caps)
    
    time.sleep(2)
    
    consoleClear()
    
    print("Generating a secure Password: ")
    with Progress() as progress:

        task2 = progress.add_task("[green]Processing...", total=1000)
    
        while not progress.finished:
            progress.update(task2, advance=10)
            time.sleep(0.02)
           
    consoleClear()
    
    print("----------------------------------------------------------------")
    results = generatePassword(pass_lst)
    print(f"Generated :lock: [red]Secure[/red] Password: {results['data']}")
    print("----------------------------------------------------------------")
    input("Press enter to continue.....")
    
# ────────────────────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────
# ─── UNIT TESTING + INTERNAL TESTING ────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────────────────────────

if option_selected == 3:
    print("\n INTERNAL ONLY (UNIT-TESTING)\n")

    cmd_unittest = 'python test_final_code_proj.py'
    
    f = open("internal.txt", "w")
    p = subprocess.run(cmd_unittest, stdout=f)
    f.close()
    
    f = open("internal.txt", "r")    
    
    with Progress() as progress:

        task2 = progress.add_task("[red]Checking...", total=1000)
        
        while not progress.finished:
            progress.update(task2, advance=9)
            time.sleep(0.02)
    
    for line in f:
        line = line.strip("\n")
        if "FAILED" in line:
            print("[red][bold] TESTS FAILED [/bold][/red]")
        else:
            print("[bright_green][bold] ALL TESTS PASSED [/bold][/bright_green]")
