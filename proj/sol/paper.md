# things to mention in ppr 

# Sol1
Additive Model; Learning champ-role success through Embedding layers! extremely small model like 1k params, provides good baseline

- Sol is so memory efficient! (RAM and VRAM)
    - sol 1 weighs about 3.4Kb of memory using *float32*!

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

