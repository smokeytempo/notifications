import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QLabel, QCheckBox, QGridLayout, QTabWidget
from PyQt5.QtCore import QTimer
import schedule
import time
import threading
import requests
import json
import os
from plyer import notification

class EventNotificationSystem(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Event Notification System')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget, 0, 0, 1, 3)

        self.platforms_tab = QWidget()
        self.tab_widget.addTab(self.platforms_tab, 'Platforms')

        self.platforms_layout = QGridLayout()
        self.platforms_tab.setLayout(self.platforms_layout)

        self.platforms_label = QLabel('Platforms:')
        self.platforms_layout.addWidget(self.platforms_label, 0, 0)

        self.platforms_combo = QComboBox()
        self.platforms_combo.addItems(['GitHub', 'Twitter', 'Instagram', 'TikTok', 'YouTube', 'Reddit', 'Discord', 'Telegram', 'Google Calendar'])
        self.platforms_layout.addWidget(self.platforms_combo, 0, 1)

        self.username_label = QLabel('Username:')
        self.platforms_layout.addWidget(self.username_label, 1, 0)

        self.username_input = QLineEdit()
        self.platforms_layout.addWidget(self.username_input, 1, 1)

        self.api_key_label = QLabel('API Key:')
        self.platforms_layout.addWidget(self.api_key_label, 2, 0)

        self.api_key_input = QLineEdit()
        self.platforms_layout.addWidget(self.api_key_input, 2, 1)

        self.last_post_time_label = QLabel('Last Post Time:')
        self.platforms_layout.addWidget(self.last_post_time_label, 3, 0)

        self.last_post_time_input = QLineEdit()
        self.platforms_layout.addWidget(self.last_post_time_input, 3, 1)

        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.add_platform)
        self.platforms_layout.addWidget(self.add_button, 4, 0)

        self.platforms_list_label = QLabel('Platforms List:')
        self.platforms_layout.addWidget(self.platforms_list_label, 5, 0)

        self.platforms_list = []
        self.platforms_list_widget = QVBoxLayout()
        self.platforms_list_container = QWidget()
        self.platforms_list_container.setLayout(self.platforms_list_widget)
        self.platforms_layout.addWidget(self.platforms_list_container, 6, 0, 1, 2)

        self.settings_tab = QWidget()
        self.tab_widget.addTab(self.settings_tab, 'Settings')

        self.settings_layout = QGridLayout()
        self.settings_tab.setLayout(self.settings_layout)

        self.interval_label = QLabel('Interval (minutes):')
        self.settings_layout.addWidget(self.interval_label, 0, 0)

        self.interval_input = QLineEdit()
        self.interval_input.setText('1')
        self.settings_layout.addWidget(self.interval_input, 0, 1)

        self.notification_type_label = QLabel('Notification Type:')
        self.settings_layout.addWidget(self.notification_type_label, 1, 0)

        self.notification_type_combo = QComboBox()
        self.notification_type_combo.addItems(['System Notification', 'Discord', 'Telegram'])
        self.settings_layout.addWidget(self.notification_type_combo, 1, 1)

        self.discord_channel_id_label = QLabel('Discord Channel ID:')
        self.settings_layout.addWidget(self.discord_channel_id_label, 2, 0)

        self.discord_channel_id_input = QLineEdit()
        self.settings_layout.addWidget(self.discord_channel_id_input, 2, 1)

        self.telegram_bot_token_label = QLabel('Telegram Bot Token:')
        self.settings_layout.addWidget(self.telegram_bot_token_label, 3, 0)

        self.telegram_bot_token_input = QLineEdit()
        self.settings_layout.addWidget(self.telegram_bot_token_input, 3, 1)

        self.telegram_chat_id_label = QLabel('Telegram Chat ID:')
        self.settings_layout.addWidget(self.telegram_chat_id_label, 4, 0)

        self.telegram_chat_id_input = QLineEdit()
        self.settings_layout.addWidget(self.telegram_chat_id_input, 4, 1)

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_notification_system)
        self.layout.addWidget(self.start_button, 1, 0)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_notification_system)
        self.layout.addWidget(self.stop_button, 1, 1)

        self.notification_system_running = False

    def add_platform(self):
        platform = self.platforms_combo.currentText()
        username = self.username_input.text()
        api_key = self.api_key_input.text()
        last_post_time = self.last_post_time_input.text()
        if platform and username and api_key and last_post_time:
            self.platforms_list.append((platform, username, api_key, last_post_time))
            self.update_platforms_list()

    def update_platforms_list(self):
        self.platforms_list_widget.clear()
        for platform, username, api_key, last_post_time in self.platforms_list:
            label = QLabel(f'{platform}: {username} - API Key: {api_key} - Last Post Time: {last_post_time}')
            self.platforms_list_widget.addWidget(label)

    def start_notification_system(self):
        if not self.notification_system_running:
            self.notification_system_running = True
            self.thread = threading.Thread(target=self.run_notification_system)
            self.thread.start()

    def stop_notification_system(self):
        if self.notification_system_running:
            self.notification_system_running = False

    def run_notification_system(self):
        interval = int(self.interval_input.text())
        while self.notification_system_running:
            for platform, username, api_key, last_post_time in self.platforms_list:
                if platform == 'GitHub':
                    self.check_github_events(username, api_key, last_post_time)
                elif platform == 'Twitter':
                    self.check_twitter_events(username, api_key, last_post_time)
                elif platform == 'Instagram':
                    self.check_instagram_events(username, api_key, last_post_time)
                elif platform == 'TikTok':
                    self.check_tiktok_events(username, api_key, last_post_time)
                elif platform == 'YouTube':
                    self.check_youtube_events(username, api_key, last_post_time)
                elif platform == 'Reddit':
                    self.check_reddit_events(username, api_key, last_post_time)
                elif platform == 'Discord':
                    self.check_discord_events(username, api_key, last_post_time)
                elif platform == 'Telegram':
                    self.check_telegram_events(username, api_key, last_post_time)
                elif platform == 'Google Calendar':
                    self.check_google_calendar_events(username, api_key, last_post_time)
            time.sleep(interval * 60)

    def check_github_events(self, username, api_key, last_post_time):
        url = f'https://api.github.com/users/{username}/events'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            events = json.loads(response.text)
            for event in events:
                if event['type'] == 'PushEvent' and event['created_at'] > last_post_time:
                    self.send_notification('GitHub', f'New push event detected for {username}')

    def check_twitter_events(self, username, api_key, last_post_time):
        url = f'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={username}&count=1'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tweets = json.loads(response.text)
            for tweet in tweets:
                if tweet['created_at'] > last_post_time:
                    self.send_notification('Twitter', f'New tweet detected for {username}')

    def check_instagram_events(self, username, api_key, last_post_time):
        url = f'https://graph.instagram.com/{username}/media?fields=id,media_url,timestamp&access_token={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            media = json.loads(response.text)
            for item in media['data']:
                if item['timestamp'] > last_post_time:
                    self.send_notification('Instagram', f'New media detected for {username}')

    def check_tiktok_events(self, username, api_key, last_post_time):
        url = f'https://api.tiktok.com/v2/user/info/{username}'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_info = json.loads(response.text)
            if user_info['created'] > last_post_time:
                self.send_notification('TikTok', f'New media detected for {username}')

    def check_youtube_events(self, username, api_key, last_post_time):
        url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={username}&type=video&maxResults=1&key={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            videos = json.loads(response.text)
            for video in videos['items']:
                if video['snippet']['publishedAt'] > last_post_time:
                    self.send_notification('YouTube', f'New video detected for {username}')

    def check_reddit_events(self, username, api_key, last_post_time):
        url = f'https://www.reddit.com/user/{username}/.json'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_info = json.loads(response.text)
            for post in user_info['data']['children']:
                if post['data']['created_utc'] > last_post_time:
                    self.send_notification('Reddit', f'New post detected for {username}')

    def check_discord_events(self, username, api_key, last_post_time):
        url = f'https://discord.com/api/v9/guilds/{self.discord_channel_id_input.text()}/channels/{self.discord_channel_id_input.text()}/messages'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            messages = json.loads(response.text)
            for message in messages:
                if message['author']['username'] == username and message['created_at'] > last_post_time:
                    self.send_notification('Discord', f'New message detected for {username}')

    def check_telegram_events(self, username, api_key, last_post_time):
        url = f'https://api.telegram.org/bot{api_key}/getUpdates'
        response = requests.get(url)
        if response.status_code == 200:
            updates = json.loads(response.text)
            for update in updates['result']:
                if update['message']['from']['username'] == username and update['message']['date'] > last_post_time:
                    self.send_notification('Telegram', f'New message detected for {username}')

    def check_google_calendar_events(self, username, api_key, last_post_time):
        url = f'https://www.googleapis.com/calendar/v3/calendars/primary/events?maxResults=1&key={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            events = json.loads(response.text)
            for event in events['items']:
                if event['start']['dateTime'] > last_post_time:
                    self.send_notification('Google Calendar', f'New event detected for {username}')

    def send_notification(self, platform, message):
        notification_type = self.notification_type_combo.currentText()
        if notification_type == 'System Notification':
            notification.notify(
                title=f'{platform} Notification',
                message=message,
                app_name='Event Notification System',
                timeout=10
            )
        elif notification_type == 'Discord':
            url = f'https://discord.com/api/v9/channels/{self.discord_channel_id_input.text()}/messages'
            data = {'content': message}
            response = requests.post(url, json=data, headers={'Authorization': f'Bearer {self.api_key_input.text()}'})
            if response.status_code == 200:
                print(f'Discord notification sent for {platform}')
        elif notification_type == 'Telegram':
            url = f'https://api.telegram.org/bot{self.telegram_bot_token_input.text()}/sendMessage'
            data = {'chat_id': self.telegram_chat_id_input.text(), 'text': message}
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print(f'Telegram notification sent for {platform}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EventNotificationSystem()
    window.show()
    sys.exit(app.exec_())
