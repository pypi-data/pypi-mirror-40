import torch
import os
from collections import defaultdict

import shutil


class Session(object):
    """Session(model, **args)

    Attributes:
      name (str): A shorthand name for the session, such as 'autoencoder-1'
      description (str): A longer description of the session and it's purpose
      metrics (dict): A set of metrics that were measured over training and/or
        evaluation
      epoch (int): The most recently completed epoch of training
      model (torch.nn.Module): A torch machine learning model, or list of models.
      optim (torch.optim.Optimizer): Some optimizer or list of optimizers for
        your model(s).
    """

    def __init__(self, model=None, optim=None):
        super().__init__()
        self.model = model
        self.optim = optim

        self.name = 'Unnamed Model'
        self.description = 'N/A'
        self.metrics = defaultdict(lambda: [])
        self.epoch = 0

        self.resumed = False

    ##############################################################################
    # SETTINGS METHODS                                                           #
    ##############################################################################

    def rename(self, name):
        """Name setter alias method"""
        self.set_name(name)

    def set_name(self, name):
        self.name = name

    def describe(self, description=None):
        """Description setter alias method"""
        self.set_description(description)

    def set_description(self, description):
        """description getter/setter method"""
        self.description = description

    def set_optim(self, optim):
        self.optim = optim

    def set_model(self, model):
        self.model = model

    ##############################################################################
    # INTERFACE METHODS                                                          #
    ##############################################################################

    def next_epoch(self):
        self.epoch += 1

    def append_metrics(self, metrics):
        for key in metrics:
            self.metrics[key].append(metrics[key])

    def resume(self):
        """Resume a session for training."""
        if not self.model and not self.optim:
            raise AttributeError("Model and Optimizer not set. Set them before resuming/suspending a session.")

        if not self.resumed:
            # self.next_epoch()
            self.resumed = True

    def suspend(self):
        """Suspend a session for later."""
        if not self.model and not self.optim:
            raise AttributeError("Model and Optimizer not set. Set them before resuming/suspending a session.")

        self.resumed = False

    def save(self, path):
        """Save existing state of session to a particular file"""
        if not os.path.exists(os.path.dirname(path)):
            raise ValueError(f"Path {path} does not exist. Did you mistype any subfolders?")

        # model_state = None
        if type(self.model) in (list, tuple):
            model_state = [m.state_dict() for m in self.model]
        else:
            model_state = self.model.state_dict()

        # optim_state = None
        if type(self.optim) in (list, tuple):
            optim_state = [o.state_dict() for o in self.optim]
        else:
            optim_state = self.optim.state_dict()

        session = {
            'name': self.name,
            'description': self.description,
            'metrics': dict(self.metrics),
            'epoch': self.epoch,
            'model_state': model_state,
            'optim_state': optim_state,
        }

        torch.save(session, path)

    def load(self, path):
        """Load a session from a file."""

        if not os.path.exists(path):
            raise ValueError(f"Path '{path}' does not exist. Did you mistype any subfolders?")

        session = torch.load(path)

        model_state = session['model_state']

        if type(self.model) in (list, tuple):
            for m, s in zip(self.model, model_state):
                m.load_state_dict(s)
        else:
            self.model.load_state_dict(model_state)

        optim_state = session['optim_state']
        if type(self.optim) in (list, tuple):
            for o, s in zip(self.optim, optim_state):
                o.load_state_dict(s)
        else:
            self.optim.load_state_dict(optim_state)

        self.name = session['name']
        self.description = session['description']
        self.metrics = defaultdict(lambda: [], session['metrics'])
        self.epoch = session['epoch']


class AutoSession(Session):
    """Autosaving Session

    """

    def __init__(self, model, optim, save_path=None, save_frequency=1):
        super().__init__(model, optim)
        self.set_frequency(save_frequency)
        self.save_path = save_path

    ##############################################################################
    # SETTINGS METHODS                                                           #
    ##############################################################################

    def set_frequency(self, frequency):
        """Set how often to actually save your session"""
        self.frequency = frequency
        self.counter = self.epoch % frequency

    def get_frequency(self):
        return self.frequency

    def set_save_path(self, path):
        self.save_path = path

    ##############################################################################
    # INTERFACE METHODS                                                          #
    ##############################################################################

    def load(self, path):
        """Load a particular training session"""
        super().load(path)
        self.save_path = path

    def save(self, path=None):
        return self.autosave(path)

    def autosave(self, path=None):
        if not self.resumed:
            raise AttributeError("Begin training before trying to save.")
        elif not path and not self.save_path:
            raise AttributeError("Either specify a path through this method or set one via set_save_path(path)")

        self.counter += 1
        if self.counter == self.frequency:
            self.counter = 0
            path = path if path is not None else self.save_path
            self._save(path)
            return True
        else:
            return False

    def _save(self, path):
        if not os.path.exists(os.path.dirname(path)):
            raise ValueError(f"Path {path} does not exist. Did you mistype any subfolders?")

        # model_state = None
        if type(self.model) in (list, tuple):
            model_state = [m.state_dict() for m in self.model]
        else:
            model_state = self.model.state_dict()

        # optim_state = None
        if type(self.optim) in (list, tuple):
            optim_state = [o.state_dict() for o in self.optim]
        else:
            optim_state = self.optim.state_dict()

        session = {
            'name': self.name,
            'description': self.description,
            'metrics': dict(self.metrics),
            'epoch': self.epoch,
            'model_state': model_state,
            'optim_state': optim_state,
        }

        torch.save(session, path)

