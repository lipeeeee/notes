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

- put dataset computation in fn's so older models wont be computing synergy for hours,
- also we should look into freezing computed datasets if they take too long, just like in tokenizers in transformers

- idk if oracle's elixir need data cleaning before processing into dataset, best is to clean whilst processing

# champ embeddings
- v0: need translation from name to ID from day 0 cuz we should never change champ representation
- v1: just embed champ number
- v2: synergy calcs(carefull because this might put too much emphasis on meta drafts...)

# role embeddings
- v1: from here picks should already be embedded

# refining
- things like golddiff@10 and how much by they win should probably be considered and impact model's confidence
- we should build a benchmark where we input some drafts experts think its geniunly best and check how they do

# data loading & gpu performance speed
- Entire selected dataset on GPU	==== Avoids repeated input transfers BUT takes some gpu memory
- Dataset in RAM, batches to GPU	==== Avoids disk reads during training BUT CPU-GPU copy kernels can suck
- Dataset on disk, batches through RAM to GPU ==== Small memory footprint BUT loading may become the bottleneck

# iterations
diff layers, diff input data, diff output data, diff hyperparams(dotdict impl)

definition + hyperparams configs

# oracle's elixir struct

165 unique columns

| Group | Fields |
|---|---|
| Match and source (10) | `gameid`, `datacompleteness`, `url`, `league`, `year`, `split`, `playoffs`, `date`, `game`, `patch` |
| Participant identity (7) | `participantid`, `side`, `position`, `playername`, `playerid`, `teamname`, `teamid` |
| Draft (12) | `firstPick`, `champion`, `ban1`, `ban2`, `ban3`, `ban4`, `ban5`, `pick1`, `pick2`, `pick3`, `pick4`, `pick5` |
| Result and combat (17) | `gamelength`, `result`, `kills`, `deaths`, `assists`, `teamkills`, `teamdeaths`, `doublekills`, `triplekills`, `quadrakills`, `pentakills`, `firstblood`, `firstbloodkill`, `firstbloodassist`, `firstbloodvictim`, `team kpm`, `ckpm` |
| Dragons (14) | `firstdragon`, `dragons`, `opp_dragons`, `elementaldrakes`, `opp_elementaldrakes`, `infernals`, `mountains`, `clouds`, `oceans`, `chemtechs`, `hextechs`, `dragons (type unknown)`, `elders`, `opp_elders` |
| Heralds and grubs (5) | `firstherald`, `heralds`, `opp_heralds`, `void_grubs`, `opp_void_grubs` |
| Baron and Atakhan (5) | `firstbaron`, `barons`, `opp_barons`, `atakhans`, `opp_atakhans` |
| Towers and inhibitors (9) | `firsttower`, `towers`, `opp_towers`, `firstmidtower`, `firsttothreetowers`, `turretplates`, `opp_turretplates`, `inhibitors`, `opp_inhibitors` |
| Damage (6) | `damagetochampions`, `dpm`, `damageshare`, `damagetakenperminute`, `damagemitigatedperminute`, `damagetotowers` |
| Vision (7) | `wardsplaced`, `wpm`, `wardskilled`, `wcpm`, `controlwardsbought`, `visionscore`, `vspm` |
| Gold and farming (13) | `totalgold`, `earnedgold`, `earned gpm`, `earnedgoldshare`, `goldspent`, `gspd`, `gpr`, `total cs`, `minionkills`, `monsterkills`, `monsterkillsownjungle`, `monsterkillsenemyjungle`, `cspm` |


| Measurement | 10 min | 15 min | 20 min | 25 min |
|---|---|---|---|---|
| Gold | `goldat10` | `goldat15` | `goldat20` | `goldat25` |
| XP | `xpat10` | `xpat15` | `xpat20` | `xpat25` |
| CS | `csat10` | `csat15` | `csat20` | `csat25` |
| Opponent gold | `opp_goldat10` | `opp_goldat15` | `opp_goldat20` | `opp_goldat25` |
| Opponent XP | `opp_xpat10` | `opp_xpat15` | `opp_xpat20` | `opp_xpat25` |
| Opponent CS | `opp_csat10` | `opp_csat15` | `opp_csat20` | `opp_csat25` |
| Gold difference | `golddiffat10` | `golddiffat15` | `golddiffat20` | `golddiffat25` |
| XP difference | `xpdiffat10` | `xpdiffat15` | `xpdiffat20` | `xpdiffat25` |
| CS difference | `csdiffat10` | `csdiffat15` | `csdiffat20` | `csdiffat25` |
| Kills | `killsat10` | `killsat15` | `killsat20` | `killsat25` |
| Assists | `assistsat10` | `assistsat15` | `assistsat20` | `assistsat25` |
| Deaths | `deathsat10` | `deathsat15` | `deathsat20` | `deathsat25` |
| Opponent kills | `opp_killsat10` | `opp_killsat15` | `opp_killsat20` | `opp_killsat25` |
| Opponent assists | `opp_assistsat10` | `opp_assistsat15` | `opp_assistsat20` | `opp_assistsat25` |
| Opponent deaths | `opp_deathsat10` | `opp_deathsat15` | `opp_deathsat20` | `opp_deathsat25` |

each game has: **12 rows**: ten players (`participantid` 1–10) and two teams (`100` and `200`). `(gameid, participantid)` is unique. Empty cells represent missing values.
