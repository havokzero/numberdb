import random
from dotenv import load_dotenv
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',

]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def load_environment_variables():
    load_dotenv()

def display_progress_bar(items):
    return tqdm(items, desc="Processing")

def print_success(message):
    print(Fore.GREEN + message)

def print_error(message):
    print(Fore.RED + message)
