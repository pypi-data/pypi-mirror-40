# Pacifica Unique ID
[![Build Status](https://travis-ci.org/pacifica/pacifica-uniqueid.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-uniqueid)
[![Build status](https://ci.appveyor.com/api/projects/status/08piypij9crj4a9n?svg=true)](https://ci.appveyor.com/project/dmlb2000/pacifica-uniqueid)
[![Code Climate](https://codeclimate.com/github/pacifica/pacifica-uniqueid/badges/gpa.svg)](https://codeclimate.com/github/pacifica/pacifica-uniqueid)
[![Issue Count](https://codeclimate.com/github/pacifica/pacifica-uniqueid/badges/issue_count.svg)](https://codeclimate.com/github/pacifica/pacifica-uniqueid)
[![Docker Stars](https://img.shields.io/docker/stars/pacifica/uniqueid.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/uniqueid/general)
[![Docker Pulls](https://img.shields.io/docker/pulls/pacifica/uniqueid.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/uniqueid/general)
[![Docker Automated build](https://img.shields.io/docker/automated/pacifica/uniqueid.svg?maxAge=2592000)](https://cloud.docker.com/swarm/pacifica/repository/docker/pacifica/uniqueid/builds)

This is the pacifica unique ID generator API.

This service provides unique IDs for other pacifica services.

## The API

The Call:
```
curl 'http://localhost:8000/getid?range=10&mode=file'
```
The Response
```
{"endIndex": 9, "startIndex": 0}
```

Select a different mode to get different unique IDs.  If a mode is currently unsupported by the database,
a new row will be started to support it

```
curl 'http://localhost:8000/getid?range=10&mode=file'
curl 'http://localhost:8000/getid?range=10&mode=upload'
```
The Response
```
{"endIndex": 9, "startIndex": 0}
{"endIndex": 9, "startIndex": 0}
```
