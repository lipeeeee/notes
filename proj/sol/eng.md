# proj setup 
running specific files seperatly makes it more direct what u trying to do
- sol/train.py
- sol/run.py / inference.py or fancier name (THIS IS CLI RUN)
- sol/helpers.py (that is imported eveywhere and setups env and checks for pkgs/data)
- config/sol_n.py configs, defaulting to latest or last_used(we can do a .sol_env! which can be cute)


keep in mind: the scraping of data from oracle should be consistent across all
iterations ideally (just scrape all, each config will NEED post-processing)
- post-processing fns should have alot of args for multiple usages in multiple configs

# iterations
diff layers, diff input data, diff output data, diff hyperparams(dotdict impl)

definition + hyperparams configs
