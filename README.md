# Smart-Document-Retrieval-System


* Document Structure Visualisation 
```
Document
|
|-- Title (Autocomplete Search)
|
|-- Content
|   |-- Eliminate stop words, tokens < 3 characters, and HTML
|   |-- Stem words
|
|-- Authors
|   |-- Array of author objects
|       |-- First name
|       |-- Last name
|       |-- Email
|
|-- Date (Publication Date)
|   |-- Date object
|
|-- Geopoint
|   |-- Longitude
|   |-- Latitude
|
|-- TemporalExpressions
|   |-- List of temporal expressions
|
|-- Georeferences
    |-- List of georeferenced expressions
``` 