def session_test():
    title('session')

    subtest(1, "Basic Initialization")
    model = torch.nn.Linear(10, 1)
    optim = torch.optim.Adam(model.parameters(), 1e-4)

    session = Session(model, optim)

    passed = True
    passed = passed if session.model is model else False
    passed = passed if session.optim is optim else False
    passed = passed if session.name == 'Unnamed Model' else False
    passed = passed if session.description == 'N/A' else False
    passed = passed if session.epoch == 0 else False
    passed = passed if len(session.metrics) == 0 else False
    passed = passed if not session.resumed else False
    evaluate(passed)

    subtest(2, "Setters")
    session.rename("TEST")
    session.describe("A TEST")
    session.resume()
    session.suspend()

    passed = True
    passed = passed if session.name == "TEST" else False
    passed = passed if session.description == "A TEST" else False
    passed = passed if session.epoch == 0 else False
    passed = passed if session.resumed == False else False
    evaluate(passed)

    subtest(3, "Saving and Loading")
    try:
        os.mkdir('test_folder')
    except:
        pass

    session.epoch = 12
    session.save("./test_folder/session_test.sesh")

    model2 = torch.nn.Linear(10, 1)
    optim2 = torch.optim.Adam(model2.parameters(), 1e-4)
    session2 = Session(model2, optim2)
    session2.load("./test_folder/session_test.sesh")

    passed = True
    passed = passed if session2.epoch == 12 else False
    passed = passed if session2.name == "TEST" else False
    passed = passed if session2.description == "A TEST" else False
    passed = passed if session2.resumed == False else False
    evaluate(passed)

    subtest(4, "Multiple Models")

    model1 = (test.Model(), test.Model())
    optim1 = (test.optim(model1[0].parameters()), test.optim(model1[1].parameters()))
    session = Session(model1, optim1)

    if os.path.exists('./test_folder'):
        shutil.rmtree('./test_folder')
        os.makedirs('./test_folder')

    session.save('./test_folder/session.sesh')


    model2 = (test.Model(), test.Model())
    optim2 = (test.optim(model2[0].parameters()), test.optim(model2[1].parameters()))
    session = Session(model2, optim2)
    session.load('./test_folder/session.sesh')

    passed = True

    for k1, k2 in zip(session.model[0].state_dict().values(), model1[0].state_dict().values()):
        passed = passed if torch.equal(k1, k2) else False

    evaluate(passed)

    end()

    if os.path.exists('./test_folder'):
        shutil.rmtree('./test_folder')
        os.makedirs('./test_folder')


def autosession_test():
    shutil.rmtree('./test_folder')

    title("Auto-Session")
    model = torch.nn.Linear(10, 1)
    optim = torch.optim.Adam(model.parameters(), 1e-4)
    session = AutoSession(model, optim)

    subtest(1, "Begin/End Training")
    passed = True

    session.resume()
    passed = passed if session.epoch == 0 else False
    passed = passed if session.resumed else False

    session.suspend()
    passed = passed if session.resumed == False else False
    evaluate(passed)

    subtest(2, "Storing Metrics")
    passed = True
    session.append_metrics({
        'Loss': 0,
        'Validation': 2
    })
    passed = passed if session.metrics['Loss'][-1] == 0 else False
    passed = passed if session.metrics['Validation'][-1] == 2 else False
    evaluate(passed)

    subtest(3, "Save Frequencies (Frequency 1)")
    session.epoch = 0
    session.resume()
    passed = True
    passed = passed if session.autosave('test_folder/autosession_test.sesh') else False
    passed = passed if session.autosave('test_folder/autosession_test.sesh') else False
    session.suspend()
    evaluate(passed)

    # Frequency of 2
    subtest(4, "Save Frequencies (Frequency 2)")
    session.epoch = 0
    session.set_frequency(2)
    session.resume()
    passed = True
    passed = passed if not session.autosave('test_folder/autosession_test.sesh') else False
    passed = passed if session.autosave('test_folder/autosession_test.sesh') else False
    passed = passed if not session.autosave('test_folder/autosession_test.sesh') else False
    passed = passed if session.autosave('test_folder/autosession_test.sesh') else False
    session.suspend()
    evaluate(passed)

    subtest(5, "Loading an Old Session")
    model2 = torch.nn.Linear(10, 1)
    optim2 = torch.optim.Adam(model2.parameters(), 1e-4)
    session2 = AutoSession(model2, optim2)
    session2.load('test_folder/autosession_test.sesh')

    passed = True
    passed = passed if session2.metrics['Loss'][-1] == 0 else False
    passed = passed if session2.metrics['Validation'][-1] == 2 else False
    evaluate(passed)

    subtest(6, "Multiple Models")
    if os.path.exists('./test_folder'):
        shutil.rmtree('./test_folder')
        os.makedirs('./test_folder')

    model_a = (test.Model(), test.Model)
    optim_a = (test.optim(model_a[0].parameters()), test.optim(model_a[1].parameters()))
    session = AutoSession(model_a, optim_a)

    session.save('test_folder/session.sesh')



    end()
    shutil.rmtree('./test_folder')

if __name__ == '__main__':
    session_test()
    autosession_test()
