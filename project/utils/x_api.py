import tweepy

access_token = "1877497859261755392-8JWrKiBBF4itOMupeTCELA1FvVm7hZ"
token_secret = "HuorboZQqINdTRUVEAnMY0tL69KOpJ255kdgkslIE1XuI"
api_key = "3NVaOSmDjAnKDH0IRFM4Cl4zN"
api_secret = "lcL3C5HMWOkougoYNl3sH1aHgjCCqFFdoY4fVY7bdTPuCoDBTw"

x_client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=token_secret
)

class XClient:
    def get_post(self):
        user_id = x_client.get_me().data.id

        try:
            tweets = x_client.get_users_tweets(
                id=user_id,
                max_results=10,
                user_auth=True,
            )

            # Itera e stampa i tweet
            if tweets.data:
                for tweet in tweets.data:
                    print(f"Tweet ID: {tweet.id}, Testo: {tweet.text}")
            else:
                print("Nessun tweet trovato.")
        except tweepy.TweepyException as e:
            print(f"Errore: {e}")

def main():
    #r = x_client.create_tweet(text="Porco tweet")
    r = XClient().get_post()
    pass

if __name__ == '__main__':
    main()


