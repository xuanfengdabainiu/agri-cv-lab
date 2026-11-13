# Paper Notes

## 1. One-sentence summary

The study identifies blueberry bZIP transcription factors genome-wide and analyzes their expression responses to salt, drought, and ABA stress.

## 2. Problem

The authors want to identify candidate bZIP genes that may connect ABA signaling with salt and drought tolerance in blueberry.

## 3. Core workflow

```text
Blueberry genome
  -> bZIP domain search and filtering
  -> 102 VcbZIP genes
  -> phylogeny, motifs, gene structures, promoter elements
  -> salt/drought/ABA RNA-seq expression analysis
  -> stress-responsive gene screening and correlation analysis
  -> RT-qPCR validation
```

## 4. Experiments

- Identify candidates with Pfam bZIP HMM profiles and Arabidopsis reference sequences.
- Confirm domains with SMART and CDD.
- Construct phylogenetic groups with Arabidopsis bZIP proteins.
- Analyze motifs, exon-intron structures, and 2 kb promoter regions.
- Compare expression under drought, salt, and ABA stress.
- Validate selected genes with RT-qPCR.

## 5. Limitations

- The study depends on online databases and software versions that may change.
- Raw RNA-seq analysis requires substantial storage and compute time.
- The paper's data availability statement points to supplementary materials, while the raw reads are stored in NCBI BioProjects.
- Reproducing wet-lab RT-qPCR is outside this computational project.

## 6. Possible improvements

- Use a reproducible command-line workflow instead of manual web tools.
- Record exact database versions and downloaded files.
- Re-run differential expression from raw reads and compare against the supplied tables.
- Add independent visualization and statistical checks.
- Compare the results with a newer blueberry genome annotation when appropriate.

