# Apriori Algorithm

Apriori is an algorithm for frequent item set mining and association rule learning over relational databases.

# Run

Firstly you should install requirements in requirements.txt via 

    pip install -r requirements.txt
  
  Then, you can run the program. Program take 3 command line argument for file name, min support and min confidance, if you don't enter support or confidence program will delete all candidates which have minimum support and confidance for thoose candidate.
  So you can run like this

    python apriori.py filename.(txt or xlsx) 1.0(float for min support) 0.5(float for min confidance)
