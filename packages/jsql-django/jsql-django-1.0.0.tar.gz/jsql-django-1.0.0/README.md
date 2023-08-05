# jsql-django
#### A JSQL Django plugin for executing hashed queries

# Getting Started
#### Install JSQL Django plugin
```shell
pip install jsql-django
```
#### Include JSQL Django plugin views to your `urls.py` file
##### Import views
```python
from jsql.view import SelectView, InsertView, UpdateView, DeleteView
```
##### Describe urls
```python 
    url('select', SelectView.as_view()),
    url('insert', InsertView.as_view()),
    url('update', UpdateView.as_view()),
    url('delete', DeleteView.as_view()),
```

#### Include ApiKey and MemberKey in your `settings.py` file
```python
API_KEY = 'your_api_key'
MEMBER_KEY = 'your_member_key'
```