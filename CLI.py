import click
import re
import COLORS

ssn_pattern = r"\d\d\d-\d\d-\d\d\d\d"

@click.command()
@click.option('--first_name', prompt=f'{COLORS.GREEN}Your first name{COLORS.RESET}', help='The user\'s first Name')
@click.option('--last_name', prompt=f'{COLORS.GREEN}Your last name{COLORS.RESET}', help='The user\'s last name')
@click.option('--ssn', prompt=f'{COLORS.GREEN}Your SSN ###-##-#### {COLORS.YELLOW}(your entry will be hidden){COLORS.RESET}', hide_input = True,help='The user\'s SSN')
def get_creds(first_name, last_name, ssn):
    '''
    This function gathers all the user's credentials. It can be called without any arguments or with --help for a more detailed breakdown on the arguments.\n
    For this function to actually return anything, 'standalone_mode = False' must be entered as the parameter to this function. An example of this can be seen in the commented code at the bottom.
    :return: A dictionary with keys {first_name, last_name, ssn} or -1 if the ssn doesn't follow format ###-##-####
    '''
    if re.search(ssn_pattern, ssn) is None:
        print(f"{COLORS.YELLOW}The SSN is invalid. Make sure your SSN is entered as ###-##-#### including hyphens.{COLORS.RESET}")
        return -1
    credentials = {"first_name": first_name.lower(), "last_name": last_name.lower(), "ssn": ssn}

    return credentials
'''
if __name__ == "__main__":
    # The function MUST be called like this or else click will bone you
    creds = get_creds(standalone_mode = False)
    print(creds)
'''