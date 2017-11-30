tail' (_:xs) = xs
tail' [] = []

head' (x:_) = x

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

concat' (x:xs) ys = x:(concat' xs ys)
concat' [] ys = ys

quickSort' [] = []
quickSort' (x:xs) = concat' (quickSort' (filter' (<x) xs)) (x:(quickSort' (filter (>= x) xs) ))