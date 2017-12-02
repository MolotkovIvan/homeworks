import Prelude hiding (lookup)

data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) deriving Show

lookup x (Node k v l r) | x > k      = lookup x r
                        | x < k      = lookup x l
                        | otherwise  = Just v
lookup _ Nil = Nothing

insert x y (Node k v l r) | x > k     = Node k v l (insert x y r)
                          | x < k     = Node k v (insert x y l) r
                          | otherwise = Node x y l r
insert x y Nil = Node x y Nil Nil

delete x (Node k v l r) | x > k     = Node k v l (delete x r)  
                        | x < k     = Node k v (delete x l) r
                        | otherwise = join l r
    where
        join l Nil = l
        join Nil r = r
        join l r = Node k' v' l r'
            where
                k' = getKey (leftmost r)
                v' = getValue (leftmost r)
                r' = delete (getKey (leftmost r)) r
                leftmost (Node k v Nil r) = (Node k v Nil r)
                leftmost (Node _ _ l _) = leftmost l
                getKey (Node k _ _ _) = k
                getValue (Node _ v _ _) = v
delete _ Nil = Nil
