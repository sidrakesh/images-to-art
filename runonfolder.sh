for file in ~/Downloads/testpics1/*
do
  echo "$file"
  outputFolder="testout1"
  result=$(echo "$file" | sed "s/testpics1/$outputFolder/")
  python3 triangleit.py -n 800 "$file" "$result"
done