tail' (x:xs) = xs
tail' [] = []

head' (x:xs) = [x]
head' [] = []

take' 0 _ = []
take' _ [] = []
take' n (x:xs) = x:(take' (n-1) xs)

drop' 0 xs = xs
drop' _ [] = []
drop' n (x:xs) = drop' (n-1) (xs)

filter' f (x:xs) | f x       = x:(filter' f xs)
                 | otherwise = filter' f xs
filter' _ [] = []

foldl' f n (x:xs) = foldl' f (f n x) xs
foldl' _ n [] = n

len' xs = len'' 0 xs
    where
        len'' n [] = n   
        len'' n (x:xs) = len'' (n+1) xs 

concat' [] ys = ys
concat' xs ys = concat' (take' ((len' xs) - 1) xs) ((last' xs) : ys)
    where
        last' (x:[]) = x
        last' (x:xs) = last xs

qsort' [] = []
qsort' (x:xs) = concat' (qsort' (filter' (<=x) xs)) (x:(qsort'(filter (>= x) xs)))