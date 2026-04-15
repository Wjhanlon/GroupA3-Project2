import click
import re
import COLORS

def get_creds():
    '''
    This function gathers all the user's credentials.
    :return: A dictionary with keys {username, ssn} or -1 if the ssn doesn't follow format ###-##-#### excluding hyphens.
    '''
    ssn_pattern = r"\d\d\d\d\d\d\d\d\d"
    click.clear()
    user_name = click.prompt(f"{COLORS.GREEN}Your username{COLORS.RESET}", type=str)
    click.clear()
    ssn = click.prompt(f'{COLORS.GREEN}Your SSN{COLORS.YELLOW} (your entry will be hidden){COLORS.RESET}', type=str, hide_input = True)
    if re.search(ssn_pattern, ssn) is None:
        click.clear()
        print(f"{COLORS.YELLOW}The SSN is invalid. Make sure your SSN is entered as ###-##-#### excluding hyphens.{COLORS.RESET}")
        return -1
    credentials = {"username": user_name, "ssn": ssn}

    return credentials

def poll():
    click.clear()
    candidates = ("william hanlan", "owen hart")
    candidate = None
    loop = True
    while loop:
        print(f"{COLORS.GREEN}William Hanlan (VP Cole Lentini)\nOwen Hart (VP John Perveiler)\n---------------------------------------------------------------{COLORS.RESET}")
        candidate = click.prompt(f"{COLORS.RED}Your{COLORS.WHITE} presidential{COLORS.BLUE} candidate{COLORS.RESET}", type=str)
        if candidate.lower() in candidates:
            break
        else:
            click.clear()
            print(f"{COLORS.RED}THAT WAS NOT AN OPTION.{COLORS.RESET}\n")
    click.clear()
    favorite_color = click.prompt(f"{COLORS.GREEN}Your favorite color{COLORS.RESET}", type=str)
    click.clear()
    jumping_jacks = click.prompt(f"{COLORS.GREEN}Number of jumping jacks you can do until failure{COLORS.RESET}", type=str)
    poll_results = {"candidate": candidate, "favorite_color": favorite_color, "jumping_jacks": jumping_jacks}
    return poll_results

'''
if __name__ == "__main__":
    creds = get_creds()
    print(creds)
    poll_results = poll()
    print(poll_results)
'''