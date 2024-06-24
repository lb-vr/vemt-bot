How to contribute with translation
==================================

## install tools
very simply, exec `pip install -r DEVs-requirements.txt` in your local repogitory.
If you already have `xgettext` command, you may not have to exec.

## extract translation targets from codes
if you have used `DEVs-requirements.txt`, hit `pybabel extract --input-dirs ./src/ -o locale/vemt.pot`.
other way is more comvenient with `xgettext`: `find src/ -name '*.py' | xargs xgettext -k"_" --from-code=utf-8 -o locale/vemt.pot -d vemt`

## Translate, translate, translate!
Thanks with your favor, we have more language to use!

## postrogue
I feel there are few people to use these tool other than us :(
