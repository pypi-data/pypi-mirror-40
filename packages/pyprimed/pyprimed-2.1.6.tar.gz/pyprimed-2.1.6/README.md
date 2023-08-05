# pyprimed: a python library to manage PrimedIO

Create a personalized web application that is unique and relevant for each and every user with [Primed.io](https://www.primed.io/).

## Installation
```
pip install pyprimed
```

## Quickstart
### Import the SDK and initiate the connection
```python
from pyprimed.pio import Pio

pio = Pio(uri='http://<user>:<password>@<api_url>:<port>')
```

### Create a Universe, and attach a few Targets
```python
# create a new universe and attach a single target
pio\
  .universes\
  .create(name='myfirstuniverse')\
  .targets\
  .upsert([{'key':'ARTICLE-1', 'value':{'url': 'www.example.com/article-1'}}])

# retrieving the newly created universe
u = pio.universes.filter(name='myfirstuniverse').first

# list all targets currently associated with this universe
for target in u.targets.all():
  print(target.key, target.created_at)

# prepare a list of new targets
new_targets = [
  {'key': 'ARTICLE-2', 'value': {'url': 'www.example.com/article-2'}}, 
  {'key': 'ARTICLE-3', 'value': {'url': 'www.example.com/article-3'}}
]

# upsert the new targets
u.targets.upsert(new_targets)

# targets are upserted, which means that for a given key there
# can be only one instance in the database. Trying to create an
# instance with the same key will update the value of the record
# in the database
u.targets.upsert([{'key':'ARTICLE-1', 'value':{'url': 'THIS IS NEW!'}}])
u.targets.filter(key='ARTICLE-1').first.value 
```

### Create a Model, and attach a few Signals
```python
# create a new model and attach a single signal
pio\
  .models\
  .create(name='myfirstmodel')\
  .signals\
  .upsert([{'key':'ALICE'}])

# retrieving the created model
m = pio.models.filter(name='myfirstmodel').first

# list all signals currently associated with this model
for signal in m.signals.all():
  print(signal.key, signal.created_at)

# prepare a list of new signals
new_signals = [
  {'key': 'BOB'}, 
  {'key': 'CHRIS'}
]

# create the new signals
m.signals.upsert(new_signals)

# prepare a set of predictions (sk stand for signal.key, and tk for target.key)
# WARNING: `sk` and `tk` should always be a string!
predictions = [
  {'sk': 'ALICE', 'tk': 'ARTICLE-1', 'score': 0.35},
  {'sk': 'BOB', 'tk': 'ARTICLE-1', 'score': 0.75}, 
  {'sk': 'CHRIS', 'tk': 'ARTICLE-1', 'score': 0.15}
]

# create the new predictions 
u = pio.universes.filter(name='myfirstuniverse').first

pio\
    .predictions\
    .on(model=m, universe=u)\
    .upsert(predictions)
```

### Create a Campaign, Experiment and set up an AB test to start using the Predictions
```python
from pyprimed.models.abvariant import ControlAbvariant, CustomAbvariant

e = mycampaign.experiments.create(name="myexperiment")

# ControlAbvariant assigns uniformly random scores
# to each of the targets of the associated universe, for
# each personalise call
control = ControlAbvariant(label='A')

# The CustomAbvariant takes a `models` argument that
# allows specifiying multiple models and how much each
# contributes to the final blended score
ab = CustomAbvariant(label='B', models={mymodel: 1.0})

# When attaching A/B variants to the experiment we can
# specify how much traffic should flow to each A/B
# variant
e.abvariants.create({ab: 0.01, control: 0.99})

res1 = c.personalise(keys={'device': 'iphone', 'userid': '123'}, abvariant='A') # abvariant with label 'A' will be returned
```

## Developer
Build the documentation:
```
cd docs && pydocmd build
```

Preview documentation on http://localhost:8000
```
cd docs && pydocmd serve
```