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

#ifndef __LOGNUM_DOT_H_INCLUDED__
#define __LOGNUM_DOT_H_INCLUDED__

#include <limits>
#include <math.h>


/**
   A class representing positive numbers on a logarithmic scale.
 */
class Lognum {
public:

  double logval;

public:

  inline explicit Lognum(double logval_in=0) :
    logval(logval_in) {;}

  inline Lognum& operator *=(Lognum that) {
    logval += that.logval;
    return(*this);
  }

  inline Lognum& operator *=(double v) {
    logval += log(v);
    return(*this);
  }

  inline Lognum& operator /=(Lognum that) {
    logval -= that.logval;
    return(*this);
  }

  static const Lognum ZERO;
};

Lognum operator +(Lognum a, Lognum b);

inline Lognum& operator +=(Lognum &a, Lognum b) {
  return(a = a + b);
}

inline Lognum operator *(Lognum a, Lognum b) {
  return Lognum(a.logval + b.logval);
}

inline Lognum operator *(Lognum a, double v) {
  return Lognum(a.logval + log(v));
}

inline Lognum operator *(double v, Lognum a) {
  return Lognum(a.logval + log(v));
}

inline Lognum operator /(Lognum a, Lognum b) {
  return Lognum(a.logval - b.logval);
}

inline bool operator ==(Lognum a, Lognum b) {
  return(a.logval == b.logval);
}

inline bool operator !=(Lognum a, Lognum b) {
  return(a.logval != b.logval);
}

inline bool operator <(Lognum a, Lognum b) {
  return(a.logval < b.logval);
}

inline bool operator <=(Lognum a, Lognum b) {
  return(a.logval <= b.logval);
}

inline bool operator >(Lognum a, Lognum b) {
  return(a.logval > b.logval);
}

inline bool operator >=(Lognum a, Lognum b) {
  return(a.logval >= b.logval);
}


#endif /*__LOGNUM_DOT_H_INCLUDED__*/
