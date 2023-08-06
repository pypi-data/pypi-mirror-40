# I wrote file-manip as a tool too cover my tracks when performing pentests. OS independent.

## Functions:
    
### find_files: Recursive file search, looks for a flag in a filename and returns a list with all files that have that flag in them

    find_files(base_path, flag)

### insert_flag: Inserts a flag into a file, doesn't care about file format, if line_no is not provided then it appends the flag to the end of the file

    insert_flag(flag, fname, line_no = None)

### replace_flag: Similar to insert_flag, however, replace flag replaces a flag with another flag. 

    replace_flag(old_flag, new_flag, fname)

### remove_flag: Removes a flag entirely from a file. *old_file and new_file can be the same file

    remove_flag(flag, old_file, new_file) 

### normalize_str: takes a string and converts to lowercase and normalized to NFKD for tests and comparisons

    normalize_str(string)

### compare_normalized: compares strings that are normalized *very very useful when comparing strangly formatted files
    
    compare_normalized(string_0, string_1)


## To Do:

- add metadata manipulation
    
