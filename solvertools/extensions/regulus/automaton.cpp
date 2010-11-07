/*
# Copyright (c) 2010, Alex Schwendner
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials
#       provided with the distribution.
#     * Neither the name of the Manic Sages nor the names of its
#       contributors may be used to endorse or promote products
#       derived from this software without specific prior written
#       permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
*/

#include <assert.h>
#include <iostream>
#include <math.h>
#include <sstream>
#include "automaton.h"


bool Automaton::checkEdge(const Edge &e) const {
  return(0 <= e.dest &&
	 e.dest < nodes.size());
}

Automaton::Node::Node() :
  fingerprint(0) {
  ;
}

Automaton::Node Automaton::transformNode(const Node &v, size_t a, size_t b) {
  Node w = v;
  for(int i = 0; i < 26; ++i) {
    if(w.fingerprint & (1 << i))
      w.letterEdge[i].dest = a * w.letterEdge[i].dest + b;
  }
  for(size_t i = 0; i < w.epsilonEdges.size(); ++i) {
    w.epsilonEdges[i].dest = a * w.epsilonEdges[i].dest + b;
  }
  return(w);
}

Automaton::Node Automaton::translateNode(size_t offset, const Node &v) {
  return(transformNode(v, 1, offset));
}

Automaton::Node Automaton::mapNode(const std::vector<long> &mapsTo, const Node &v) {
  Node w = v;
  for(uint_fast8_t i = 0; i < 26; ++i) {
    if(w.fingerprint & (1 << i)) {
      if(mapsTo[w.letterEdge[i].dest] == -1) {
	w.fingerprint &= ~(1 << i);
      } else {
	w.letterEdge[i].dest = mapsTo[w.letterEdge[i].dest];
      }
    }
  }
  w.epsilonEdges = std::vector<Edge>();
  for(size_t i = 0; i < v.epsilonEdges.size(); ++i) {
    Edge e = v.epsilonEdges[i];
    if(mapsTo[e.dest] == -1) continue;
    e.dest = mapsTo[e.dest];
    w.epsilonEdges.push_back(e);
  }
  return(w);

}

Automaton::Automaton() throw () {
  startState = 0;
  acceptState = 0;
  nodes = std::vector<Node>(1);
  assert(checkRep());
}

Automaton::Automaton(const char* regex) throw (SpecException) {
  *this = automatonFromRegex(regex);
}

Automaton::Automaton(const std::string &regex) throw (SpecException) {
  *this = automatonFromRegex(regex);
}

const Automaton::OpMap Automaton::operators =
  makeOperatorMap();

Automaton::OpMap Automaton::makeOperatorMap() {
  OpMap op_map;
  // Concatenation has precedence 0.
  op_map['*'] = Operator( 1, &Automaton::kleeneStar);
  op_map['+'] = Operator( 1, &Automaton::atLeastOnce);
  op_map['?'] = Operator( 1, &Automaton::atMostOnce);
  op_map['|'] = Operator(-1, &Automaton::alternation);
  op_map['#'] = Operator(-2, &Automaton::cartesianProduct);
  op_map['&'] = Operator(-2, &Automaton::tensorProduct);
  return(op_map);
}

