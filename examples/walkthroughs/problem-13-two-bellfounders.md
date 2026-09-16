# problem-13-two-bellfounders
site: hard
voices: notebook, notebook
gold authors: 2   return_author: False
gold changes: [0, 0, 1, 0, 0]
notes: Gold hinge after unit 3. Both voices are hedged scientific we. Default cut should stay quiet.

## cut after unit 1   score=0.336   pred=0 gold=0
verdict: true seam
drivers: hedge higher on the right (0.000 vs 0.081)
  register_l1                  0.132   six-number register vector (exam card)
  function_cosine_distance     0.091   smoothed function-word cosine distance
  char3_distance               0.766   damped character 3-gram distance
  delta                        0.094   intra-document Burrows Delta on function words
  left  first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.000 we_person=0.056
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.081 we_person=0.047

## cut after unit 2   score=0.032   pred=0 gold=0
verdict: true seam
  register_l1                  0.003   six-number register vector (exam card)
  function_cosine_distance     0.110   smoothed function-word cosine distance
  char3_distance               0.773   damped character 3-gram distance
  delta                        0.112   intra-document Burrows Delta on function words
  left  first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.059 we_person=0.059
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.071 we_person=0.043

## cut after unit 3   score=0.310   pred=0 gold=1
verdict: missed fold (same_register_miss)
drivers: hedge higher on the left (0.080 vs 0.056); we_person higher on the left (0.060 vs 0.037)
  register_l1                  0.117   six-number register vector (exam card)
  function_cosine_distance     0.077   smoothed function-word cosine distance
  char3_distance               0.770   damped character 3-gram distance
  delta                        0.072   intra-document Burrows Delta on function words
  left  first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.080 we_person=0.060
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.056 we_person=0.037

## cut after unit 4   score=0.210   pred=0 gold=0
verdict: true seam
drivers: we_person higher on the left (0.061 vs 0.026)
  register_l1                  0.059   six-number register vector (exam card)
  function_cosine_distance     0.138   smoothed function-word cosine distance
  char3_distance               0.809   damped character 3-gram distance
  delta                        0.125   intra-document Burrows Delta on function words
  left  first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.061 we_person=0.061
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.079 we_person=0.026

## cut after unit 5   score=0.336   pred=0 gold=0
verdict: true seam
drivers: we_person higher on the left (0.059 vs 0.000); hedge higher on the right (0.059 vs 0.105)
  register_l1                  0.115   six-number register vector (exam card)
  function_cosine_distance     0.223   smoothed function-word cosine distance
  char3_distance               0.809   damped character 3-gram distance
  delta                        0.168   intra-document Burrows Delta on function words
  left  first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.059 we_person=0.059
  right first_person=0.000 second_person=0.000 contraction=0.000 formal=0.000 hedge=0.105 we_person=0.000

