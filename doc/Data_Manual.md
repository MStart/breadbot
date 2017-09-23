## About YAML
* All the data files are based on YAML.
* All the data files are in "yaml" folder

## How to write data files
* At first you must define a tag in every data file. 
 * Now there're 3 tags: nom, dia, sec
 * nom tag is for knowledge items, they can be searched. 
 * dia tag is for dialoge items, they can not be searched, but for talking.
 * sec tag is for security items, which can only be viewed by super user.

## Some examples
* Examples 1 (one question with multiple answers)
 * The answer will be display randomly. 
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
ans:
- Fine, thank you.
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
* "que" items must all be lower case and without any punctuations. 
* You should not write ":" in "ans" items or it will be an error when insert the data. 
* Do not use boolean values. For example: single word "true", "false", "yes", "no"...
* add "'" around your data when start with "[" and end with "]".

## Insert data into database
* Launch the bread-console
* Type "insert" to insert yaml files into databse. 
* Type "show" to show all the data from database for checking.
