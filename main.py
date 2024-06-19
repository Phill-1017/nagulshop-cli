import argparse
import sys

from core import register, login, create_offer, offers, message, show_messages, create_bid_cli, get_bids

session_info = {}

def role_based_interface(user_role):
    if user_role == "admin":
        return admin_commands()
    else:
        return user_commands()

def admin_commands():
    parser = argparse.ArgumentParser(description="Admin Interface", add_help=False)
    subparsers = parser.add_subparsers(title="Available commands for admin", description="These commands are available for admin role", metavar="COMMAND")

    subparsers.add_parser('help', help='Show this help message').set_defaults(func=lambda args: parser.print_help())

    offer_parser = subparsers.add_parser('create_offer', help='Create a new offer (Admin only)')
    offer_parser.add_argument('name', type=str, help='Name of the product')
    offer_parser.add_argument('price', type=float, help='Price of the product')
    offer_parser.add_argument('description', type=str, help='Description of the product')
    offer_parser.set_defaults(func=create_offer)

    offers_parser = subparsers.add_parser('offers', help='List all offers')
    offers_parser.set_defaults(func=offers)

    message_parser = subparsers.add_parser('message', help='Send a message to another user')
    message_parser.add_argument('sender', type=str, help='Your username')
    message_parser.add_argument('receiver', type=str, help='Username of the message receiver')
    message_parser.add_argument('message_text', type=str, help='Content of the message')
    message_parser.set_defaults(func=message)

    show_messages_parser = subparsers.add_parser('show_messages', help='Show all messages received by a user')
    show_messages_parser.add_argument('receiver', type=str, help='Username whose messages are to be shown')
    show_messages_parser.set_defaults(func=show_messages)

    get_bids_parser = subparsers.add_parser('get_bids', help='View all bids for a specific offer')
    get_bids_parser.add_argument('offer_id', type=int, help='ID of the offer to view bids for')
    get_bids_parser.set_defaults(func=get_bids)

    bid_parser = subparsers.add_parser('create_bid', help='Place a bid on an offer')
    bid_parser.add_argument('offer_id', type=int, help='ID of the offer to bid on')
    bid_parser.add_argument('bid_amount', type=float, help='Amount of your bid')
    bid_parser.add_argument('bidder_id', type=int, help='Your user ID')
    bid_parser.set_defaults(func=create_bid_cli)

    return parser

def user_commands():
    parser = argparse.ArgumentParser(description="User Interface", add_help=False)
    subparsers = parser.add_subparsers(title="Available commands for users", description="These commands are available for regular users", metavar="COMMAND")

    subparsers.add_parser('help', help='Show this help message').set_defaults(func=lambda args: parser.print_help())

    offers_parser = subparsers.add_parser('offers', help='List all offers available')
    offers_parser.set_defaults(func=offers)

    message_parser = subparsers.add_parser('message', help='Send a message to another user')
    message_parser.add_argument('sender', type=str, help='Your username')
    message_parser.add_argument('receiver', type=str, help='Username of the message receiver')
    message_parser.add_argument('message_text', type=str, help='Content of the message')
    message_parser.set_defaults(func=message)

    show_messages_parser = subparsers.add_parser('show_messages', help='Show all messages received by a user')
    show_messages_parser.add_argument('receiver', type=str, help='Username whose messages are to be shown')
    show_messages_parser.set_defaults(func=show_messages)

    get_bids_parser = subparsers.add_parser('get_bids', help='View all bids for a specific offer')
    get_bids_parser.add_argument('offer_id', type=int, help='ID of the offer to view bids for')
    get_bids_parser.set_defaults(func=get_bids)

    bid_parser = subparsers.add_parser('create_bid', help='Place a bid on an offer')
    bid_parser.add_argument('offer_id', type=int, help='ID of the offer to bid on')
    bid_parser.add_argument('bid_amount', type=float, help='Amount of your bid')
    bid_parser.add_argument('bidder_id', type=int, help='Your user ID')
    bid_parser.set_defaults(func=create_bid_cli)

    return parser

def interactive_mode(parser):
    print("Interactive mode activated. Type 'help' for command options or 'exit' to quit.")
    while True:
        command_input = input("Enter command: ").strip().split()
        if command_input[0] == 'exit':
            print("Exiting.")
            break
        try:
            args = parser.parse_args(command_input)
            if hasattr(args, 'func'):
                args.func(args)
        except SystemExit:
            continue

def post_login_callback(args, user_role):
    session_info['role'] = user_role
    print(f"Logged in as {args.username} with role {user_role}. Type 'help' to see available commands.")
    parser = role_based_interface(user_role)
    interactive_mode(parser)

def main():
    parser = argparse.ArgumentParser(description="Nagul Shop Command Line Interface", add_help=False)
    subparsers = parser.add_subparsers(help='commands')

    register_parser = subparsers.add_parser('register', help='Register a new user. Specify username, password, and role.')
    register_parser.add_argument('username', type=str, help='Username')
    register_parser.add_argument('password', type=str, help='Password')
    register_parser.add_argument('role', type=str, help='Role (admin or user)')
    register_parser.set_defaults(func=register)

    login_parser = subparsers.add_parser('login', help='Login a user. Provide username and password.')
    login_parser.add_argument('username', type=str, help='Username')
    login_parser.add_argument('password', type=str, help='Password')
    login_parser.set_defaults(func=lambda args: login(args, post_login_callback=post_login_callback))

    if len(sys.argv) == 1:
        print("No commands provided. Type 'help' for usage or 'register' or 'login' to begin.")
        interactive_mode(parser)
    else:
        args, unknown = parser.parse_known_args()
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
