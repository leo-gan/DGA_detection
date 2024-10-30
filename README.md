This project presents you with the model training for the `DGA anomaly detection`.
It also contains the best models.

>[Domain Generation Algorithms (DGA) (Wikipedia)](https://en.wikipedia.org/wiki/Domain_generation_algorithm#Detection) 
are algorithms seen in various families of malware that are used to periodically 
generate a large number of domain names that can be used as rendezvous points with their 
command and control servers. The large number of potential rendezvous points 
makes it difficult for law enforcement to effectively shut down botnets, 
since infected computers will attempt to contact some of these domain names 
every day to receive updates or commands. The use of public-key cryptography 
in malware code makes it unfeasible for law enforcement and other actors to 
mimic commands from the malware controllers as some worms will automatically 
reject any updates not signed by the malware controllers.

The project is a part of the `DGA anomaly detection` research.

# The best models
## Update: 2022-09-26
It is the `catboost.0.977.26_ensemble.model`. It is trained on 1000 iterations, 
so it is smaller than the previous best model.

See the `DGA_detection.ipynb`: "Ensemble: token-based and bytes-based" section.

The model features are engineered from the domain names of the DNS traffic: 
- ngram length numbers, extracted by a tokenizer: 14 lengths
- bytes as features: 26 bytes. 
- Note: for the long domain names, the model takes bytes from
  the middle of the string.

## 2022-09-23
So far, it is `catboost.0.964.26_bytes.model` it trained on 1400 iterations.
The `catboost.0.962.32_bytes.model` is nearby. It trained on 1000 iterations.
The reason we use the first one, is it smaller.
