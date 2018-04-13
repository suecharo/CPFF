## KPHMMER_API_access.py
- KPHMMER でそれぞれの API を叩いた回数を表示するバージョン
$ python3 KPHMMER_API-access.py で普通の使い方

## KPHMMER_stat.py
- KPHMMER analysis で出力した，hmm file を用いて，対象の fasta に対し HMMER をかける。
- その出力の tsv file と 対象生物の KPHMMER query で出力された yaml file を入力として，統計的な結果を求める
$ python3 KPHMMER_stat.py hoge.tsv piyo.yml
