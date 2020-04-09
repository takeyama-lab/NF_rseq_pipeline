# NF_rseq_pipeline 
有川さん作成のRNA-seq pipelineを，ワークフロー言語であるNextflowに書き換えたもの。全てdocker環境で実施するようにしてあるので，Nextflowとdocker(singularity)さえあれば他の環境構築は必要ない。 
東大スパコンとOILのスパコンにはsingularityが標準で存在するので実質必要なのはNextflowだけである。

## Requirements
- [Nextflow](https://www.nextflow.io/)

## Getting started

### 1. Installing Nextflow

1. Make sure 8 or later is installed on your computer by using the command: `java -version`
2. Enter the below commands in your terminal (The command creates a file nextflow in `~/bin`)

```
mkdir -p ~/bin
cd ~/bin
wget -qO- https://get.nextflow.io | bash
``` 
3. Run the classic Hello world by entering the following command: `~/bin/nextflow run hello` 

### 3. Clone this repository

```
cd
git clone https://github.com/TsumaR/NF_rseq_pipeline.git
```

### 4. Modifying config file 

First, copy config file to the directory.

```
cd ./NF_seq_pipeline

cp config_file/local.config ./
```
Second, edit the `local.config` file.

### 5. Make directory

```
mkdir log
mkdir summary
```

### 6. Run the pipeline

```
~/bin/nextflow run nextflow/main.nf -c run.config -resume -with-report log.01.main.html
~/bin/nextflow run nextflow/hisat2.nf -c run.config -resume -with-report log.02.hisat2.html
~/bin/nextflow run nextflow/stringtie.nf -c run.config -resume -with-report log.03.stringtie.html
~/bin/nextflow run nextflow/qc_for_R.nf -c run.config -resume -with-report log.04.qc_for_R.html
~/bin/nextflow run nextflow/summary.nf -c run.config -resume -with-report log.05.summary.html
``` 

or

```
qsub run..sh
```

## Information 
Version of packages 
