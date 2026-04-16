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
    candidates = ("william hanlon", "owen hart")
    while True:
        print(
            f"{COLORS.GREEN}William Hanlon (VP Cole Lentini)\nOwen Hart (VP John Perveiler)\n---------------------------------------------------------------{COLORS.RESET}")
        candidate = click.prompt(f"{COLORS.RED}Your{COLORS.WHITE} presidential{COLORS.BLUE} candidate{COLORS.RESET}",
                                 type=str)
        if candidate.lower() in candidates:
            break
        else:
            click.clear()
            print(f"{COLORS.RED}THAT WAS NOT AN OPTION.{COLORS.RESET}\n")
    click.clear()
    return {"candidate": candidate}

def candidate_to_index(candidate_name):


    mapping = {"william hanlon": 0, "owen hart": 1}
    return mapping.get(candidate_name.lower(), -1)


def show_receipt(receipt_hash):
    click.clear()
    print(f"{COLORS.GREEN}Vote submitted successfully!{COLORS.RESET}")
    print(f"\nYour verification receipt (save this):")
    print(f"{COLORS.YELLOW}{receipt_hash}{COLORS.RESET}")
    print(f"\nUse this to verify your vote on the bulletin board after polls close.")
    input("\nPress Enter to continue...")

'''

if __name__ == "__main__":
    creds = get_creds()
    print(creds)
    poll_results = poll()
    print(poll_results)
'''