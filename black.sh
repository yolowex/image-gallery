# this only works on linux
find . -type f -name "*.py" -print0 | xargs -0 black
