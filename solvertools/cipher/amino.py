import re

'''
Utilities for working with nucleotide and amino acid sequences.
'''

def amino_encode(s):
    '''
    Convenience function for converting a DNA string into an amino
    acid sequence.
    '''
    return str(NucleotideSequence(s).to_amino())

def base_pair(ch):
    '''
    Given a DNA base, returns the complementary base.
    '''
    if(ch=='A'):
        return 'T'
    if(ch=='C'):
        return 'G'
    if(ch=='G'):
        return 'C'
    if(ch=='T'):
        return 'A'

def _groups_of_three(x):
    return (x[i:i+3] for i in xrange(0,len(x)-2,3))

class NucleotideSequence(object):
    '''
    Represents a sequence of DNA or RNA nucleotides.
    '''

    def __init__(self, seq):
        '''
        Creates a new nucleotide sequence.  seq may be either a string
        (both T's and U's are allowed) or another nucleotide sequence.
        '''
        if isinstance(seq, basestring):
            self.nucleotides = seq.upper().replace('U','T')
        elif isinstance(seq, NucleotideSequence):
            self.nucleotides = seq.nucleotides
        else:
            raise TypeError

    def conjugate(self):
        '''
        Returns the conjugate of this sequence.
        '''
        return type(self)(''.join(map(base_pair,reversed(self.nucleotides))))

    def as_rna(self):
        '''
        Returns a copy of this nucleotide sequence as an RNA sequence.
        (If this sequence is DNA, then all T's are converted to U's.)
        '''
        return RNASequence(self)

    def as_dna(self):
        '''
        Returns a copy of this nucleotide sequence as a DNA sequence.
        '''
        return DNASequence(self)

    def to_amino(self,start_behavior='keep'):
        """
        Convert this sequence to an amino acid sequence.

        Start behaviors:
        'keep' - Codes from the beginning to the string to the end of the string.
        'chop' - Codes from the beginning of the string to the end of the string.  Will discard a single leading Met and arbitrarily many trailing stop codons.
        'search' - Starts coding when it finds a start codon.  Stops if it encounters a stop codon.
        """
        if start_behavior!='keep' and start_behavior!='chop' and start_behavior!='search':
            raise ValueError('Unrecognized start behavior.  Allowed behaviors are keep, chop, search.')
        code = self.nucleotides
        if(start_behavior=='search'):
            offset = code.find('ATG')
            if offset!=-1:
                code = code[offset+3:]
            else:
                code = ''
        sequence = ''.join(map(genetic_code.__getitem__,_groups_of_three(code)))
        if(start_behavior=='search'):
            sequence = re.sub('#.*','',sequence)
        elif(start_behavior=='chop'):
            sequence = re.sub('^M','',sequence)
            sequence = re.sub('#*$','',sequence)
        return AminoSequence(sequence)

    def __getitem__(self, index):
        '''Returns a slice of this nucleotide sequence.'''
        if isinstance(index, slice):
            return type(self)(self.nucleotides[index])
        else:
            raise TypeError('Only slicing is supported.  Use str() if you need individual characters.')

class DNASequence(NucleotideSequence):
    '''
    A DNA sequence.

        >>> n = DNASequence('GATATCGCA')
        >>> n
        < DNA sequence GATATCGCA >
        >>> n.as_rna()
        < RNA sequence GAUAUCGCA >
        >>> n.conjugate()
        < DNA sequence TGCGATATC >
        >>> n[2:8]
        < DNA sequence TATCGC >
        >>> n.to_amino()
        < Amino acid sequence DIA >
        >>> n.to_amino().long_form()
        'ASPILEALA'
    '''

    def __repr__(self):
        return '< DNA sequence %s >' % str(self) 

    def __str__(self):
        return self.nucleotides

class RNASequence(NucleotideSequence):
    '''
    An RNA sequence.  See the documentation for ``DNASequence``.
    '''

    def __repr__(self):
        return '< RNA sequence %s >' % str(self)

    def __str__(self):
        return self.nucleotides.replace('T','U')

