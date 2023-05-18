from dotenv import load_dotenv
import os

# Get bot authentication from environment.
load_dotenv()
token = os.environ.get('AUTH_TOKEN')

def main():
    return 0

if __name__ == '__main__':
    main()