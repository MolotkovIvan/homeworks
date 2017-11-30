tail' (_:xs) = xs
tail' _ = []

head' (x:xs) = x

take' 0 _ = []
take' _ [] = []
take' n (x:xs) = x:(take' (n-1) xs)

drop' 0 xs = xs
drop' _ [] = []
drop' n (x:xs) = drop' (n-1) (xs)

filter' f (x:xs) | f x       = x:(filter' f xs)
                 | otherwise = filter' f xs
filter' _ _ = []

foldl' f n (x:xs) = foldl' f (f n x) xs
foldl' _ n _ = n

concat' xs ys = foldr' (:) ys xs
    where
        foldr' f a (x:xs) = f x (foldr f a xs)
        foldr' _ a _ = a 

concat'' (x:xs) ys = (:) x (concat'' xs ys)
concat'' _ ys = ys

qsort' [] = []
qsort' (x:xs) = concat'' (qsort' (filter' (<x) xs)) (x:(qsort'(filter (>= x) xs)))