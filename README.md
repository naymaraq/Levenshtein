## Levenshtein distance

How do we find the minimum edit distance? We can think of this as a search task, in
which we are searching for the shortest path—a sequence of edits—from one string
to another

Let’s first define the minimum edit distance between two strings. Given two
strings, the source string X of length n, and target string Y of length m, we’ll define
D(i, j) as the edit distance between X[1..i] and Y[1.. j], i.e., the first i characters of X
and the first j characters of Y. The edit distance between X and Y is thus D(n,m)

![equation](https://qkdb.files.wordpress.com/2012/10/edit_distance.png)

Tasks
- [ ] Branch from master 
- [ ] Implement class, which have two methods which are returns the distance and the alignment backtrace
- [ ] Solve merge conflicts 

The output will look-like this

```python
>>> from Levenshtein import LevDist
>>> m = LevDist('Price', 'Prize')
>>> print(m.get_distance())
>>> print(m.get_backtrace())
```
