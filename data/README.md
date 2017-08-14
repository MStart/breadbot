## About YAML
* All the data files are based on YAML.
* All the data files are in 'yaml' folder

## How to write data files
* At first you must define a tag in every data file. 
 * Now there're 3 tags: nom, dia, sec
 * nom tag is for knowledge items, they can be searched by 'search' command. 
 * dia tag is for dialoge items, they can not be search, which can improve the performance of nom search. 
 * sec tag is for security items, which can only be viewed by super user.

* Then you can write your datas: 
* Examples 1 (one question with multiple answers)
 * The answer will be selected randomly. 
```
que:
- how are you
ans:
 - Fine, thank you.
 - I am OK.
```
* Example 2 (multiple questions with one answer)
```
que:
- how are you
- how do you do
ans: Fine, thank you.
```
* Example 3 (one block answer)
 * The multiple answer text will output as one block answer.
```
que:
- hello
ans: |
  I'm fine, 
  Thanks
```

## Attention
* 'que' items must all be lower case and without any punctuations. 
* 'ans' items will display randomly, but display all at once if you use 'ans: |'. 
* You should not write ':' in 'ans' items or it will be error when insert the data. 
* add ' when your yaml data is start with [ and end with ].

## Insert data into database
* Run insert.py to insert yaml files into databse. 
* You can use show.py to check the database data. 
