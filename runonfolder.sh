for file in ~/Downloads/testpics3/*
do
  echo "$file"
  outputFolder="testout7"
  result=$(echo "$file" | sed "s/testpics3/$outputFolder/")
  python3 convert-to-stars.py -n 800 -b medium "$file" "$result"
done