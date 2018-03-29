# KPHMMER : Hidden Markov Model generator for detecting KEGG pathway specific genes
Generate an HMM file of Pfam-domain that is specifically found by inputting multiple species and pathways registered in KEGG

## what purpose?
- To divide the pathway into two categories such as primary metabolism and secondary metabolism, and to search for frequent Pfam domains in either category.
- To obtain amino acids of genes contained in a specific pathway of a certain species.
- In order to shorten the calculation time, we created a Pfam-domain set that considers only specific species and related species.

## How to use?
KPHMMER consists of five submethods.

```
$ python KPHMMER.py -h
usage: KPHMMER.py [-h] {query,search,analysis,convert,config} ...

KPHMMER, Hidden Markov Model generator for detecting KEGG pathway specific
genes by suecharo. <suehiro619@gmail.com>

positional arguments:
  {query,search,analysis,convert,config}
                        Each is a subcommand. Please refer to the help of each
                        subcommand.
    query               It receives the KEGG's organism code (ex.hsa) and
                        outputs the motif yaml file.
    search              Receive a string and search KEGG's organism code
                        (ex.hsa).
    analysis            Receive motif yaml file and outputs frequently
                        appearing pfam motif only in the selected category.
    convert             Receive motif yaml file and outputs the gene contained
                        therein as fasta file.
    config              Check the currently set category or change the
                        setting.

optional arguments:
  -h, --help            show this help message and exit
```

