# problem-24-gift-abstract
site: gift
voices: notebook, notice
gold authors: 2   return_author: False
gold changes: [0, 0, 1, 0, 0]
notes: Gift authorship: student hedges, supervisor deletes the hedges and installs must/shall.

## cut after unit 1   score=0.207   pred=0 gold=0
verdict: true seam
drivers: hedge higher on the left (0.062 vs 0.028); formal higher on the right (0.000 vs 0.028); we_person higher on the left (0.062 vs 0.042)
  register_l1                  0.063   six-number register vector (exam card)
  function_cosine_distance     0.087   smoothed function-word cosine distance
  char3_distance               0.789   damped character 3-gram distance
  delta                        0.087   intra-document Burrows Delta on function words
  left  first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.062 we_person=0.062
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.028 hedge=0.028 we_person=0.042

## cut after unit 2   score=0.409   pred=0 gold=0
verdict: true seam
drivers: hedge higher on the left (0.097 vs 0.000); formal higher on the right (0.000 vs 0.036); we_person higher on the left (0.065 vs 0.036)
  register_l1                  0.177   six-number register vector (exam card)
  function_cosine_distance     0.177   smoothed function-word cosine distance
  char3_distance               0.783   damped character 3-gram distance
  delta                        0.134   intra-document Burrows Delta on function words
  left  first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.097 we_person=0.065
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.036 hedge=0.000 we_person=0.036

## cut after unit 3   score=0.456   pred=1 gold=1
verdict: true fold
drivers: we_person higher on the left (0.087 vs 0.000); hedge higher on the left (0.065 vs 0.000); formal higher on the right (0.000 vs 0.049)
  register_l1                  0.216   six-number register vector (exam card)
  function_cosine_distance     0.208   smoothed function-word cosine distance
  char3_distance               0.745   damped character 3-gram distance
  delta                        0.159   intra-document Burrows Delta on function words
  left  first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.065 we_person=0.087
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.049 hedge=0.000 we_person=0.000

## cut after unit 4   score=0.117   pred=0 gold=0
verdict: true seam
drivers: we_person higher on the left (0.067 vs 0.000); hedge higher on the left (0.050 vs 0.000); formal higher on the right (0.017 vs 0.037)
  register_l1                  0.028   six-number register vector (exam card)
  function_cosine_distance     0.155   smoothed function-word cosine distance
  char3_distance               0.830   damped character 3-gram distance
  delta                        0.125   intra-document Burrows Delta on function words
  left  first_person=0.000 second_person=0.000 contraction=0.000 formal=0.017 hedge=0.050 we_person=0.067
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.037 hedge=0.000 we_person=0.000

## cut after unit 5   score=0.236   pred=0 gold=0
verdict: true seam
drivers: we_person higher on the left (0.053 vs 0.000); hedge higher on the left (0.040 vs 0.000); formal higher on the left (0.027 vs 0.000)
  register_l1                  0.067   six-number register vector (exam card)
  function_cosine_distance     0.172   smoothed function-word cosine distance
  char3_distance               0.769   damped character 3-gram distance
  delta                        0.115   intra-document Burrows Delta on function words
  left  first_person=0.000 second_person=0.000 contraction=0.000 formal=0.027 hedge=0.040 we_person=0.053
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.000 we_person=0.000

