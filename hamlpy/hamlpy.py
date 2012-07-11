#!/usr/bin/env python
from nodes import RootNode, FilterNode, HamlNode, create_node
from optparse import OptionParser
import sys

class Compiler:
    def process(self, raw_text):
        split_text = raw_text.strip().split('\n')
        return self.process_lines(split_text)

    def process_lines(self, haml_lines, options=None):
        
        root = RootNode()
        line_iter = iter(haml_lines)

        haml_node=None
        for line_number, line in enumerate(line_iter):
            node_lines = line

            if not isinstance(root.parent_of( HamlNode(line) ), FilterNode):
                if line.count('{') - line.count('}') == 1:
                    start_multiline=line_number # For exception handling

                    while line.count('{') - line.count('}') != -1:
                        try:
                            line = line_iter.next()
                        except StopIteration:
                            raise Exception('No closing brace found for multi-line HAML beginning at line %s' % (start_multiline+1))
                        node_lines += line

            # Blank lines
            if haml_node is not None and len(node_lines.strip()) == 0:
                haml_node.newlines += 1
            else:
                haml_node = create_node(node_lines)
                root.add_node(haml_node)
                
        if options and options.debug_tree:
            return root.debug_tree()
        else:
            return root.render()

def convert_files():
    import sys
    import codecs

    parser = OptionParser()
    parser.add_option("-d", "--debug-tree", dest="debug_tree",
    action="store_true", help="Print the generated tree instead of the HTML")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        print "Specify the input file as the first argument."
    else: 
        infile = args[0]
        haml_lines = codecs.open(infile, 'r', encoding='utf-8').read().splitlines()

        compiler = Compiler()
        output = compiler.process_lines(haml_lines, options=options)
        
        # TODO: I broke this
        if len(args) == 2:
            outfile = codecs.open(args[1], 'w', encoding='utf-8')
            outfile.write(output)
        else:
            print output

if __name__ == '__main__':
    convert_files()
