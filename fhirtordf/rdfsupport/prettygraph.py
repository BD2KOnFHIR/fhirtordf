# Copyright (c) 2017, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the Mayo Clinic nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
import re
from rdflib import Graph, BNode, Literal
from rdflib.plugins.serializers.turtle import TurtleSerializer, SUBJECT, VERB, _GEN_QNAME_FOR_DT
from rdflib.namespace import NAME_START_CATEGORIES, RDF


# Two changes to the serializer -- one is in the label routine where the serializer (deliberately) mangles the
# format. (use_plain=True).  The second is the actual layout...

class TurtleSeriailizerMod(TurtleSerializer):
    """
    TurtleSerializerMod is an override to the basic TurtleSerializer.

    This change has been tested against rdflib 4.2.2
    other versions may or may not work.
    """
    def label(self, node, position):
        if node == RDF.nil:
            return '()'
        if position is VERB and node in self.keywords:
            return self.keywords[node]
        if isinstance(node, Literal):
            return node._literal_n3(
                # use_plain=True,
                use_plain=False,
                qname_callback=lambda dt: self.getQName(
                    dt, _GEN_QNAME_FOR_DT))
        else:
            node = self.relativize(node)

            return self.getQName(node, position == VERB) or node.n3()

    def p_squared(self, node, position, newline=False):
        if (not isinstance(node, BNode) or node in self._serialized or
                self._references[node] > 1 or position == SUBJECT):
            return False

        if not newline:
            self.write(' ')

        if self.isValidList(node):
            # this is a list
            self.write('(')
            self.depth += 1  # 2
            self.doList(node)
            self.depth -= 1  # 2
            self.write(' )')
        else:
            self.subjectDone(node)
            self.depth += 1
            self.write('[\n' + self.indent())
            # self.write('[')
            self.depth -= 1
            self.predicateList(node, newline=True)
            # self.predicateList(node, newline=False)
            self.write('\n' + self.indent() + ']')
            # self.write(' ]')
            # self.depth -= 1

        return True
TurtleSerializer.p_squared = TurtleSeriailizerMod.p_squared
TurtleSerializer.label = TurtleSeriailizerMod.label

# The following change allows numeric concept identifiers in turtle output.  It is necessary for coding schemes
# such as SNOMED CT.
NAME_START_CATEGORIES.append('Nd')


class PrettyGraph(Graph):
    @staticmethod
    def strip_prefixes(g: Graph):
        """ Remove the prefixes from the graph for aesthetics """
        return re.sub(r'^@prefix .* .\n', '',
                      g.serialize(format="turtle").decode(),
                      flags=re.MULTILINE).strip()

    def serialize(self, format='turtle', **args):
        assert len(args) == 0, "All arguments to serialize are fixed"

        return super().serialize(format=format, spacious=False).decode('utf-8')
