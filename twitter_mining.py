from helperfunctions import *
from tweepy import TweepError
from multiprocessing import freeze_support
from multiprocessing import Pool
from itertools import repeat


def search_tweets(start, end, screen_name, virtuald, tweet_lim, topics=[]):
    # tweepy API
    client = get_twitter_client()
    print('Getting {}\'s Tweets...'.format(screen_name))

    # check that 'start' is after account was created
    user_data = client.get_user(screen_name)
    created = user_data.created_at
    if start<created:
        start = created
    if not end:                                                                 
        end = datetime.datetime.today()

    # save tweet ids to jsonl file
    total_tweets = get_all_user_tweets(screen_name, 
                                       start, end, 
                                       topics=topics,
                                       tweet_lim=tweet_lim, 
                                       virtuald=virtuald)
    print('Found {} tweets from {}.'.format(total_tweets, screen_name))


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
    
    start = datetime.datetime(2015, 1, 1)                                       
    end = datetime.datetime.today()
    
    screen_names = [
        'realDonaldTrump', 'POTUS', 'WhiteHouse', 'PressSec',
        'RudyGiuliani', 'StephenBannon', 'jeffsessions', 'KellyannePolls',
        'GenFlynn',
        'NBCNews', 'CNN', 'cnnbrk', 'FoxNews', 'AP',
                   ]                                 
    topics = [
        'muslims', 'muslim', 'islam', 'islamic', 'mosque', 'mosques',
        'radical', 'radicals', 'terrorism', 'terrorists', 'terrorist', 
        'terror', 'ISIS', 
        'travel', 'ban', 'eo', 'executive', 'order','orders', 'screening', 
        'resist', 'protect', 'protection',
        'airport', 'airports', 'visa', 'visas','target', 'targets', 'refug', 
        'refugee', 'refugees', 'middle', 'east', 'eastern', 'easterners'
        'Iran', 'Iraq', 'Libya', 'Somalia', 'Sudan', 'Yemen', 'Syria',
             ]

    # command line arguments                                                        
    args        = mining_cml()                                                             
    verbosity   = args.verbose                                                        
    virtuald    = args.virtual                                                         
    tweet_lim   = args.tweet_lim                                                      
    search      = args.search
    multisearch = args.multisearch
    write       = args.write

    # search for tweets
    if search:
        for screen_name in screen_names:
            search_tweets(start, end, screen_name, virtuald, tweet_lim,
                          topics=topics)
    if multisearch:
        freeze_support()
        pool = Pool()
        pool.starmap(search_tweets, 
                    zip(repeat(start), repeat(end), screen_names, 
                        repeat(virtuald), repeat(tweet_lim))
                    )

    # save tweets -> save entire tweet  
    if write:
        write_tweets(screen_names, verbosity) 
