# problem-01-kiln-then-notice
site: easy
voices: stall, notice
gold authors: 2   return_author: False
gold changes: [0, 0, 1, 0, 0]
notes: Stall first person + contractions against shall/must notice. Clean exam hinge.

## cut after unit 1   score=0.301   pred=0 gold=0
verdict: true seam
drivers: formal higher on the right (0.000 vs 0.044); contraction higher on the left (0.059 vs 0.029)
  register_l1                  0.113   six-number register vector (exam card)
  function_cosine_distance     0.059   smoothed function-word cosine distance
  char3_distance               0.816   damped character 3-gram distance
  delta                        0.047   intra-document Burrows Delta on function words
  left  first_person=0.059 second_person=0.000 contraction=0.059 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.059 second_person=0.000 contraction=0.029 formal=0.044 hedge=0.000 we_person=0.000

## cut after unit 2   score=0.323   pred=0 gold=0
verdict: true seam
drivers: first_person higher on the left (0.118 vs 0.020); formal higher on the right (0.000 vs 0.059); contraction higher on the left (0.059 vs 0.020)
  register_l1                  0.123   six-number register vector (exam card)
  function_cosine_distance     0.091   smoothed function-word cosine distance
  char3_distance               0.862   damped character 3-gram distance
  delta                        0.072   intra-document Burrows Delta on function words
  left  first_person=0.118 second_person=0.000 contraction=0.059 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.020 second_person=0.000 contraction=0.020 formal=0.059 hedge=0.000 we_person=0.000

## cut after unit 3   score=0.487   pred=1 gold=1
verdict: true fold
drivers: first_person higher on the left (0.114 vs 0.000); formal higher on the right (0.000 vs 0.073); contraction higher on the left (0.068 vs 0.000)
  register_l1                  0.284   six-number register vector (exam card)
  function_cosine_distance     0.090   smoothed function-word cosine distance
  char3_distance               0.864   damped character 3-gram distance
  delta                        0.066   intra-document Burrows Delta on function words
  left  first_person=0.114 second_person=0.000 contraction=0.068 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.073 hedge=0.000 we_person=0.000

## cut after unit 4   score=0.135   pred=0 gold=0
verdict: true seam
drivers: first_person higher on the left (0.088 vs 0.000); formal higher on the right (0.018 vs 0.071); contraction higher on the left (0.053 vs 0.000)
  register_l1                  0.044   six-number register vector (exam card)
  function_cosine_distance     0.096   smoothed function-word cosine distance
  char3_distance               0.806   damped character 3-gram distance
  delta                        0.081   intra-document Burrows Delta on function words
  left  first_person=0.088 second_person=0.000 contraction=0.053 formal=0.018 hedge=0.000 we_person=0.000
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.071 hedge=0.000 we_person=0.000

## cut after unit 5   score=0.017   pred=0 gold=0
verdict: true seam
drivers: first_person higher on the left (0.070 vs 0.000); formal higher on the right (0.028 vs 0.071); contraction higher on the left (0.042 vs 0.000)
  register_l1                  0.001   six-number register vector (exam card)
  function_cosine_distance     0.065   smoothed function-word cosine distance
  char3_distance               0.757   damped character 3-gram distance
  delta                        0.059   intra-document Burrows Delta on function words
  left  first_person=0.070 second_person=0.000 contraction=0.042 formal=0.028 hedge=0.000 we_person=0.000
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.071 hedge=0.000 we_person=0.000

