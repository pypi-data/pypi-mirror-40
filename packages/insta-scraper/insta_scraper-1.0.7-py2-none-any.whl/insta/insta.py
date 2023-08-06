from instagram.instagram import *
from getpass import getpass
import argparse


def main():

    parser = argparse.ArgumentParser(
        description="""It allows user to download
            photos,videos and statuses of a target user.
            Target user should be friend of instagram user
            else it will download profile picture only.
            """
    )
    parser.add_argument('-u', '--user', type=str, required=True, help='instagram username')
    parser.add_argument('-f', '--friendname', type=str, required=True, help='friend\'s username')
    args = parser.parse_args()

    password = getpass('Password:')
    status = insta_login(args.user, password)

    if not status:
        print 'Invalid Username or Password.'
        return

    print 'Logged in as %s' % args.user

    query_hash = get_query_hash(args.friendname)

    target_user_profile_id = get_profile_id()

    download_media(args.friendname, query_hash, target_user_profile_id)


if __name__ == '__main__':

    main()
