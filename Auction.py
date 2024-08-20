import time
import threading
class Auction:
    def __init__(self, item, start_price, auctioneer, reserve_price=None, bid_increment=1, duration=None):
        self.item = item
        self.current_price = start_price
        self.current_bidder = None
        self.auctioneer = auctioneer
        self.is_active = True
        self.reserve_price = reserve_price
        self.bid_increment = bid_increment
        self.bidders = {}
        self.start_time = time.time()
        self.duration = duration  # Auction time limit in seconds
        self.end_time = None if duration is None else self.start_time + duration

    def place_bid(self, bidder_name, bid_amount):
        if not self.is_active:
            print(f"The auction for {self.item} has ended.")
            return
        
        if bid_amount < self.current_price + self.bid_increment:
            print(f"Bid must be at least {self.current_price + self.bid_increment}.")
            return
        
        self.current_price = bid_amount
        self.current_bidder = bidder_name
        self.bidders[bidder_name] = bid_amount
        print(f"{bidder_name} placed a bid of {bid_amount}!")

    def auto_close(self):
        if self.end_time and time.time() >= self.end_time:
            self.close_auction()

    def close_auction(self):
        self.is_active = False
        if self.current_price >= self.reserve_price:
            print(f"Auction closed! {self.item} sold to {self.current_bidder} for {self.current_price}.")
        else:
            print(f"Auction closed! Reserve price not met, {self.item} not sold.")

    def auction_status(self):
        print(f"Auction for {self.item}: Current highest bid is {self.current_price} by {self.current_bidder}.")

# Auction management functions
def create_auction(auctioneer):
    item = input("Enter the item name for auction: ")
    start_price = float(input("Enter the starting price: "))
    reserve_price = float(input("Enter the reserve price (or press Enter to skip): ") or 0)
    bid_increment = float(input("Enter minimum bid increment: "))
    duration = int(input("Enter auction duration in seconds (or press Enter for no time limit): ") or 0)
    auction = Auction(item, start_price, auctioneer, reserve_price, bid_increment, duration)
    return auction

def participate_in_auction(auction):
    print(f"Auction started for {auction.item}.")
    
    def auto_close_timer(auction):
        while auction.is_active:
            time.sleep(1)
            auction.auto_close()

    if auction.duration:
        threading.Thread(target=auto_close_timer, args=(auction,)).start()

    while auction.is_active:
        auction.auction_status()
        action = input("Enter 'bid' to place a bid, 'close' to end auction, or 'status' to view current status: ").strip().lower()
        if action == 'bid':
            bidder_name = input("Enter your name: ")
            bid_amount = float(input("Enter your bid amount: "))
            auction.place_bid(bidder_name, bid_amount)
        elif action == 'close':
            auction.close_auction()
        elif action == 'status':
            auction.auction_status()
        else:
            print("Invalid action. Try again.")
        time.sleep(1)

def main():
    auctioneer = input("Enter auctioneer name: ")
    auction = create_auction(auctioneer)
    participate_in_auction(auction)

if __name__ == "__main__":
    main()
