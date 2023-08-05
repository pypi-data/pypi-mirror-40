from git import Repo
from git.util import Actor
import yaml
import os
import StringIO

class GitYamlDB(object):
    def __init__(self, data_dir):
        self._data_dir = data_dir

        self._yamls = {}  # {file, yaml}
        self._observers = []  # call observers on save
        self._repo = None

        self._init_repo()

    def _init_repo(self):
        if os.path.exists(self._data_dir):
            self._repo = Repo(self._data_dir)
        else:
            self._repo = Repo.init(self._data_dir)

    def _get_filename(self, filename):
        return os.path.join(self._data_dir, '%s.yml' % filename)

    def _commit(self, message, name, email):
        actor = Actor(name, email)
        self._repo.git.add(A=True)
        self._repo.index.commit(message,
                                author=actor,
                                committer=actor)

    def open(self, filename):
        if os.path.exists(self._get_filename(filename)):
            with open(self._get_filename(filename)) as f:
                self._yamls[filename] = yaml.load(f)
        else:
            self._yamls[filename] = {}

        def deep(data):
            if isinstance(data, dict) and '_link' in data:
                data.update(self.open(data['_link']))
            if isinstance(data, dict):
                for key in data:
                    deep(data[key])
            if isinstance(data, list):
                for it in data:
                    deep(it)
        deep(self._yamls[filename])

        return self._yamls[filename]

    def save_one(self, filename):
        if not os.path.exists(os.path.dirname(self._get_filename(filename))):
            os.makedirs(os.path.dirname(self._get_filename(filename)))
        with open(self._get_filename(filename), 'w') as f:
            yaml.dump(self._yamls[filename], f, default_flow_style=False)


    def save(self, message, name, email, commit=True):
        for filename, data in self._yamls.items():
            def deep(data):
                if isinstance(data, dict) and '_link' in data:
                    linked = self.open(data['_link'])
                    linked.update(data)
                    del linked['_link']
                    self.save_one(data['_link'])
                    for key in data.keys():
                        if key != '_link':
                            del data[key]
                if isinstance(data, dict):
                    for key in data:
                        deep(data[key])
                if isinstance(data, list):
                    for it in data:
                        deep(it)
            deep(self._yamls[filename])

            if not os.path.exists(os.path.dirname(self._get_filename(filename))):
                os.makedirs(os.path.dirname(self._get_filename(filename)))
            with open(self._get_filename(filename), 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
        if commit:
            self._commit(message, name, email)
        # Call observers
        for observer in self._observers:
            observer(self)

    def _get_all_filenames(self):
        filenames = []
        for root, _, files in os.walk(self._data_dir, topdown=True):
            for file in files:
                filename = os.path.join(root, file)
                if os.path.join(self._data_dir, '.git') in root:
                    continue
                filenames.append(filename[len('%s/' % self._data_dir):-len('.yml')])
        return filenames
            

    def validate(self, filename):
        def _formatted():
            self.open(filename)
            f = StringIO.StringIO()
            yaml.dump(self._yamls[filename], f, default_flow_style=False)
            f.seek(0)
            return f.read()
        def _original():
            with open(self._get_filename(filename)) as f:
                return f.read()
        return _original() == _formatted()

    def validate_all(self):
        for filename in self._get_all_filenames():
            if not self.validate(filename):
                return False
        return True

    def reformate(self, filename, name, email, save=True):
        self.open(filename)
        if save:
            self.save('[auto] Reformate %s' % filename, name, email)
    
    def reformate_all(self, name, email, commit=False):
        for filename in self._get_all_filenames():
            self.open(filename)
        self.save('[auto] Reformate all', name, email, commit=commit)