Automaton Automaton::automatonFromRegex(const char* regex) throw (SpecException) {
  using std::make_pair;
  using std::pair;
  using std::vector;
  typedef vector<Automaton> OperandStack;
  typedef vector<Operator> OperatorStack;
  vector<pair<OperandStack, OperatorStack> > parse_stack;

  OperandStack  operand_stack;
  OperatorStack operator_stack;
  operand_stack.push_back(Automaton());
  while(*regex) {
    char c = *regex;

    Operator op;
    Automaton v;
    OpMap::const_iterator val_ittr = operators.find(c);
    if(c == '(') {
      parse_stack.push_back(make_pair<OperandStack, OperatorStack>(operand_stack, operator_stack));
      operand_stack = OperandStack();
      operator_stack = OperatorStack();
      operand_stack.push_back(Automaton());
      ++regex;
      continue;
    } else if(c == ')') {
      if(parse_stack.empty()) {
	throw SpecException("Unbalanced parentheses: unexpected \')\'");
      }
      while(!operator_stack.empty()) {
	assert(operand_stack.size() >= 2);
	Operator bop = operator_stack.back();
	operator_stack.pop_back();
	Automaton o2 = operand_stack.back();
	operand_stack.pop_back();
	Automaton o1 = operand_stack.back();
	operand_stack.pop_back();
	operand_stack.push_back((o1.*(bop.op))(o2));
      }
      assert(operand_stack.size() == 1);
      op = Operator(0, &Automaton::concat);
      v = operand_stack.back();
      operand_stack  = parse_stack.back().first;
      operator_stack = parse_stack.back().second;
      parse_stack.pop_back();
    } else if(val_ittr != operators.end()) {
      op = val_ittr->second;
      v = Automaton();
    } else {
      // Default operation of concatenation has precedence 0.
      op = Operator(0, &Automaton::concat);
      v = Automaton(c);
    }

    while(!operator_stack.empty() &&
	  operator_stack.back().prec >=
	  op.prec) {
      assert(operand_stack.size() >= 2);
      Operator bop = operator_stack.back();
      operator_stack.pop_back();
      Automaton o2 = operand_stack.back();
      operand_stack.pop_back();
      Automaton o1 = operand_stack.back();
      operand_stack.pop_back();
      operand_stack.push_back((o1.*(bop.op))(o2));
    }

    operator_stack.push_back(op);
    operand_stack.push_back(v);
    ++regex;
  }

  if(!parse_stack.empty()) {
    throw SpecException("Unbalanced parentheses: missing \')\'");
  }

  while(!operator_stack.empty()) {
    assert(operand_stack.size() >= 2);
    Operator bop = operator_stack.back();
    operator_stack.pop_back();
    Automaton o2 = operand_stack.back();
    operand_stack.pop_back();
    Automaton o1 = operand_stack.back();
    operand_stack.pop_back();
    operand_stack.push_back((o1.*(bop.op))(o2));
  }

  assert(operand_stack.size() == 1);
  return(operand_stack.back());
}

Automaton Automaton::automatonFromRegex(const std::string &regex) throw (SpecException) {
  return(automatonFromRegex(regex.c_str()));
}

Automaton::Automaton(char c) throw (SpecException) {
  if('a' <= c && c <= 'z') {
    c += 'A' - 'a';
  }
  if('A' <= c && c <= 'Z') {
    startState = 0;
    acceptState = 1;
    nodes = std::vector<Node>(2);
    nodes[0].fingerprint = 1 << (c - 'A');
    nodes[0].letterEdge[c - 'A'] = Edge(acceptState);
  } else if(c == '.') {
    startState = 0;
    acceptState = 1;
    nodes = std::vector<Node>(2);
    for(int i = 0; i < 26; ++i) {
      nodes[0].fingerprint |= 1 << i;
      nodes[0].letterEdge[i] = Edge(acceptState);
    }
  } else {
    std::ostringstream s;
    s << "Invalid specification character \'";
    s << c;
    s << "\'.";
    throw SpecException(s.str());
  }
  assert(checkRep());
}

bool Automaton::checkRep() const {
  if(nodes.size() < 1) return(false);
  if(startState  < 0 || startState  >= nodes.size()) return(false);
  if(acceptState < 0 || acceptState >= nodes.size()) return(false);
  for(size_t i = 0; i < nodes.size(); ++i) {
    const Node &v = nodes[i];
    for(uint_fast8_t j = 0; j < 26; ++j) {
      if(v.fingerprint & (1<<j)) {
	if(!checkEdge(v.letterEdge[j]))
	  return(false);
      }
    }
    for(size_t j = 0; j < v.epsilonEdges.size(); ++j) {
      if(!checkEdge(v.epsilonEdges[j]))
	return(false);
    }
  }
  return(true);
}

Automaton Automaton::simplify() const {
  Automaton bob = *this;

  size_t n;
  do {
    n = bob.nodes.size();
    bob = bob.simplifyLoneEpsilonEdges();
    bob = bob.simplifyDeadEnds();
  } while(bob.nodes.size() < n);

  return(bob);
}

