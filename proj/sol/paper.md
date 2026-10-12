# things to mention in ppr 

# Sol1
Additive Model; Learning champ-role success through Embedding layers! extremely small model like 1k params, provides good baseline

## Evaluation Function:

```
logit = bias + Σ(strength[blue[r], r] - strength[red[r], r])
               r=1..5

P(Blue wins) = sigmoid(logit)
```
Where:
- strength: Learnable embedding table of shape (n_champions, 5).
- blue[r]: Blue team's champion assigned to role r.
- red[r]: Red team's champion assigned to role r.
- r: Role index (Top, Jungle, Mid, ADC, Support).
- bias: Learnable scalar representing baseline Blue-side advantage.
- sigmoid: Converts the resulting logit into a win probability between 0 and 1.

