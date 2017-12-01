data BinaryTree k v = Nil | Node k v (BinaryTree k v) (BinaryTree k v) deriving Show

lookup' x (Node k v l r) | x > k      = lookup' x r
                         | x < k      = lookup' x l
                         | otherwise  = Just v
lookup' _ Nil = Nothing

insert' x y (Node k v l r) | x > k     = Node k v l (insert' x y r)
                           | x < k     = Node k v (insert' x y l) r
                           | otherwise = Node x y l r
insert' x y Nil = Node x y Nil Nil

getKey (Node k _ _ _) = k

getValue (Node _ v _ _) = v

delete' x (Node k v l r) | x > k     = Node k v l (delete' x r)  
                         | x < k     = Node k v (delete' x l) r
                         | otherwise = reconstruct' l r
                            where
                                reconstruct' Nil Nil = Nil
                                reconstruct' l Nil = l
                                reconstruct' Nil r = r
                                reconstruct' l r = Node (getKey (lr' r)) (getValue (lr' r)) l (delete' (getKey (lr' r)) r)
                                    where
                                        lr' (Node k v Nil r) = (Node k v Nil r)
                                        lr' (Node _ _ l _) = lr' l
delete' _ Nil = Nil







--(Node 2 2 (Node 1 3 Nil Nil) (Node 5 4 (Node 4 7 Nil Nil) (Node 8 13 Nil Nil)))
