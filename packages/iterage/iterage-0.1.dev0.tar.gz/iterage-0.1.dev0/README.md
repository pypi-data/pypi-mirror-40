# iterage

toolset for python iterators and generators

## iterator operations

Documentation of *iterage* functions and python standard library functions
for do things with iterators and generators.

### reduce

#### any / iterage.reduce.iany

To check if at least one element is true, use the `any` built-in function:

		any([True,  False, False]) # -> True
		any([False, False, False]) # -> False
		
		l = [0, 1, 14]
		any(x > 10 for x in l) # -> True
		any(x < 0 for x in l)  # -> False
		
		# iterage
		iterage.reduce.iany(l, lambda x: x > 10) # -> True


#### all / iterage.reduce.iall

To check if all elements are true:

		all([True, True, True])  # -> True
		all([True, False, True]) # -> False
		
		l = [0, 1, 14]
		any(x >= 0 for x in l) # -> True
		any(x < 0 for x in l)  # -> False
		
		# iterage
		iterage.reduce.iall(l, lambda x: x >= 0) # -> True
		
#### not any / iterage.reduce.inone
	
To check if no element is true:
 
		not any([False, False, False]) # -> True
		not any([True,  False, True])  # -> False
		
		l = [0, 1, 14]
		not any(x >= 0 for x in l) # -> False
		not any(x < 0 for x in l)  # -> True
		
		# iterage
		iterage.reduce.inone(x < 0 for x in l) # -> True
		
		
#### iterage.reduce.iempty
	
Check if iterable is empty:
		
		iterage.reduce.iempty(x < 0 for x in [0,1,2,3]) # -> True
		iterage.reduce.iempty(x > 1 for x in [0,1,2,3]) # -> False
		
#### iterage.reduce.icount
	
Count elements:
		
		iterage.reduce.icount(range(4)) # -> 4
		
#### iterage.reduce.icount_if
	
Count true elements:

		iterage.reduce.count_if([True, False, False]) # -> 1
		
		iterage.reduce.count_if(x > 1 for x in [0,1,2,3]) # -> 2
		
		# alternative
		sum(1 for x in [0,1,2,3] if x > 1) # -> 2
		iterage.reduce.icount(x for x in [0,1,2,3] if x > 1) # -> 2
		
## similar tools

* https://github.com/pytoolz/toolz/blob/master/toolz/itertoolz.py
* https://pypi.python.org/pypi/more-itertools/

