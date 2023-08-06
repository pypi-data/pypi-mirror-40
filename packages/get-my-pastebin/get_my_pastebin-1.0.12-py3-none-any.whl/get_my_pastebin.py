import click
from pick import pick
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import pyperclip

API_RESULTS_LIMIT = 1000
LOGIN_URL = 'https://pastebin.com/api/api_login.php'
API_LIST_URL = f'https://pastebin.com/api/api_post.php'
API_RAW_PASTE_URL = 'https://pastebin.com/api/api_raw.php'

@click.command()
@click.option('--api-key', required=True, help='API Dev key')
@click.option('--username', required=True, help='Your username account')
@click.option('--password', required=True, help='Your password account')
@click.argument('search')
def main(api_key, username, password, search):
    """ Terminal application to find and copy your own Paste for Pastebin"""
    user_key = get_user_key(api_key, username, password)
    title = f'Results: {search}'
    options = get_list(api_key, user_key, search)
    if not options:
        click.echo('Not results')
    else:
        # Show list to pick item
        def get_label(option): return option.get('label')
        option, index = pick(options, title, indicator='*', options_map_func=get_label)
        raw_paste = get_raw_paste(api_key, user_key, option['paste_key'])
        # Print raw paste
        click.echo(raw_paste)
        # Copy to clipboard
        pyperclip.copy(raw_paste)

def get_user_key(api_key, username, password):
    """Get login key"""
    post_url = 'http://localhost:3000/vim'
    headers = {}
    headers['Content-Type'] = 'application/json'
    post_data = urllib.parse.urlencode(
        {
            'api_dev_key' : api_key,
            'api_user_name': username,
            'api_user_password': password
        }
            ).encode('ascii')
    post_response_user_key = urllib.request.urlopen(url=LOGIN_URL, data=post_data)
    return post_response_user_key.read().decode("utf-8")

def get_list(api_key, user_key, search):
    # Get all list
    post_data = urllib.parse.urlencode(
            {
                'api_option': 'list',
                'api_dev_key' : api_key,
                'api_user_key': user_key,
                'results_limit': API_RESULTS_LIMIT
            }
                ).encode('ascii')
    response_list = urllib.request.urlopen(url=API_LIST_URL, data=post_data)
    data_list = '<list>' + response_list.read().decode("utf-8") + '</list>'
    data_list = ET.fromstring(data_list)
    # Search data
    results = []
    for paste in data_list:
        found = False
        label = ''
        paste_key = ''
        # Search in node. Save label and key
        for item in paste:
            if item.tag == 'paste_title' and search.upper() in item.text.upper():
                found = True
                label = item.text
            if item.tag == 'paste_key':
                paste_key = item.text
        # Save node
        if found:
            results.append(
                    {
                        'label': label,
                        'paste_key': paste_key
                    }
                )

    return results

def get_raw_paste(api_key, user_key, paste_key):
    # Get raw paste
    post_data = urllib.parse.urlencode(
            {
                'api_option': 'show_paste',
                'api_dev_key' : api_key,
                'api_user_key': user_key,
                'api_paste_key': paste_key
            }
                ).encode('ascii')
    response_paste = urllib.request.urlopen(url=API_RAW_PASTE_URL, data=post_data)
    # Clear
    raw_paste = response_paste.read().decode("utf-8").replace('\r', '')

    return raw_paste

if __name__ == '__main__':
    main()
