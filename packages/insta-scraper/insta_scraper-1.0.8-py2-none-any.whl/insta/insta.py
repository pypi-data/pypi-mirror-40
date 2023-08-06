from instagram.instagram import *
from getpass import getpass
import argparse
import os


def download_user_data(friendname):

    print '\n\n[+]Downloading %s media' % friendname
    query_hash = get_query_hash(friendname, location)

    if not query_hash:
        return

    target_user_profile_id = get_profile_id()

    download_media(friendname, query_hash, target_user_profile_id, location)


def main():

    global location
    parser = argparse.ArgumentParser(
        description="""It allows user to download
            photos,videos and statuses of a target user.
            we can specifiy one or more target users.
            Target user should be friend of instagram user
            else it will download profile picture only.
            """
    )
    parser.add_argument('-u', '--user', type=str, required=True, help='Your Instagram Username')
    parser.add_argument('-t', '--target-users', nargs='+', help='One or more friends Usernames to download')
    parser.add_argument('-f', '--filename', type=file, help='A file containing target instagram usernames.')
    parser.add_argument('-o', '--output-dir', type=str, help='Output directory to store media')
    args = parser.parse_args()

    to_iterate = None

    if args.target_users:
        to_iterate = args.target_users
    elif args.filename:
        to_iterate = args.filename
    else:
        print '\nPlease type insta-scraper -h to see help.'
        return

    if args.output_dir:
        if not os.path.isdir(args.output_dir):
            print 'Directory doesn\'t exist.'
            return
        else:
            location = args.output_dir
    else:
        location = os.getcwd()

    password = getpass('Password:')

    try:
        status = insta_login(args.user, password)

        if not status:
            print 'Invalid Username or Password.'
            return

        print '\nLogged in as %s' % args.user
    except requests.exceptions.ConnectionError:
        print 'Try again sometime.'
        return

    for friend in to_iterate:
        download_user_data(friend.strip())


if __name__ == '__main__':

    main()
