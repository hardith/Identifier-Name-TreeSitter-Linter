from tree_sitter import Language, Parser
from pygithub_helper import get_file_contents
from identifier_violation_helper import check_violation
from export_to_csv import export_csv
import sys

def main():
  #Parse input arguments
  from argparse import ArgumentParser
  parser = ArgumentParser()

  parser.add_argument("-g", "--githuburl", dest="githuburl",
                        help="specify the githuburl", metavar="GITHUBURL")
  parser.add_argument("-e", "--extension", dest="extension",
                        help="specify the extension", metavar="EXTENSION")
  parser.add_argument("-l", "--language", dest="language",
                        help="specify the language", metavar="LANGUAGE")
  parser.add_argument("-o1", "--output1", dest="output1",
                        help="specify the output1 file path", metavar="OUTPUT1")
  parser.add_argument("-o2", "--output2", dest="output2",
                        help="specify the output2 file path", metavar="OUTPUT2")

  args = parser.parse_args()

  #Set githubURL
  if args.githuburl is None:
    print("specify the githuburl")
    sys.exit(2)
  else:
    githubURL = args.githuburl

  #Set extension
  if args.extension is None:
    print("Error: specify the extension EX: .py,.js,.go,.rb")
    sys.exit(2)
  else:
    allowed_extension = ['.py','.js','.go','.rb']
    if args.extension not in allowed_extension:
      print("Error: allowed extension are .py,.js,.go,.rb")
      sys.exit(2)
    extension = args.extension
  
  #Set language
  if args.language is None:
    print("Error: specify the language")
    sys.exit(2)
  else:
    allowed_language = ['python','javascript','go','ruby']
    if args.language not in allowed_language:
      print("Error: allowed extension are python,javascript,go,ruby")
      sys.exit(2)
    language = args.language

  #Set output1
  if args.output1 is None:
    print("Error: specify the output1 file path")
    sys.exit(2)
  else:
    output1 = args.output1
  
  #Set output2
  if args.output2 is None:
    print("Error: specify the output2 file path")
    sys.exit(2)
  else:
    output2 = args.output2

  start_execution(githubURL,extension,language,output1,output2)

def start_execution(githubURL,extension,language,output1_path,output2_path):
  

  Language.build_library(
    # Store the library in the `build` directory
    'build/my-languages.so',

    # Include one or more languages
    [
      'languages/tree-sitter-javascript',
      'languages/tree-sitter-python',
      'languages/tree-sitter-go',
      'languages/tree-sitter-ruby',
    ]
  )

  LANGUAGE = Language('build/my-languages.so', language)

  parser = Parser()
  parser.set_language(LANGUAGE)

  #Test source byte string
  # source = bytes("""
  # def foo():
  #     if bar:
  #          baz()
  # """, "utf8")

  # EX: file_content_list = get_file_contents("https://github.com/adaptives/python-examples",".py")
  file_content_list = get_file_contents(githubURL,extension)
  identifier_list = []
  identifier_violation_list = []

  for i in range(len(file_content_list)):

    source = file_content_list[i].decoded_content
    file_path = file_content_list[i].path

    tree = parser.parse(source)

    # create a query for finding all the identifiers in the file
    query = LANGUAGE.query(
          """((identifier) @identifier)
          """
    )

    # run the query with the tree node to find all occurances
    captures = query.captures(tree.root_node)

    # split the source byte string by '\n' so that trversing and looping is easier dynammically
    strList = source.split(b'\n')


    for i in range(len(captures)):

      line_number = captures[i][0].start_point[0]
      start_index = captures[i][0].start_point[1]
      end_index =  captures[i][0].end_point[1]

      name_identifier = strList[line_number][start_index:end_index].decode('utf-8')

      identifier_details = {
        "identifier_name":name_identifier,
        "filepath" : file_path,
        "line_number" : line_number,
        "start_index" : start_index,
        "end_index" : end_index
      }

      identifier_list.append(identifier_details)

      violation_list = check_violation(name_identifier)

      if len(violation_list) > 0:
        identifier_violation_details = {
          "identifier_name":name_identifier,
          "filepath" : file_path,
          "line_number" : line_number,
          "start_index" : start_index,
          "end_index" : end_index,
          "violation_list": ";".join(violation_list)
        }
        identifier_violation_list.append(identifier_violation_details)

  export_csv(identifier_list,output1_path)
  export_csv(identifier_violation_list,output2_path)


if __name__ == "__main__":
  main()
  print("---------------------Finished Execution-------------------------------------")

