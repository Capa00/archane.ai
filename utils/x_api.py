import tweepy

client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAA0wyAEAAAAAMMqqJI9MOZBY%2FUVMzwQN92x25Gs%3DQPHblEkFRfdN9r3YuxipM7V9UmhmCrh9kTCEpLZuvJOe8mpubc")
access_token = "1877497859261755392-8JWrKiBBF4itOMupeTCELA1FvVm7hZ"
token_secret = "HuorboZQqINdTRUVEAnMY0tL69KOpJ255kdgkslIE1XuI"
api_key = "3NVaOSmDjAnKDH0IRFM4Cl4zN"
api_secret = "lcL3C5HMWOkougoYNl3sH1aHgjCCqFFdoY4fVY7bdTPuCoDBTw"

client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=token_secret
)
def main():
    r = client.create_tweet(text="Terzo tweet")
    pass

if __name__ == '__main__':
    main()

