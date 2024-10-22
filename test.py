import urllib.parse

def gen_x_link(hash_id):
    text = f"Check out $RIKO, the fearless pet of GRA.FUN! Join the community and earn points with my referral link! 👇 \nhttps://t.me/adtgtestbot?start={hash_id}\nBSC is ours for the taking! 🏴‍☠️"
    encoded_text = urllib.parse.quote(text, safe='')
    link = "https://x.com/intent/post?text="+encoded_text
    return link