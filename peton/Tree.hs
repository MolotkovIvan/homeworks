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
                        | otherwise = order l r
                            where
                                order l Nil = l
                                order Nil r = r
                                order l r = Node (getKey (mostleft r)) (getValue (mostleft r)) l (delete (getKey (mostleft r)) r)
                                    where
                                        mostleft (Node k v Nil r) = (Node k v Nil r)
                                        mostleft (Node _ _ l _) = mostleft l
                                        getKey (Node k _ _ _) = k
                                        getValue (Node _ v _ _) = v
delete _ Nil = Nil
