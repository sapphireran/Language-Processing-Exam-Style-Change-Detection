# problem-22-kiln-return
site: return
voices: stall, notice, stall
gold authors: 2   return_author: True
gold changes: [0, 1, 0, 1, 0]
notes: authors=2 but 1+sum(changes)=3. Naive author count over-counts the return.

## cut after unit 1   score=0.261   pred=0 gold=0
verdict: true seam
drivers: first_person higher on the left (0.125 vs 0.090); formal higher on the right (0.000 vs 0.030)
  register_l1                  0.092   six-number register vector (exam card)
  function_cosine_distance     0.093   smoothed function-word cosine distance
  char3_distance               0.809   damped character 3-gram distance
  delta                        0.062   intra-document Burrows Delta on function words
  left  first_person=0.125 second_person=0.000 contraction=0.062 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.090 second_person=0.015 contraction=0.060 formal=0.030 hedge=0.000 we_person=0.000

## cut after unit 2   score=0.459   pred=1 gold=1
verdict: true fold
drivers: formal higher on the right (0.000 vs 0.036)
  register_l1                  0.248   six-number register vector (exam card)
  function_cosine_distance     0.081   smoothed function-word cosine distance
  char3_distance               0.855   damped character 3-gram distance
  delta                        0.056   intra-document Burrows Delta on function words
  left  first_person=0.107 second_person=0.000 contraction=0.071 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.091 second_person=0.018 contraction=0.055 formal=0.036 hedge=0.000 we_person=0.000

## cut after unit 3   score=0.089   pred=0 gold=0
verdict: true seam
drivers: first_person higher on the right (0.073 vs 0.119); second_person higher on the right (0.000 vs 0.024); contraction higher on the right (0.049 vs 0.071)
  register_l1                  0.027   six-number register vector (exam card)
  function_cosine_distance     0.057   smoothed function-word cosine distance
  char3_distance               0.800   damped character 3-gram distance
  delta                        0.047   intra-document Burrows Delta on function words
  left  first_person=0.073 second_person=0.000 contraction=0.049 formal=0.024 hedge=0.000 we_person=0.000
  right first_person=0.119 second_person=0.024 contraction=0.071 formal=0.024 hedge=0.000 we_person=0.000

## cut after unit 4   score=0.538   pred=1 gold=1
verdict: true fold
drivers: first_person higher on the right (0.056 vs 0.172); contraction higher on the right (0.037 vs 0.103); formal higher on the left (0.037 vs 0.000)
  register_l1                  0.371   six-number register vector (exam card)
  function_cosine_distance     0.089   smoothed function-word cosine distance
  char3_distance               0.867   damped character 3-gram distance
  delta                        0.072   intra-document Burrows Delta on function words
  left  first_person=0.056 second_person=0.000 contraction=0.037 formal=0.037 hedge=0.000 we_person=0.000
  right first_person=0.172 second_person=0.034 contraction=0.103 formal=0.000 hedge=0.000 we_person=0.000

## cut after unit 5   score=0.440   pred=0 gold=0
verdict: true seam
drivers: first_person higher on the right (0.074 vs 0.200); contraction higher on the right (0.044 vs 0.133); formal higher on the left (0.029 vs 0.000)
  register_l1                  0.228   six-number register vector (exam card)
  function_cosine_distance     0.097   smoothed function-word cosine distance
  char3_distance               0.839   damped character 3-gram distance
  delta                        0.078   intra-document Burrows Delta on function words
  left  first_person=0.074 second_person=0.015 contraction=0.044 formal=0.029 hedge=0.000 we_person=0.000
  right first_person=0.200 second_person=0.000 contraction=0.133 formal=0.000 hedge=0.000 we_person=0.000

