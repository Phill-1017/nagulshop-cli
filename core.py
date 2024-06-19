import os
import requests

from basemodel.AccountRequest import AccountRequest
from basemodel.CreateBidRequest import CreateBidRequest
from basemodel.LoginRequest import LoginRequest
from basemodel.CreateOfferRequest import CreateOfferRequest
from basemodel.Message import MessageModel

BASE_URL = os.getenv("API_URL", "http://localhost:8000")

headers = {'Content-Type': 'application/json'}

def register(args):
    register_url = f"{BASE_URL}/account/register"
    account_request = AccountRequest(username=args.username, password=args.password, role=args.role)
    account_json = account_request.dict()
    requests.post(register_url, json=account_json, headers=headers)
    print("Registration process complete.")

def login(args, post_login_callback):
    login_url = f"{BASE_URL}/account/login"
    login_request = LoginRequest(username=args.username, password=args.password)
    login_json = login_request.dict()
    result = requests.post(login_url, json=login_json)
    if result:
        print(f"Login successful for {args.username}.")
        user_role = result.json().get('role')  # Assuming result is a JSON response
        post_login_callback(args, user_role)
    else:
        print("Login failed or user not found.")

def create_offer(args):
    create_offer_url = f"{BASE_URL}/shoe-offer/create"
    offer_request = CreateOfferRequest(name=args.name, price=args.price, description=args.description)
    offer_json = offer_request.dict()
    requests.post(create_offer_url, json=offer_json)
    print("Offer creation process completed.")

def message(args):
    message_url = f"{BASE_URL}/message"
    message = MessageModel(sender=args.sender, receiver=args.receiver, message=args.message_text)
    message_json = message.dict()
    requests.post(message_url, json=message_json)
    print("Message posted successfully.")

def create_bid_cli(args):
    create_bid_url = f"{BASE_URL}/bid/bid"
    bid_request = CreateBidRequest(offer_id=args.offer_id, bid_amount=args.bid_amount, bidder_id=args.bidder_id)
    bid_json = bid_request.dict()
    result = requests.post(create_bid_url, json=bid_json)
    print(result.text)

def offers():
    offers_url = f"{BASE_URL}/shoe-offer/all"
    offers = requests.get(offers_url)
    if offers:
        for offer in offers:
            print(f"Offer ID: {offer.id}, Name: {offer.name}, Price: {offer.price}, Description: {offer.description}")
    else:
        print("No offers found.")

def show_messages(args):
    show_messages_url = f"{BASE_URL}/message/messages/{args.receiver}"
    try:
        messages = requests.get(show_messages_url)
        if messages:
            for msg in messages.messages:
                print(f"From: {msg.sender}, Message: {msg.text}")
        else:
            print("No messages found.")
    except Exception as e:
        print(f"Error: {str(e)}")

def get_bids(args):
    get_bids_url = f"{BASE_URL}/bid/bids/{args.offer_id}"
    bids = requests.get(get_bids_url)
    if bids:
        for bid in bids:
            print(f"Bid ID: {bid.id}, Bidder ID: {bid.bidder_id}, Amount: {bid.bid_amount}")
    else:
        print("No bids found.")
