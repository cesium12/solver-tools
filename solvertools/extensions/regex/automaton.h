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

#ifndef __AUTOMATON_DOT_H_INCLUDED__
#define __AUTOMATON_DOT_H_INCLUDED__

#include <map>
#include <stdexcept>
#include <stdint.h>
#include <string>
#include <vector>
#include "lognum.h"


/**
   A class representing an immutable finite state machine.

   The automaton works with the language A-Z and SPACE, where SPACE
   represents a word break. The automaton is nondeterministic in that
   each node may have any number of \a epsilon edges, which consume no
   input. Each non-epsilon edge leaving a node must consume a distinct
   character A-Z or SPACE.

   @invariant <tt>nodes.size() >= 1</tt>
   @invariant <tt>0 <= startState < nodes.size()</tt>
   @invariant <tt>0 <= acceptState < nodes.size()</tt>
   @invariant All internal edges have valid targets.
 */
class Automaton {
private:

  /**
     A weighted directed edge in the automaton.
   */
  struct Edge {
  public:
    uint_fast32_t dest;
    Lognum cost;

    Edge(uint_fast32_t dest_in=-1, Lognum cost_in=Lognum(0)) :
      dest(dest_in), cost(cost_in) {;}
  };

  /**
     Checks whether the representation invariant holds for this edge.
   */
  bool checkEdge(const Edge &e) const;

public:

  /**
     A vertex with its outgoing edges.
   */
  struct Node {
    friend class Automaton;
  private:
    uint32_t fingerprint;
    Edge letterEdge[26];
    std::vector<Edge> epsilonEdges;
  public:
    Node();
    inline uint32_t getFingerprint() const {
      return fingerprint;
    }
    inline uint_fast32_t getLetterDest(uint_fast32_t i) const {
      return letterEdge[i].dest;
    }
    inline Lognum getLetterCost(uint_fast32_t i) const {
      return letterEdge[i].cost;
    }
    inline uint_fast32_t getNumEpsilonEdges() const {
      return epsilonEdges.size();
    }
    inline uint_fast32_t getEpsilonDest(uint_fast32_t i) const {
      return epsilonEdges[i].dest;
    }
    inline Lognum getEpsilonCost(uint_fast32_t i) const {
      return epsilonEdges[i].cost;
    }
  };

  /**
     An exception thrown when creating an Automaton with an invalid
     specification character or string.
   */
  class SpecException : public std::domain_error {
  public:
    SpecException(const std::string &s) : std::domain_error(s) {
      ;
    }
  };

private:

  uint_fast32_t startState;
  uint_fast32_t acceptState;
  std::vector<Node> nodes;

  /**
     Creates an Automaton which does nothing but offset the weight.
   */
  explicit Automaton(Lognum c);

  /**
     Returns a copy of a node \c v with each pointer \f$i\f$ mapped to
     \f$ai+b\f$.
   */
  static Node transformNode(const Node &v, size_t a, size_t b);

  /**
     Returns a copy of a node \c v with the pointers translated by \c
     offset.
   */
  static Node translateNode(size_t offset, const Node &v);

  /**
     Maps the pointers in node \c v using the map \c mapsTo and
     returns them as a new Node.
  */
  static Node mapNode(const std::vector<long> &mapsTo, const Node &v);

  /**
     Checks the representation invariant.
   */
  bool checkRep() const;

  /**
     Constructs a hopefully simpler Automaton representing the same
     language.
  */
  Automaton simplify() const;
  Automaton simplifyLoneEpsilonEdges() const;
  Automaton simplifyDeadEnds() const;

  /*
    Here's a complicated bunch of stuff to handle extensible
    operations in Automaton specification strings.
   */

  /**
     A binary operator on automata.
   */
  struct Operator {
    int prec; ///< Operator precedence
    Automaton (Automaton::*op)(const Automaton&) const;
    Operator() :
      prec(0), op(&Automaton::concat) {;}
    Operator(int prec_in, Automaton (Automaton::*op_in)(const Automaton&) const) :
      prec(prec_in), op(op_in) {;}
  };
  typedef std::map<char, Operator> OpMap;
  static const OpMap operators;   ///< The operators used in automata specification strings.
  static OpMap makeOperatorMap(); ///< Constructs the operator map at initialization time.

public:

  /**
     Creates an Automaton matching the empty string.
   */
  Automaton() throw ();

  /**
     Creates an Automaton matching a single character.
     
     If the character is 'A'-'Z' or 'a'-'z', only matches that
     specific letter (case insensitive).  If the character is '.',
     matches any single letter.

     @throws \c SpecException if \c c is not 'A'-'Z', 'a'-'z', or '.'.
   */
  Automaton(char c) throw (SpecException);

