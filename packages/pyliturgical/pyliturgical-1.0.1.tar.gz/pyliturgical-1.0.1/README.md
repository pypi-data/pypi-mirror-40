# pyliturgical

[![CircleCI](https://circleci.com/gh/pizen/pyliturgical/tree/master.svg?style=svg)](https://circleci.com/gh/pizen/pyliturgical/tree/master)

**Library for getting liturgical information, such as color, for a date.**

Example:

```python
>>> from pyliturgical import calendar
>>> from datetime import date
>>> calendar.lookup(date(2018, 12, 25))
('Christmas Day', 'white')
```