Automaton Automaton::simplifyLoneEpsilonEdges() const {
  assert(checkRep());

  const size_t n = nodes.size();
  std::vector<bool> marked(n,false);
  std::vector<size_t> drainsTo(n);
  std::vector<size_t> stack;

  // Remove nodes which have only a single outgoing epsilon edge.
  for(size_t i = 0; i < n; ++i) {
    if(marked[i]) continue;
    size_t p = i;
    stack.push_back(p);
    while(!marked[p]) {
      const Node &v = nodes[p];
      marked[p] = true;
      drainsTo[p] = p;
      if(v.fingerprint ||
	 v.epsilonEdges.size() != 1 ||
	 p == acceptState) {
	break;
      }
      p = v.epsilonEdges[0].dest;
      stack.push_back(p);
    }
    size_t end = drainsTo[p];
    stack.pop_back();
    while(!stack.empty()) {
      p = stack.back();
      stack.pop_back();
      drainsTo[p] = end;
    }
  }

  size_t m = 0;
  std::vector<long> mapsTo(n,-1);
  for(size_t i = 0; i < n; ++i) {
    if(drainsTo[i] != i) continue;
    mapsTo[i] = m++;
  }
  for(size_t i = 0; i < n; ++i) {
    if(drainsTo[i] == i) continue;
    mapsTo[i] = mapsTo[drainsTo[i]];
  }

  Automaton bob;
  bob.startState  = mapsTo[startState];
  bob.acceptState = mapsTo[acceptState];
  bob.nodes = std::vector<Node>(m);
  for(size_t i = 0; i < n; ++i) {
    if(drainsTo[i] != i) continue;
    bob.nodes[mapsTo[i]] = mapNode(mapsTo, nodes[i]);
  }

  assert(bob.checkRep());
  return(bob);
}

Automaton Automaton::simplifyDeadEnds() const {
  const size_t n = nodes.size();
  std::vector<std::vector<size_t> > in(n), out(n);

  for(size_t i = 0; i < n; ++i) {
    for(uint_fast8_t k = 0; k < 26; ++k) {
      if(nodes[i].fingerprint & (1<<k)) {
	size_t j = nodes[i].letterEdge[k].dest;
	out[i].push_back(j);
	in[j].push_back(i);
      }
    }
    for(size_t k = 0; k < nodes[i].epsilonEdges.size(); ++k) {
      size_t j = nodes[i].epsilonEdges[k].dest;
      out[i].push_back(j);
      in[j].push_back(i);
    }
  }

  std::vector<bool> vs(n,false), vt(n,false);
  std::vector<size_t> stack;
  
  vs[startState] = true;
  stack.push_back(startState);
  while(!stack.empty()) {
    size_t p = stack.back();
    stack.pop_back();
    assert(vs[p]);
    for(size_t k = 0; k < out[p].size(); ++k) {
      size_t q = out[p][k];
      if(vs[q]) continue;
      vs[q] = true;
      stack.push_back(q);
    }
  }
  assert(stack.empty());
  
  vt[acceptState] = true;
  stack.push_back(acceptState);
  while(!stack.empty()) {
    size_t p = stack.back();
    stack.pop_back();
    assert(vt[p]);
    for(size_t k = 0; k < in[p].size(); ++k) {
      size_t q = in[p][k];
      if(vt[q]) continue;
      vt[q] = true;
      stack.push_back(q);
    }
  }
  assert(stack.empty());

  if(!vt[startState] || !vs[acceptState]) {
    Automaton bob;
    bob.nodes = std::vector<Node>(2);
    bob.startState = 0;
    bob.acceptState = 1;
    return(bob);
  }

  size_t m = 0;
  std::vector<long> mapsTo(n,-1);
  for(size_t i = 0; i < n; ++i) {
    if(!vs[i] || !vt[i]) continue;
    mapsTo[i] = m++;
  }
  //std::cout << "n = " << n << ", m = " << m << std::endl;

  assert(mapsTo[startState]  != -1);
  assert(mapsTo[acceptState] != -1);

  Automaton bob;
  bob.startState  = mapsTo[startState];
  bob.acceptState = mapsTo[acceptState];
  bob.nodes = std::vector<Node>(m);
  for(size_t i = 0; i < n; ++i) {
    if(mapsTo[i] == -1) continue;
    bob.nodes[mapsTo[i]] = mapNode(mapsTo, nodes[i]);
  }

  assert(bob.checkRep());
  return(bob);
}

