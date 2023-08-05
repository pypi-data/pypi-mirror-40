import requests
from cryptography.fernet import Fernet
import json

class PlotServerAPI():
    def __init__(self, username, key, api_url, verbose=False):
        self.username = username
        self.key = key 
        self.api_url = api_url
        self.encoder = Fernet(key)
        self.verbose = verbose

    def upload(self, entry, data):
        joined = self.username + data
        raw   = self.encoder.encrypt(joined.encode('utf8'))
        body = {
            "user": self.username,
            "raw" : raw.decode('utf-8')
        }
        res = requests.post(self.api_url + entry, data=json.dumps(body))
        if self.verbose:
            print(res.text)

class Project():
    def __init__(self, name, plot_api, fresh_start=False):
        self.name = name;
        self.fresh_start = fresh_start;
        self.cleaned = not fresh_start;
        self.plot_api = plot_api
        self.files = []
        self.frames = {}
        self.upload_entry = "/api/upload"
        self.prepare_entry = "/api/prepare"
        self.prepared = False

    def prepare_project(self):
        mode = "/append"
        if not self.cleaned:
            mode = "/refresh"
            self.cleaned = True
        raw = json.dumps([self.name, self.files])
        res = self.plot_api.upload(self.prepare_entry+mode, raw)
        self.prepared = True

    def add_files(self, files):
        if self.prepared:
            print("Project: Can't add any files to the project that is already prepared.")
            return
        for file in files:
            self.files.append(file)

    def add_frame(self, file, step, value):
        if not self.prepared:
            print("Project: Project is not prepared. Run prepare_project() first.")
            return
        if file not in self.files:
            print('Project: File {} is not detected in project {}.'.format(file, self.name))
            return
        self.frames[file] = [step, value]

    def send_frames(self):
        raw = json.dumps([self.name, self.frames])
        self.plot_api.upload(self.upload_entry, raw)
        self.frames = {}
