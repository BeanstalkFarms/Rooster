# Rooster Server

### Intro
The Rooster server uses a custom index to answer user questions.
While gpt_index was useful in getting the first iteration, it showed low answer quality.

After experimentation, using GPT to summarize key points of each doc and then asking it to pick the right doc given the
question and all of the key points proved to be a better method to provide GPT context.

### Index
build_doc_lookup.py has two relevant methods. 

#### generate_lookup_doc - build index and save to lookup.txt
#### get_doc_num_to_path - map lookup.txt line # to document