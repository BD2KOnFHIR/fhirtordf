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
from typing import Optional, List, Set, Callable

from rdflib import URIRef, Graph, OWL, RDF, BNode
from rdflib.compare import graph_diff
from rdflib.term import Node

from fhirtordf.rdfsupport.namespaces import FHIR
from fhirtordf.rdfsupport.prettygraph import PrettyGraph


def subj_pred_idx_to_uri(s: URIRef, p: URIRef, idx: Optional[int] = None) -> URIRef:
    """ Convert FHIR subject, predicate and entry index into a URI.  The resulting element can be substituted
    for the name of the target BNODE
    :param s: Subject URI (e.g. "fhir:Patient/f201", "fhir:Patient/f201.Patient.identifier_0", ...)
    :param p: Predicate URI (e.g. "fhir:Patient.identifier", "fhir.Identifier.use
    :param idx: Relative position of BNODE if in a list
    :return: URI that can replace the BNODE (e.g. "fhir:Patient/f201
    """
    return URIRef(str(s) + '.' + str(p).rsplit('/', 1)[1] + ("_{}".format(idx) if idx is not None else ''))


def map_node(s: Node, sk_s: URIRef, gin: Graph, gout: Graph) -> None:
    """
    Transform the BNode whose subject is s into its equivalent, replacing s with its 'skolemized' equivalent
    :param s: Actual subject
    :param sk_s: Equivalent URI of subject in output graph
    :param gin: Input graph
    :param gout: Output graph
    """
    for p, o in gin.predicate_objects(s):
        if not isinstance(o, BNode):
            gout.add((sk_s, p, o))
        else:
            sk_o = subj_pred_idx_to_uri(sk_s, p, gin.value(o, FHIR.index))
            gout.add((sk_s, p, sk_o))
            map_node(o, sk_o, gin, gout)


def skolemize(gin: Graph) -> Graph:
    """
    Replace all of the blank nodes in graph gin with FHIR paths
    :param gin: input graph
    :return: output graph
    """
    gout = Graph()

    # Emit any unreferenced subject BNodes (boxes)
    anon_subjs = [s for s in gin.subjects() if isinstance(s, BNode) and len([gin.subject_predicates(s)]) == 0]
    if anon_subjs:
        idx = None if len(anon_subjs) == 1 else 0
        for s in anon_subjs:
            map_node(s, FHIR['treeRoot' + ('_{}'.format(idx) if idx is not None else '')], gin, gout)
            if idx is not None:
                idx += 1

    # Cover all other non-bnode entries
    for subj in set(s for s in gin.subjects() if isinstance(s, URIRef)):
        map_node(subj, subj, gin, gout)
    return gout


def complete_definition(subj: Node,
                        source_graph: Graph,
                        target_graph: Optional[Graph]=None) -> PrettyGraph:
    """
    Return the transitive closure of subject.
    :param subj: URI or BNode for subject
    :param source_graph: Graph containing defininition
    :param target_graph: return graph (for recursion)
    :return: target_graph
    """
    if target_graph is None:
        target_graph = PrettyGraph()
    for p, o in source_graph.predicate_objects(subj):
        target_graph.add((subj, p, o))
        if isinstance(o, BNode):
            complete_definition(o, source_graph, target_graph)
    return target_graph


def dump_nt_sorted(g: Graph) -> List[str]:
    """
    Dump graph g in a sorted n3 format
    :param g: graph to dump
    :return: stringified representation of g
    """
    return [l.decode('ascii') for l in sorted(g.serialize(format='nt').splitlines()) if l]


def rdf_compare(g1: Graph, g2: Graph, ignore_owl_version: bool=False, ignore_type_arcs: bool = False,
                compare_filter: Optional[Callable[[Graph, Graph, Graph], None]]=None) -> str:
    """
    Compare graph g1 and g2
    :param g1: first graph
    :param g2: second graph
    :param ignore_owl_version:
    :param ignore_type_arcs:
    :param compare_filter: Final adjustment for graph difference. Used, for example, to deal with FHIR decimal problems.
    :return: List of differences as printable lines or blank if everything matches
    """
    def graph_for_subject(g: Graph, subj: Node) -> Graph:
        subj_in_g = complete_definition(subj, g)
        if ignore_type_arcs:
            for ta_s, ta_o in subj_in_g.subject_objects(RDF.type):
                if isinstance(ta_s, BNode) and isinstance(ta_o, URIRef):
                    subj_in_g.remove((ta_s, RDF.type, ta_o))
        if ignore_owl_version:
            subj_in_g.remove((subj, OWL.versionIRI, subj_in_g.value(subj, OWL.versionIRI)))
        return subj_in_g

    def primary_subjects(g: Graph) -> Set[Node]:
        anon_subjs = set(anon_s for anon_s in g.subjects()
                         if isinstance(anon_s, BNode) and len([g.subject_predicates(anon_s)]) == 0)
        return set(s_ for s_ in g1.subjects() if isinstance(s_, URIRef)).union(anon_subjs)

    rval = ""

    # Step 1: Find any subjects in one graph that don't exist in the other
    g1_subjs = primary_subjects(g1)
    g2_subjs = primary_subjects(g2)
    for s in g1_subjs - g2_subjs:
        rval += "\n===== Subjects in Graph 1 but not Graph 2: "
        rval += PrettyGraph.strip_prefixes(complete_definition(s, g1))
    for s in g2_subjs - g1_subjs:
        rval += "\n===== Subjects in Graph 2 but not Graph 1: "
        rval += PrettyGraph.strip_prefixes(complete_definition(s, g2))

    # Step 2: Iterate over all of the remaining subjects comparing their contents
    for s in g1_subjs.intersection(g2_subjs):
        s_in_g1 = graph_for_subject(g1, s)
        s_in_g2 = graph_for_subject(g2, s)
        in_both, in_first, in_second = graph_diff(skolemize(s_in_g1), skolemize(s_in_g2))
        if compare_filter:
            compare_filter(in_both, in_first, in_second)
        if len(list(in_first)) or len(list(in_second)):
            rval += "\n\nSubject {} DIFFERENCE: ".format(s) + '=' * 30
            if len(in_first):
                rval += "\n\t----> First: \n" + '\n'.join(dump_nt_sorted(in_first))
            if len(in_second):
                rval += "\n\t----> Second: \n" + '\n'.join(dump_nt_sorted(in_second))
            rval += '-' * 40
    return rval
