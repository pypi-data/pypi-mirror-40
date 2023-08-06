# JTOS

JSON to SQL. Inspired by the Loopback Query Language, this is a standalone Python library to convert JSON objects to SQL.

## Schema

### Select
```json
{
  "select": {
    "tables": [],
    "fields": []
   }
}
```
### Joins
```json
{
  "join": {
    "type": "LEFT | RIGHT etc",
    "conditions":{
      "from": {
        "table": "",
        "field": ""
      },
      "to": {
        "table": "",
        "field": ""
      }
    } 
  }
}
```

### Where Conditions
```json
{
  "where": [
    {
      "field": "",
      "op": <op>,
      "val": "",
      "join": "o|a"
    }
  ]
}
```

NOTE: An operator should only be included from the second index and it will be prepended to the built string

### Ordering
```json
{
  "select":{
    ...,
    "orderBy": {
      "<field>": "ASC|DESC"
    }
  }
}
```
### Paging
```json
{
  "limit": 100,
  "offset": 3
}
```
### Insert
```json
{
  "insert": {
    "table": "",
    "values": {
      "<field>": "<value>"
    }
  }
}
```


## Operations

* gt - >
* lt - <
* gte - >=
* lte - <=
* e - =
* ne - !=
* l - LIKE
* nl - NOT LIKE
* a - AND
* a - OR

---

## Notes

This does **no** authentication or validation,
it just blindly trusts the tests.

Do not run on production unless you are comfortable with it in your test environment first

## Contributing

Tests, please! But also any work on Upserts or Delete are also greatly appreciated

## TODO

* [X] Select
* [X] Where
* [X] Joins
* [X] Insert
* [ ] Upsert (this syntax is quite different so maybe needs a different parser)
* [X] Delete


## Examples
  
Examples are included in the `tests` directory

