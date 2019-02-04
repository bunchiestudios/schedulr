# schedulr

[![Build Status](https://travis-ci.org/bunchiestudios/schedulr.svg?branch=master)](https://travis-ci.org/bunchiestudios/schedulr)

Schedulr is a tool to help you organize and schedule projects with your team. It
lets you setup how long team members will work on differnt projects, gives you
statistics on what everyone is working on, and what projects are missing some
love. This project is currently in development.

## Running

This project requires `python >= 3.6` installed, with a working version of
`pip`.

To run this project, copy the `sample_config.py` file to a `config.py` file.
Fill out all the sample config values. As an example, you might want to add
`sqlite:///test_db.sqlite` as the `DB_STRING` to test with a local database. The
`SECRET_KEY` is a random string of your choice used to generate session strings.

Next, install all dependencies with:
```sh
$ pip3 install -r requirements.txt
```

Finally, copy either `sample_run.bat` or `sample_run.sh` into a `run.{bat,sh}`
(depending on your system) and execute the file. You should have a working
server locally on http://localhost:5000.

## Legal

You can find legal disclosures in the DISCLOSURES.md file in the root of this
project.
You can also find this project's license in the LICENSE file, at the root of
this project.
