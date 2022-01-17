def getENS(mention):
    if ".eth" in mention[1] or "0x" in mention[1]:
        return mention[1]
    else:
        return "ERROR"

def get_reply_count(mention):
    try:
        return int(mention[2])
    except:
        return 10

def isVerified(mention):
    if mention[3].lower() == "verified":
        return True
    else:
        return False

def get_like_count(mention):
    try:
        return int(mention[4])
    except:
        return 0

def get_retweet_count(mention):
    try:
        return int(mention[5])
    except:
        return 0
    

#look_for_mentions()
def clean_mentions(mentions):
    print("MENTIONS ",mentions)
    cleaned_data = []

    for mention in mentions:
        ens = ""
        num_of_replies = 10
        is_verified = False
        like_count = 0
        retweet_count = 0

        parts = mention.split(' ')
        num_of_attributes = len(parts)

        if num_of_attributes == 1:
            ens = "ERROR"
        elif num_of_attributes == 2:
            ens = getENS(parts)
        elif num_of_attributes == 3:
            ens = getENS(parts)
            num_of_replies = get_reply_count(parts)

        elif num_of_attributes == 4:
            ens = getENS(parts)
            num_of_replies = get_reply_count(parts)
            is_verified = isVerified(parts)
        elif num_of_attributes == 5:
            ens = getENS(parts)
            num_of_replies = get_reply_count(parts)
            is_verified = isVerified(parts)
            like_count = get_like_count(parts)
        
        elif num_of_attributes == 6:
            ens = getENS(parts)
            num_of_replies = get_reply_count(parts)
            is_verified = isVerified(parts)
            like_count = get_like_count(parts)
            retweet_count = get_retweet_count(parts)
        else:
            ens = "ERROR"

        cleaned_data.append([ens, num_of_replies, is_verified, like_count, retweet_count])
    
    return cleaned_data
