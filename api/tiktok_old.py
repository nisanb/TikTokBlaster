from TikTokApi import TikTokApi

custom_verifyFp = "verify_kip21zo9_AsvgZoOf_osR9_4TD4_BqLR_P1Vq5uXNujv8"
# custom_verifyFp = "verify_kip2gsld_Tiu5qinc_F3Fy_4o2L_BFmO_48nugeefacSn"

api = TikTokApi(custom_verifyFp="verify_kip2gsld_Tiu5qinc_F3Fy_4o2L_BFmO_48nugeefacSn")


def get_videos_by_hash_tag(hash_tag: str = "puppy", count: int = 5):
    return api.byHashtag(hashtag=hash_tag, count=count)
