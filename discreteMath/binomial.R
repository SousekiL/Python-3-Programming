printBinomailPar <- function(n, i, j) {
  parK <- c()
  par <- c()
  for (k in seq(0, n)) {
    .parK <- choose(n, k)
    .par <- i ^ (n - k) * j ^ (k)
    
    parK <- c(parK, .parK)
    par <- c(par, .par)
  }
  clist <- parK * par
  print(paste0(clist, collapse = ','))
}

printBinomailPar(3, 3, -2)


choose(5, 3) * choose(5, 3) * 6

## We have an unlimited supply of tomatoes, bell peppers and lettuce. We want to make a salad
## out of 4 units among these three ingredients (we do not have to use all ingredients).
## The order in which we use the ingredients does not matter. How many different salads we can make?

# read data of xls files

