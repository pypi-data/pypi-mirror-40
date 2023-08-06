# Proteinko

[README на српском](https://github.com/stefs304/proteinko/blob/master/README_srb.md)

Proteinko is package that enables you to represent a protein sequence (that is
 its physicochemical properties) as spatial signals.

Protein is a sequence of amino acid residues, each of which has characteristic physical and chemical properties.
Local properties of a protein are reflection of local cumulative effect of amino acid residues that make up said protein.
By modeling physico-chemical properties for each amino acid residue as a normal distribution spanning the neighbouring amino acid 
residues, we obtain a continuous signal which represents a spatial distribution of specific physicochemical property of a protein.

This way we can represent a protein sequence as a distribution of following properties:
* hydropathy
* donor atoms
* acceptor atoms
* isoelectric point
* molecular volume

Proteinko also allows for usage of custom amino acid residue scales.

Manuscript ready for publishing.

### Example
![signals](https://raw.githubusercontent.com/stefs304/proteinko/master/example.png)

### Installation
```buildoutcfg
pip install proteinko
```

### Usage

```
from proteinko import ProteinSignal

sequence = <your_protein_sequence>
protein = ProteinSignal()
signal = protein.get_signal(sequence, 'hydropathy')

## ...Now play with the signal however you like
```

### Contact and portfolio

* My [Linkedin](https://rs.linkedin.com/in/stefan-stojanovic-304) profile.
* [MHCLovac](https://github.com/stefs304/mhclovac) - in this repository protein signals are usded to predict MHC binding.
