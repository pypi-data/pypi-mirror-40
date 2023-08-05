class TimeLabel:
    def __init__(self, topic, time, duration):
        self.topic = topic
        self.time = time
        self.duration = duration

class Podcast:
    def __init__(self, url, title, date, image, file_name, body, show_notes, audio_url, time_labels):
        self.url = url
        self.title = title
        self.date = date
        self.image = image
        self.file_name = file_name
        self.body = body
        self.show_notes = show_notes
        self.audio_url = audio_url
        self.time_labels = time_labels

def __call_call(endpoint) -> dict:
    from requests import get
    request = get('https://radio-t.com/site-api' + endpoint)
    return request.json()

def get_last_podcasts(count=1) -> list:
    responce = __call_call('/last/' + str(count) + '?categories=podcast')

    podcasts = []
    time_labels = []
    
    for item in responce:
        if 'time_labels' in item:
            for label in item['time_labels']:
                if 'duration' not in label: continue 
                time_label = TimeLabel(topic=label['topic'], time=label['time'], duration=label['duration'])
                time_labels.append(time_label)

        podcast = Podcast(url=item['url'],
                          title=item['title'],
                          date=item['date'],
                          image='' if 'image' not in item else item['image'],
                          file_name='' if 'file_name' not in item else item['file_name'],
                          body=item['body'],
                          show_notes='∂' if 'show_notes' not in item else item['show_notes'],
                          audio_url='' if 'audio_url' not in item else item['audio_url'],
                          time_labels=time_labels)
        podcasts.append(podcast)

    return podcasts