# Solution for University of Latvia Combinatorial Optimisation course

## Uzdevums:

> Ir doti n punkti, kur katram ir noteikta vērtība v[i].
> Ir dots sākuma punkts s un finiša punkts f (vai tas ir tas pats?).
> Dota laika matrica d, kurā jau iepriekš sarēķināts nepieciešamais laiks, lai nokļūtu no katra uz katru punktu.
> Uzdevums ir atrast tādu punktu virkni, kas sākas punktā s un beidzas punktā f un dod vislielāko vērtību, bet prasa ne vairāk laika kā dotais limits t.


## Palaišana:
```bash
docker build --tag 'puupuls-co' .
docker run -d -p 5000:5000 puupuls-co
```
Pārlūkprogrammā jāatver: http://localhost:5000