  /**
     Creates an Automaton from a POSIX-style regular expression.

     Letters and spaces match as specified in <tt>Automaton(char
     c)</tt>.

     @throws \c SpecException if \c regex does not represent a valid
     POSIX regular expression, with the extensions and restrictions
     specified above.
   */
  Automaton(const char* regex) throw (SpecException);
  Automaton(const std::string &regex) throw (SpecException);
  static Automaton automatonFromRegex(const char* regex) throw (SpecException);
  static Automaton automatonFromRegex(const std::string &regex) throw (SpecException);

  inline size_t getNumNodes() const {
    return nodes.size();
  }

  inline const Node &getNode(uint_fast32_t i) const {
    return nodes[i];
  }

  inline uint_fast32_t getStartState() const {
    return startState;
  }

  inline uint_fast32_t getAcceptState() const {
    return acceptState;
  }

  /**
     Returns true if the string \c s is accepted by the unweighted
     version of the automaton. String \c s should consist of spaces
     and letters (case insensitive).
   */
  bool accepts(const char* s) const;
  bool accepts(const std::string &s) const;

  /**
     Returns an Automaton matching the concatenation \f$A \circ B\f$
     of languages \f$A\f$ and \f$B\f$.
   */
  Automaton concat(const Automaton &that) const;
  Automaton operator >>(const Automaton &that) const;

  /**
     Returns an Automaton matching the union \f$A \cup B\f$ of
     languages \f$A\f$ and \f$B\f$.
   */
  Automaton alternation(const Automaton &that) const;
  Automaton operator |(const Automaton &that) const;
  static Automaton alternation(const std::vector<Automaton> &options);

  /**
     Returns an Automaton corresponding to the Cartesian graph product
     of two Automatons. That is, the states of \f$A
     \operatorname{\square} B\f$ are the exactly the Cartesian set
     product of the states of \f$A\f$ and \f$B\f$ and there is a
     transition between two vertices \f$(u,u')\f$ and \f$(v,v')\f$ if
     and only if \f$u=v\f$ and there is a transition from \f$u'\f$ to
     \f$v'\f$ in \f$B\f$ or \f$u'=v'\f$ and there is a transition from
     \f$u\f$ to \f$v\f$ in \f$A\f$. The start and accept states are
     \f$(s,s')\f$ and \f$(t,t')\f$ where \f$s\f$ and \f$s'\f$ and
     \f$t\f$ and \f$t'\f$ are the start and accept states of \f$A\f$
     and \f$B\f$, respectively.
   */
  Automaton cartesianProduct(const Automaton &that) const;

  /**
     Returns an Automaton corresponding to the tensor graph product of
     two Automatons. That is, the states of \f$A\times B\f$ are the
     exactly the Cartesian set product of the states of \f$A\f$ and
     \f$B\f$ and there is a transition between two vertices
     \f$(u,u')\f$ and \f$(v,v')\f$ if and only if there is a
     transition from \f$u\f$ to \f$v\f$ in \f$A\f$ and also a
     transition from \f$u'\f$ to \f$v'\f$ in \f$B\f$. The weight of a
     transition is the product of the weights of the two transitions
     in \f$A\f$ and \f$B\f$. The start and accept states are
     \f$(s,s')\f$ and \f$(t,t')\f$ where \f$s\f$ and \f$s'\f$ and
     \f$t\f$ and \f$t'\f$ are the start and accept states of \f$A\f$
     and \f$B\f$, respectively.
   */
  Automaton tensorProduct(const Automaton &that) const;

  /**
     Returns an Automaton matching the Kleene star \f$L^*\f$ of a
     language \f$L\f$.
   */
  Automaton kleeneStar() const;
  Automaton kleeneStar(const Automaton &that) const;
  Automaton operator *() const;

  /**
     Returns an Automaton matching 1 or more repetitions of the
     operand Automaton.
   */
  Automaton atLeastOnce() const;
  Automaton atLeastOnce(const Automaton &that) const;
  Automaton operator +() const;

  /**
     Returns an Automaton matching either 0 or 1 repetitions of the
     operand Automaton.
   */
  Automaton atMostOnce() const;
  Automaton atMostOnce(const Automaton &that) const;

  /**
     Returns a specification in the \a dot directed graph language for
     a visualization of the Automaton.
   */
  std::string dotGraph() const;

};


#endif /*__AUTOMATON_DOT_H_INCLUDED__*/
