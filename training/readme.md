`vjtools.py` is a bot to grab scoreboard on [vjudge](https://vjudge.net/group/monashicpc), it reads contest ids from standard input.

* Run: `echo <contest_id> | python vjtools.py`, e.g. `echo 383886 385030 388138 | python vjtools.py`

* You can find `contest_ids` from the URL of the contest, e.g. `https://vjudge.net/contest/361790`

* You may need to update the parser as the format of web page keep changing.