bool Automaton::accepts(const char* s) const {
  std::vector<bool> dp(nodes.size(), false);
  std::vector<size_t> stack;

  dp[startState] = true;
  stack.push_back(startState);
  while(!stack.empty()) {
    const Node &v = nodes[stack.back()];
    stack.pop_back();
    for(size_t i = 0; i < v.epsilonEdges.size(); ++i) {
      size_t j = v.epsilonEdges[i].dest;
      if(dp[j]) continue;
      dp[j] = true;
      stack.push_back(j);
    }
  }

  while(*s) {

    // follow letter edges
    {
      std::vector<bool> dpp(nodes.size(), false);
      for(size_t i = 0; i < nodes.size(); ++i) {
	if(!dp[i]) continue;
	const Node &v = nodes[i];
	int k;
	if('a' <= *s && *s <= 'z') {
	  k = *s - 'a';
	} else if('A' <= *s && *s <= 'Z') {
	  k = *s - 'A';
	} else {
	  return(false);
	}
	if(!(v.fingerprint & (1<<k))) continue;
	dpp[v.letterEdge[k].dest] = true;
      }
      dp = dpp;
    }

    // follow epsilon edges
    for(size_t i = 0; i < nodes.size(); ++i) {
      if(!dp[i]) continue;
      stack.push_back(i);
      while(!stack.empty()) {
	const Node &v = nodes[stack.back()];
	stack.pop_back();
	for(size_t i = 0; i < v.epsilonEdges.size(); ++i) {
	  size_t j = v.epsilonEdges[i].dest;
	  if(dp[j]) continue;
	  dp[j] = true;
	  stack.push_back(j);
	}
      }
    }

    ++s;
  }

  return(dp[acceptState]);
}

bool Automaton::accepts(const std::string &s) const {
  return(accepts(s.c_str()));
}

Automaton Automaton::concat(const Automaton &that) const {
  Automaton result = *this;
  size_t offset = nodes.size();
  for(size_t i = 0; i < that.nodes.size(); ++i) {
    result.nodes.push_back(translateNode(offset, that.nodes[i]));
  }
  result.nodes[acceptState].epsilonEdges.push_back(Edge(offset + that.startState));
  result.acceptState = offset + that.acceptState;

  assert(result.checkRep());
  return(result.simplify());
}

Automaton Automaton::operator >>(const Automaton &that) const {
  return(concat(that));
}

Automaton Automaton::alternation(const Automaton &that) const {
  std::vector<Automaton> bob;
  bob.push_back(*this);
  bob.push_back(that);
  return(alternation(bob));
}

Automaton Automaton::operator |(const Automaton &that) const {
  return(alternation(that));
}

Automaton Automaton::alternation(const std::vector<Automaton> &options) {
  Automaton bob;
  bob.nodes = std::vector<Node>(2);
  bob.startState  = 0;
  bob.acceptState = 1;
  size_t n = 2;

  for(size_t i = 0; i < options.size(); ++i) {
    for(size_t j = 0; j < options[i].nodes.size(); ++j) {
      bob.nodes.push_back(translateNode(n, options[i].nodes[j]));
    }
    bob.nodes[bob.startState].epsilonEdges.push_back(n + options[i].startState);
    bob.nodes[n + options[i].acceptState].epsilonEdges.push_back(bob.acceptState);
    n += options[i].nodes.size();
  }

  assert(bob.checkRep());
  return(bob.simplify());
}

Automaton Automaton::cartesianProduct(const Automaton &that) const {
  /*
    Here's idea behind the layout of the resulting graph. Each pair
    (u,v) maps to three vertices: one input and two output. The input
    vertex has an epsilon edge leading to each of the two
    corresponding output vertices. One of the output vertices has
    transitions corresponding to those in the first input graph and
    the other output vertex has such for the second graph. This is to
    work around the issue of each node having at most one transition
    per letter.
   */
  size_t n = nodes.size();
  size_t m = that.nodes.size();
  Automaton bob;
  bob.nodes = std::vector<Node>(3*n*m);
  bob.startState  = 3*(startState  * m + that.startState);
  bob.acceptState = 3*(acceptState * m + that.acceptState);
  for(size_t i = 0; i < n; ++i) {
    for(size_t j = 0; j < m; ++j) {
      size_t p = 3*(i*m+j);
      bob.nodes[p].epsilonEdges.push_back(p+1);
      bob.nodes[p].epsilonEdges.push_back(p+2);
      bob.nodes[p+1] = transformNode(nodes[i], 3*m, 3*j);
      bob.nodes[p+2] = transformNode(that.nodes[j], 3, 3*i*m);
    }
  }

  assert(bob.checkRep());
  return(bob.simplify());
}

