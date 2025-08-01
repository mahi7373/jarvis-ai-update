import schedule
import time
from pytrends.request import TrendReq

def fetch_marvel_trending():
    try:
        pytrends = TrendReq(hl='en-US', tz=330)
        pytrends.build_payload(kw_list=["Marvel"])
        trending_data = pytrends.related_queries()
        
        if "Marvel" in trending_data and trending_data["Marvel"]["top"] is not None:
            marvel_trends = trending_data["Marvel"]["top"]["query"].tolist()
            return marvel_trends[:5]
    except:
        pass
    return ["Marvel latest news", "Marvel movies update"]

def auto_generate_upload():
    topics = fetch_marvel_trending()
    topic = topics[0]
    print(f"🎬 Today's Marvel Topic: {topic}")
    print(f"✅ Would generate video for: {topic}")

if __name__ == "__main__":
    print("🚀 Jarvis Marvel Scheduler Running...")
    auto_generate_upload()
    
    schedule.every().day.at("10:00").do(auto_generate_upload)
    schedule.every().day.at("15:00").do(auto_generate_upload)
    schedule.every().day.at("20:00").do(auto_generate_upload)
    
    print("🤖 Auto Scheduler Active...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)