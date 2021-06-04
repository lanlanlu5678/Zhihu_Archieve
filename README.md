# SB LBZ

### dependancy
1. python3
2. beautiful soup 4 (by pip)

### set up
1. an archieve directory containing the *archieve_general.py* and *template*
2. define your archieve classes ("photo, dirty words, ..." etc.) by edit the `atype_list` in *archieve_general.py*
3. for each class, creat new directories "class_name/" and "class_name/imgs"

### launch
1. paste the target link to the func `crawling` at the end of *archieve_general.py*
2. select the correct index of desired class
3. mark the img flag to be 1 if want collect pictures
4. mark the link flag to be 1 if want collect links to other websites in the target article