Automaton Automaton::tensorProduct(const Automaton &that) const {
  size_t n = nodes.size();
  size_t m = that.nodes.size();
  Automaton bob;
  bob.nodes = std::vector<Node>(n*m);
  bob.startState  = startState  * m + that.startState;
  bob.acceptState = acceptState * m + that.acceptState;
  for(size_t i = 0; i < n; ++i) {
    for(size_t j = 0; j < m; ++j) {
      size_t p = i*m+j;
      bob.nodes[p].fingerprint = nodes[i].fingerprint & that.nodes[j].fingerprint;
      for(uint_fast8_t k = 0; k < 26; ++k) {
	bob.nodes[p].letterEdge[k] = Edge(nodes[i].letterEdge[k].dest * m + that.nodes[j].letterEdge[k].dest);
      }
      for(size_t k = 0; k < nodes[i].epsilonEdges.size(); ++k) {
	Edge e = nodes[i].epsilonEdges[k];
	e.dest = e.dest * m + j;
	bob.nodes[p].epsilonEdges.push_back(e);
      }
      for(size_t k = 0; k < that.nodes[j].epsilonEdges.size(); ++k) {
	Edge e = that.nodes[j].epsilonEdges[k];
	e.dest = i * m + e.dest;
	bob.nodes[p].epsilonEdges.push_back(e);
      }
    }
  }

  assert(bob.checkRep());
  return(bob.simplify());
}

Automaton Automaton::kleeneStar() const {
  Automaton bob = *this;
  size_t n = bob.nodes.size();
  bob.nodes.push_back(Node());
  bob.nodes[n].epsilonEdges.push_back(Edge(bob.startState));
  bob.nodes[bob.acceptState].epsilonEdges.push_back(Edge(n));
  bob.startState = n;
  bob.acceptState = n;
  assert(bob.checkRep());
  return(bob.simplify());
}

Automaton Automaton::kleeneStar(const Automaton &that) const {
  return(kleeneStar().concat(that));
}

Automaton Automaton::operator *() const {
  return(kleeneStar());
}

Automaton Automaton::atLeastOnce() const {
  return(this->concat(kleeneStar()));
}

Automaton Automaton::atLeastOnce(const Automaton &that) const {
  return(atLeastOnce().concat(that));
}

Automaton Automaton::operator +() const {
  return(atLeastOnce());
}

Automaton Automaton::atMostOnce() const {
  return(alternation(Automaton()));
}

Automaton Automaton::atMostOnce(const Automaton &that) const {
  return(atMostOnce().concat(that));
}

std::string Automaton::dotGraph() const {

  std::ostringstream s;

  s << "digraph {" << std::endl;
  s << "\t" << "graph [rankdir=LR];" << std::endl;

  // Add nodes
  for(size_t i = 0; i < nodes.size(); ++i) {
    s << "\t" << i << " [shape=point";
    if(i == startState &&
       i == acceptState) {
      s << ",color=\"purple\"";
    } else if(i == startState) {
      s << ",color=\"red\"";
    } else if(i == acceptState) {
      s << ",color=\"blue\"";
    }
    s << "];" << std::endl;
  }

  // Add edges
  for(size_t i = 0; i < nodes.size(); ++i) {
    Node v = nodes[i];
    std::vector<bool> r(26,false);
    for(uint_fast8_t j = 0; j < 26; ++j) {
      if(!(v.fingerprint & (1 << j))) continue;
      if(r[j]) continue;
      size_t dest = v.letterEdge[j].dest;
      std::string label;
      { // Aggregate edge label
	label.push_back((char)('A'+j));
	for(uint_fast8_t k = j+1; k < 26; ++k) {
	  if(!(v.fingerprint & (1 << k))) continue;
	  if(v.letterEdge[k].dest != dest) continue;
	  if(r[k]) continue;
	  r[k] = true;
	  label.push_back((char)('A'+k));
	}
      }
      { // Compress edge label
	std::string label2;
	size_t p = 0;
	for(size_t i = 1; i <= label.length(); ++i) {
	  if(i < label.length() && label[i] == label[p] + i - p) continue;
	  if(i-1-p < 4) {
	    for(size_t j = p; j < i; ++j) {
	      label2.push_back(label[j]);
	    }
	  } else {
	    label2.push_back(label[p]);
	    label2.push_back('-');
	    label2.push_back(label[i-1]);
	  }
	  p = i;
	}
	if(label2.length() > 1) {
	  label2 = "[" + label2 + "]";
	}
	label = label2;
      }
      s << "\t" << i << " -> " << dest;
      s << " [" << "label=\"" << label << "\"";
      s << "];" << std::endl;
    }
    for(size_t j = 0; j < v.epsilonEdges.size(); ++j) {
      Edge e = v.epsilonEdges[j];
      std::string label = "&#949;"; // \949 is Unicode epsilon
      s << "\t" << i << " -> " << e.dest;
      s << " [" << "label=\"" << label << "\"";
      s << "];" << std::endl;
    }
  }

  s << "}" << std::endl;

  return(s.str());
}
