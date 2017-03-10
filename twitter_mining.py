from helperfunctions import *
from tweepy import TweepError


def search_tweets(screen_names, virtuald, tweet_lim):
    # tweepy API
    client = get_twitter_client()
    # parameters
    start = datetime.datetime(2013, 1, 1)                                           
    end = datetime.datetime.today()

    print('Getting Tweets...')
    total_tweets = []
    for screen_name in screen_names:
        # check that 'start' is after account was created
        user_data = client.get_user('X1alejandro3x')
        created = user_data.created_at
        if start<created:
            start = created

        # save tweet ids to jsonl file
        num_tweets = get_all_user_tweets(screen_name, 
                                         start, end,
                                         tweet_lim=tweet_lim, 
                                         virtuald=virtuald)
        total_tweets.append(num_tweets)
    print('Found {} tweets.'.format(sum(total_tweets)))


def write_tweets(screen_names, verbosity):
    # tweepy API                                                                
    client = get_twitter_client()
    
    print('Writing results...')
    for screen_name in screen_names:
        # use selenium extension
        fid = 'users/{0}/usr_tweetids_{0}.jsonl'.format(screen_name)
        ftweet = 'users/{0}/usr_timeline_{0}.jsonl'.format(screen_name)
        fcheck = 'users/{0}/checkpoints_{0}.txt'.format(screen_name)
        if not os.path.isfile(fcheck):      # if no checkpoint file
            with open(fid, 'r') as f_id, open(ftweet, 'a') as f_tweet, \
                    open(fcheck, 'w') as check_p: 

                for line in iter(f_id.readline, ''):
                    # save the location of file
                    check_p.write( '{}\n'.format(f_id.tell()) )
                    # load ids
                    ids = json.loads(line)
                    
                    for tweetId in ids:
                        try:
                            tweet = client.get_status(tweetId)
                            f_tweet.write(json.dumps(tweet._json)+'\n')

                        except TweepError as e:
                            if verbosity:
                                print(e)
                            time.sleep(60*15)

        else:       # if checkpoints file allready exists
            with open(fid, 'r') as f_id, open(ftweet, 'a') as f_tweet, \
                    open(fcheck, 'r+') as check_p:  

                checkpoints = check_p.readlines()
                checkpoints = [check.strip('\n') for check in checkpoints 
                               if check.strip('\n')!='']
                # go to last checkpoint
                if checkpoints:
                    f_id.seek(int(checkpoints[-1]))
                for line in iter(f_id.readline, ''):                                              
                    # save the location of file
                    check_p.write( '{}\n'.format(f_id.tell()) )
                    # load ids
                    ids = json.loads(line)                                  
                                                                                
                    for tweetId in ids:                                     
                        try:                                                
                            tweet = client.get_status(tweetId)  
                            f_tweet.write(json.dumps(tweet._json)+'\n')

                        except TweepError as e:                             
                            if verbosity:
                                print(e)                                        
                            time.sleep(60*15)

                print('done writing results.\nCheck: {}'.format(ftweet))


if __name__=='__main__':
    screen_names = ['X1alejandro3x', 'HEPfeickert']                                 
                                                                                
    # command line arguments                                                        
    args = mining_cml()                                                             
    verbosity = args.verbose                                                        
    virtuald = args.virtual                                                         
    tweet_lim = args.tweet_lim                                                      

    # search for tweets 
    search_tweets(screen_names, virtuald, tweet_lim)

    # save tweets -> save entire tweet
    write_tweets(screen_names, verbosity)
