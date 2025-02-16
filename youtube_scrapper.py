from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.common.by import By
def youtubescrape():
    def web_driver():
        options = webdriver.ChromeOptions()
        options.add_argument("--verbose")
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920, 1200")
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        return driver

    driver = web_driver()
    driver.get('https://www.youtube.com/hashtag/deepfake/shorts')
    urls = []

    elements = driver.find_elements(By.XPATH, "//*[@id='thumbnail' and @href]")
    c = 0
    for ele in elements:
        c += 1
        print(str(c) + '-----Tag: ' + ele.tag_name)
        print('ID: ' + ele.get_attribute('id'))
        url = ele.get_attribute('href')
        urls.append(url)
        print('Link: ' + url)

    driver.quit()

    for i, video_url in enumerate(urls, start=1):
        try:
            print(f"Downloading Video {i}...")
            youtube = YouTube(video_url)
            video = youtube.streams.get_highest_resolution()
            video.download(output_path=r'C:/Users/abdul/Documents/HackRrev/DeepFake-Spot/youtube_videos')
            print(f"Video {i} downloaded successfully!")
            if i >6:
                break
        except Exception as e:
            print(f"Error downloading Video {i}: {str(e)}")

    print("All videos downloaded.")

if __name__ == "__main__" :
    youtubescrape()