class AminoSequence(object):
    '''
    Represents a sequence of amino acids.

        >> a = AminoSequence('ASDF')
        >> a
        < Amino acid sequence ASDF >
        >> a.long_form()
        'ALASERASPPHE'
        >> AminoSequence.from_three('ALASERASPPHE')
        < Amino acid sequence ASDF >
    '''

    amino_acids = (
        # normal amino acids
        ('A' , 'ALA'),
        ('C' , 'CYS'),
        ('D' , 'ASP'),
        ('E' , 'GLU'),
        ('F' , 'PHE'),
        ('G' , 'GLY'),
        ('H' , 'HIS'),
        ('I' , 'ILE'),
        ('K' , 'LYS'),
        ('L' , 'LEU'),
        ('M' , 'MET'),
        ('N' , 'ASN'),
        ('P' , 'PRO'),
        ('Q' , 'GLN'),
        ('R' , 'ARG'),
        ('S' , 'SER'),
        ('T' , 'THR'),
        ('V' , 'VAL'),
        ('W' , 'TRP'),
        ('Y' , 'TYR'),
        # special amino acids
        ('U' , 'SEC'),
        ('O' , 'PYL'),
        # wildcards
        ('B' , 'ASX'),
        ('Z' , 'GLX'),
        ('J' , 'XLE'),
        ('X' , 'XAA'),
        # stop codon
        ('#' , '###')
    )

    one_to_three = dict(amino_acids)
    three_to_one = dict(map(reversed,amino_acids))

    def __init__(self, seq):
        '''
        Constructs a new amino acid sequence.  seq can be either another amino
        acid sequence, or a string of one-letter amino acid abbreviations.
        '''
        if isinstance(seq, basestring):
            self.acids = seq.upper()
        elif isinstance(seq, AminoSequence):
            self.acids = seq.acids
        else:
            raise TypeError

    def long_form(self):
        '''
        Returns the three letter abbreviations for the sequence of amino acids.
        '''
        return ''.join(map(self.one_to_three.__getitem__,self.acids))

    def __str__(self):
        '''
        Returns the one letter abbreviations for the sequence of amino acids.
        '''
        return self.acids

    def __repr__(self):
        return '< Amino acid sequence %s >' % str(self)

    @staticmethod
    def from_three(seq):
        '''
        Converts a string of three-letter amino acid abbreviations into an AminoAcidSequence.
        '''
        seq = seq.upper()
        short_seq = ''.join(map(AminoSequence.three_to_one.__getitem__,_groups_of_three(seq)))
        return AminoSequence(short_seq)

genetic_code_tmp = (
    ('UUU' , 'PHE'),
    ('UUC' , 'PHE'),
    ('UUA' , 'LEU'),
    ('UUG' , 'LEU'),
    ('UCU' , 'SER'),
    ('UCC' , 'SER'),
    ('UCA' , 'SER'),
    ('UCG' , 'SER'),
    ('UAU' , 'TYR'),
    ('UAC' , 'TYR'),
    ('UAA' , '###'),
    ('UAG' , '###'),
    ('UGU' , 'CYS'),
    ('UGC' , 'CYS'),
    ('UGA' , '###'),
    ('UGG' , 'TRP'),
    ('CUU' , 'LEU'),
    ('CUC' , 'LEU'),
    ('CUA' , 'LEU'),
    ('CUG' , 'LEU'),
    ('CCU' , 'PRO'),
    ('CCC' , 'PRO'),
    ('CCA' , 'PRO'),
    ('CCG' , 'PRO'),
    ('CAU' , 'HIS'),
    ('CAC' , 'HIS'),
    ('CAA' , 'GLN'),
    ('CAG' , 'GLN'),
    ('CGU' , 'ARG'),
    ('CGC' , 'ARG'),
    ('CGA' , 'ARG'),
    ('CGG' , 'ARG'),
    ('AUU' , 'ILE'),
    ('AUC' , 'ILE'),
    ('AUA' , 'ILE'),
    ('AUG' , 'MET'),
    ('ACU' , 'THR'),
    ('ACC' , 'THR'),
    ('ACA' , 'THR'),
    ('ACG' , 'THR'),
    ('AAU' , 'ASN'),
    ('AAC' , 'ASN'),
    ('AAA' , 'LYS'),
    ('AAG' , 'LYS'),
    ('AGU' , 'SER'),
    ('AGC' , 'SER'),
    ('AGA' , 'ARG'),
    ('AGG' , 'ARG'),
    ('GUU' , 'VAL'),
    ('GUC' , 'VAL'),
    ('GUA' , 'VAL'),
    ('GUG' , 'VAL'),
    ('GCU' , 'ALA'),
    ('GCC' , 'ALA'),
    ('GCA' , 'ALA'),
    ('GCG' , 'ALA'),
    ('GAU' , 'ASP'),
    ('GAC' , 'ASP'),
    ('GAA' , 'GLY'),
    ('GAG' , 'GLY'),
    ('GGU' , 'GLY'),
    ('GGC' , 'GLY'),
    ('GGA' , 'GLY'),
    ('GGG' , 'GLY'),
)

genetic_code = dict(map(lambda x : (x[0].replace('U','T'),AminoSequence.three_to_one[x[1]]), genetic_code_tmp))

del genetic_code_tmp
