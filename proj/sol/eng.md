# proj setup 
running specific files seperatly makes it more direct what u trying to do
- sol/train.py
- sol/run.py / inference.py or fancier name (THIS IS CLI RUN)
- sol/helpers.py (that is imported eveywhere and setups env and checks for pkgs/data)
- sol/update_data.py for oracle scraping?
- config/sol_n.py configs, defaulting last_used(we can do a .sol_env! which can be cute)


keep in mind: the scraping of data from oracle should be consistent across all
iterations ideally (just scrape all, each config will NEED post-processing)
- post-processing fns should have alot of args for multiple usages in multiple configs

# champ embeddings
- v1: just embed champ number
- v2: synergy calcs(carefull because this might put too much emphasis on meta drafts...)

# role embeddings
- v1: from here picks should already be embedded

# refining
- things like golddiff@10 and how much by they win should probably be considered and impact model's confidence
- we should build a benchmark where we input some drafts experts think its geniunly best and check how they do

# iterations
diff layers, diff input data, diff output data, diff hyperparams(dotdict impl)

definition + hyperparams configs
