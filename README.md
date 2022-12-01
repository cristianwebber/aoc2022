advent of code 2022
===================

https://adventofcode.com/2022

Copy Cookie Session to .env (Inspect on Browser >> Application >> Cookies)


```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pre-commit install

cp -r day00 day01
cd day01
aoc-download-input

py
python3 part1.py input.txt | aoc-submit --part 1

cp part1.py part2.py

```
