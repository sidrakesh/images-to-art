for file in ~/Downloads/testpics/*
do
  echo "$file"
  outputFolder="testout"
  result=$(echo "$file" | sed "s/testpics/$outputFolder/")
  python3 triangleit.py -n 800 "$file" "$result"
done