### config
Config can adjust the following.
- The category of the pathway.
  - KEGG PATHWAY itself can be confirmed from this page. [KEGG PATHWAY](http://www.genome.jp/kegg/pathway.html#metabolism)
- Treatment of genes overlapping in two categories.
  - Select from 1st or 2nd.
  - Duplicate genes are classified in the selected one.

```
$ python KPHMMER.py config -h
usage: KPHMMER.py config [-h] [-s] [-1 CATEGORY_1ST [CATEGORY_1ST ...]]
                         [-2 CATEGORY_2ND [CATEGORY_2ND ...]] [-d [{1st,2nd}]]

Check the currently set category or change the setting.

optional arguments:
  -h, --help            show this help message and exit
  -s, --set-default     Restore conf to the default value.
  -1 CATEGORY_1ST [CATEGORY_1ST ...], --category-1st CATEGORY_1ST [CATEGORY_1ST ...]
                        Set 1st category. Multiple inputs are accepted.
  -2 CATEGORY_2ND [CATEGORY_2ND ...], --category-2nd CATEGORY_2ND [CATEGORY_2ND ...]
                        Set 2nd category. Multiple inputs are accepted.
  -d [{1st,2nd}], --duplicate [{1st,2nd}]
                        Set which categories to place duplicates.

$ python KPHMMER.py config -1 1.1 1.2 1.3
[2018/02/26 17:02:54] === Config start. ===
[2018/02/26 17:02:54] Set value start.
[2018/02/26 17:02:54] Print config start.
1st category : ['1.1', '1.2', '1.3']
2nd category : ['1.9', '1.10', '1.12']
Insert duplicate : 2nd
[2018/02/26 17:02:54] === Config finish. ===

$ python KPHMMER.py config -2 1.4 1.5 1.6
[2018/02/26 17:03:00] === Config start. ===
[2018/02/26 17:03:00] Set value start.
[2018/02/26 17:03:00] Print config start.
1st category : ['1.1', '1.2', '1.3']
2nd category : ['1.4', '1.5', '1.6']
Insert duplicate : 2nd
[2018/02/26 17:03:00] === Config finish. ===

$ python KPHMMER.py config -d 1st
[2018/02/26 17:03:07] === Config start. ===
[2018/02/26 17:03:07] Set value start.
[2018/02/26 17:03:07] Print config start.
1st category : ['1.1', '1.2', '1.3']
2nd category : ['1.4', '1.5', '1.6']
Insert duplicate : 1st
[2018/02/26 17:03:07] === Config finish. ===

$ python KPHMMER.py config -s
[2018/02/26 17:03:10] === Config start. ===
[2018/02/26 17:03:10] Set default start.
[2018/02/26 17:03:10] Print config start.
1st category : ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.11']
2nd category : ['1.9', '1.10', '1.12']
Insert duplicate : 2nd
[2018/02/26 17:03:10] === Config finish. ===
```
### search
Search is a keyword search, and you can search KEGG's organism code.

```
$ python KPHMMER.py search -h
usage: KPHMMER.py search [-h] [-a] [STRING]

Receive a string and search KEGG's organism code (ex.hsa).

positional arguments:
  STRING          Perform keyword search on the input character string.

optional arguments:
  -h, --help      show this help message and exit
  -a, --show-all  Display all organisms present on KEGG. Be careful as there
                  are many outputs.

$ python KPHMMER.py search streptomyces
[2018/02/26 17:05:49] === Search start. ===
[2018/02/26 17:05:49] Ordinaly search start.
gn:T00085	sco, STRCO, 100226; Streptomyces coelicolor A3(2)
gn:T00126	sma, STRAW, 227882; Streptomyces avermitilis MA-4680
gn:T00691	sgr, STRGG, 455632; Streptomyces griseus subsp. griseus NBRC 13350
gn:T01187	scb, 680198; Streptomyces scabiei 87.22
gn:T01601	ssx, 862751; Streptomyces sp. SirexAA-E
gn:T01602	svl, 653045; Streptomyces violaceusniger Tu 4113
gn:T01646	sct, 1003195; Streptomyces cattleya NRRL 8057 = DSM 46488
gn:T01647	sfa, 591167; Streptomyces pratensis ATCC 33331
gn:T01678	sbh, 749414; Streptom  ...

$ python KPHMMER.py search -a
[2018/02/26 17:06:19] === Search start. ===
[2018/02/26 17:06:19] Show all start.
T01001	hsa	Homo sapiens (human)	Eukaryotes;Animals;Vertebrates;Mammals
T01005	ptr	Pan troglodytes (chimpanzee)	Eukaryotes;Animals;Vertebrates;Mammals
T02283	pps	Pan paniscus (bonobo)	Eukaryotes;Animals;Vertebrates;Mammals
T02442	ggo	Gorilla gorilla gorilla (western lowland gorilla)	Eukaryotes;Animals;Vertebrates;Mammals
T01416	pon	Pongo abelii (Sumatran orangutan)	Eukaryotes;Animals;Vertebrates;Mammals
T03265	nle	Nomascus leucogenys (northern white-cheeked gibbon)	Eukaryotes;Animals;Vertebrates;Mammals
T01028	mcc	Macaca mulatta (rhesus monkey)	Eukaryotes;Animals;Vertebrates;Mammals
T02918	mcf	Macaca fascicularis (crab-eating macaque)	Eukaryotes;Animals;Vertebrates;Mammals
T04361	csab	Chlorocebus sabaeus (green monkey)	Eukaryotes;Animals;Vertebrates;Mammals
T03989	rro	Rhinopithecus roxellana (golden snub-nosed monkey)	Eukaryotes;Animals;Vertebrates;Mammals
T04641	rbb	Rhinopithecus bieti (black snub-nosed monkey)	Eukaryotes;Animals;Vertebrates;Mammals
T03264	cjc	Callithrix jacchus (white-tufted-ear marmoset)	Eukaryotes;Animals;Vertebrates;Mammals
T04350	sbq	Saimiri boliviensis boliviensis (Bolivian squirrel monkey)	Eukaryotes;Animals;Vertebrates;Mammals
T01002	mmu	Mus musculus (mouse)	Eukaryotes;Animals;Vertebrates;Mammals
T01003	rno	Rattus norvegicus (rat)	Eukaryotes;Animals;Vertebrates;Mammals
T02813	cge	Cricetulus griseus (Chinese hamster)	Eukaryote ...
```
### query
Query receives multiple KEGG's organism codes and outputs yaml file for each code.

```
$ python KPHMMER.py query -h
usage: KPHMMER.py query [-h] [-o [OUTPUT]] [-a] CODE [CODE ...]

It receives the KEGG's organism code and outputs the motif yaml file. If you
do not know KEGG's organism code (ex.hsa), use serarch method.

positional arguments:
  CODE                  Specify KEGG's organism code (ex.hsa). Multiple inputs
                        are accepted.

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        Where motif yaml file is generated. If it does not
                        exist, it is created for each directory. (default=./)
  -a, --with-analysis   If you want to do analysis together, specify this
                        method.

$ python KPHMMER.py query sco smu -o ./sco_smu
[2018/02/26 17:10:50] === Query start. ===
[2018/02/26 17:10:50] Your query : ['sco', 'smu']
[2018/02/26 17:10:50] Search pathway start.
[2018/02/26 17:10:52] Format pathway start.
[2018/02/26 17:10:52] sco's 1st pathway count : 83
[2018/02/26 17:10:52] sco's 2nd pathway count : 19
[2018/02/26 17:10:52] smu's 1st pathway count : 62
[2018/02/26 17:10:52] smu's 2nd pathway count : 8
[2018/02/26 17:10:52] Find gene start.
[2018/02/26 17:10:52] sco's 1st gene count : 1028
[2018/02/26 17:10:52] sco's 2nd gene count : 144
[2018/02/26 17:10:52] sco's duplicate gene count : 67
[2018/02/26 17:10:52] smu's 1st gene count : 403
[2018/02/26 17:10:52] smu's 2nd gene count : 25
[2018/02/26 17:10:52] smu's duplicate gene count : 13
[2018/02/26 17:10:52] Find pathway start.
[2018/02/26 17:11:22] Dump motif file start.
[2018/02/26 17:11:22] === Query finish. ===

$ ls ./sco_smu
sco.yml  smu.yml
```

#### Inside yaml file
./sco.yml (Streptomyces coelicolor)
```
CONFIG:
  1ST_CATEGORY: ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.11']
  2ND_CATEGORY: ['1.9', '1.10', '1.12']
  CREATE_DATE: 2018/02/26 17:11:22
  INSERT_DUPLICATE: 2nd
  ORGANISM: sco
GENE:
  1ST: ['sco:SCO5208', 'sco:SCO5470', 'sco:SCO3486', 'sco:SCO6782', 'sco:SCO2688',
    'sco:SCO1577', 'sco:SCO1454', 'sco:SCO6075', 'sco:SCO2194', ...]
  2ND: ['sco:SCO5888', 'sco:SCO3229', 'sco:SCO5878', 'sco:SCO5071', 'sco:SCO3243',
    'sco:SCO5893', 'sco:SCO3739', 'sco:SCO2126', 'sco:SCO7691', 'sco:SCO5074', ...]
MOTIF:
  sco:SCO0063: [ROK]
  sco:SCO0088: [Beta-lactamase2, Beta-lactamase, Peptidase_S13, Rib]
  sco:SCO0136: [EIIC-GAT]
  sco:SCO0137: [PTS_EIIA_2, PTS_IIB, EnY2]
  sco:SCO0166: [PPK2]
  sco:SCO0171: [NAPRTase]
  ...
PATHWAY:
  1ST: ['scopath:sco00770', 'scopath:sco00650', 'scopath:sco00590', 'scopath:sco00380',
    'scopath:sco00362', 'scopath:sco00621', 'scopath:sco00630', 'scopath:sco00910',
    'scopath:sco00472', 'scopath:sco00622', 'scopath:sco00920', 'scopath:sco00780',
    'scopath:sco00290', ...]
  2ND: ['scopath:sco00903', 'scopath:sco01059', 'scopath:sco00523', 'scopath:sco01055',
    'scopath:sco00401', 'scopath:sco01057', 'scopath:sco00521', 'scopath:sco01053',
    'scopath:sco00261', ...]
```

### convert
Create fasta file from yaml file generated by query.

```
$ python KPHMMER.py convert -h
usage: KPHMMER.py convert [-h] [-o [OUTPUT]] MOTIF [MOTIF ...]

Receive motif yaml file and outputs the gene contained therein as fasta file.

positional arguments:
  MOTIF                 Specify motif file path. Multiple inputs are accepted.

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        Where output file is generated. If it does not exist,
                        it is created for each directory. (default=./)

$ python KPHMMER.py convert ./sco_smu/sco.yml -o ./sco_smu/
[2018/02/26 17:29:52] === Convert start. ===
[2018/02/26 17:29:52] Comfirm motif file start.
[2018/02/26 17:29:52] Read motif start.
[2018/02/26 17:29:53] Dump fasta start.
[2018/02/26 17:30:15] === Convert finish. ===
```

### analysis
Analusys takes multiple yaml files generated by query as input.
- Output a list of Pfam-domains that are found specifically in each category as tsv file.
- Output HMM file of Pfam-domain that is found specifically in each category.
```
$ python KPHMMER.py analysis -h
usage: KPHMMER.py analysis [-h] [-o [OUTPUT]] MOTIF [MOTIF ...]

Receive motif yaml file and outputs frequently appearing pfam motif only in
the selected category.

positional arguments:
  MOTIF                 Specify motif file path. Multiple inputs are accepted.

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        Where output file is generated. If it does not exist,
                        it is created for each directory. (default=./)

$ python KPHMMER.py analysis -o ./sco_smu/ ./sco_smu/sco.yml ./sco_smu/smu.yml
[2018/02/26 17:34:03] === Analysis start. ===
[2018/02/26 17:34:03] Comfirm motif file start.
[2018/02/26 17:34:03] Read motif start.
[2018/02/26 17:34:03] Count motif start.
[2018/02/26 17:34:03] Stat motif start.
[2018/02/26 17:34:04] Dump tsv start.
[2018/02/26 17:34:04] Dump hmm start.
[2018/02/26 17:34:04] === Analysis finish. ===
```

## Output file
```
$ tree -h
.
├── [ 84K]  sco.yml
├── [510K]  sco_1st.fasta
├── [ 71K]  sco_2nd.fasta
├── [581K]  sco_all.fasta
├── [   0]  sco_smu_1st.hmm
├── [  42]  sco_smu_1st.tsv
├── [   0]  sco_smu_2nd.hmm
├── [  42]  sco_smu_2nd.tsv
├── [ 23K]  sco_smu_all.tsv
└── [ 33K]  smu.yml
```
