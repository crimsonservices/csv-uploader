# Crimson Hexagon CSV Uploader

## Requirements
1. Python 2.7+
2. CSV named `upload.csv`

## Instructions
1. Put CSV named `upload.csv` in directory with Python file
2. Open terminal or command prompt and navigate to directory
3. Run `python upload.py`
4. Done

### CSV Format

author|contents|title|url|date|type|language|latitude|longitude
---|---|---|---|---|---|---|---|---
Tyler Mills|My life is a lie!|Thoughts on Today|https://acme.com/123|2020-01-01T12:00:00|MyRedditComments|en|50.716667|-1.983333

#### Notes

1. Date **must** be in format `2020-01-01T12:00:00`
2. URL **must** be unique for each record
3. You may replace `latitude` and `longitude` for `zipcode` or a combination of `country`, `state` and `city`
4. You may generate fake values for fields you do not have data for
5. You may include the optional columns of `gender` and `age`
6. `type` must match the custom type name generated and provided to you by Crimson Hexagon