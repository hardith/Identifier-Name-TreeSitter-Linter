# Identifier-Name-TreeSitter-Linter
Python script to fetch all the identifiers from '.py','.js','.go','.rb' files from a public github repo and then check if the identifiers violate the simon butler naming convention

## Installation

This package currently only works with Python 3. There are no library dependencies, but you do need to have a C compiler installed. The following URL shows how to setup c compiler
https://code.visualstudio.com/docs/languages/cpp

```sh
pip3 install tree_sitter
pip3 install PyGithub
pip3 install pyenchant
pip3 install word2number
```
## Create GitHub Personal Access Token
In order to use PyGithub a personal access token of minimum permission "public repo" needs to be created and needs to be replaced in the "pygithub_helper.py" file at line 6. To setup the personal access token follow the link https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

```sh
token = "EnterToken"
```

Example:
```sh
#this token has been deactivated
token = "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"
```

## Usage
First you'll need a Tree-sitter language implementation for each language that you want to parse. You can clone some of the [existing language repos](https://github.com/tree-sitter) or [create your own](http://tree-sitter.github.io/tree-sitter/creating-parsers) and clone all the necessary parsers in the "languages" folder.

```sh
git clone https://github.com/tree-sitter/tree-sitter-go
git clone https://github.com/tree-sitter/tree-sitter-ruby
git clone https://github.com/tree-sitter/tree-sitter-javascript
git clone https://github.com/tree-sitter/tree-sitter-python
```

## Execution
To execute the solution after all the installation, use the below format to run the solution
```sh
python identifier-name-linter.py -g "github root url" -e "extension" -l "language" -o1 "output1 path" -o2 "output2 path"
```
Ex:
```sh
python identifier-name-linter.py -g "https://github.com/adaptives/python-examples" -e ".py" -l "python" -o1 "output1/output1.csv" -o2 "output2/output2.csv"
```

## Rules
Below are the set of instructions on how the input is passed.
* Address of a public GitHub repository
* File extension, only .py .js .go .rb allowed
* Name of Programming Language, only python, ruby, go and javascript allowed
* Filepath for output1
    (Output1 will contain list of names and locations of all identifiers in the program)
* Filepath for output2
    (Output2 will contain name and location of all identifiers that violate the following simon butler naming convention, along with the rule that they violate) 
