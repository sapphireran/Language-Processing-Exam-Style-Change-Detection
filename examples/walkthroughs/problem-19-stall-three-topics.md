# problem-19-stall-three-topics
site: control
voices: stall, stall, stall
gold authors: 1   return_author: False
gold changes: [0, 0, 0, 0, 0]
notes: Topic changes at 2 and 4. Register does not. A content model should twitch; we should not.

## cut after unit 1   score=0.202   pred=0 gold=0
verdict: true seam
drivers: first_person higher on the left (0.182 vs 0.143); contraction higher on the left (0.182 vs 0.143)
  register_l1                  0.064   six-number register vector (exam card)
  function_cosine_distance     0.052   smoothed function-word cosine distance
  char3_distance               0.617   damped character 3-gram distance
  delta                        0.035   intra-document Burrows Delta on function words
  left  first_person=0.182 second_person=0.000 contraction=0.182 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.143 second_person=0.000 contraction=0.143 formal=0.000 hedge=0.000 we_person=0.000

## cut after unit 2   score=0.152   pred=0 gold=0
verdict: true seam
drivers: first_person higher on the left (0.167 vs 0.140); contraction higher on the left (0.167 vs 0.140)
  register_l1                  0.043   six-number register vector (exam card)
  function_cosine_distance     0.050   smoothed function-word cosine distance
  char3_distance               0.655   damped character 3-gram distance
  delta                        0.031   intra-document Burrows Delta on function words
  left  first_person=0.167 second_person=0.000 contraction=0.167 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.140 second_person=0.000 contraction=0.140 formal=0.000 hedge=0.000 we_person=0.000

## cut after unit 3   score=0.094   pred=0 gold=0
verdict: true seam
  register_l1                  0.027   six-number register vector (exam card)
  function_cosine_distance     0.026   smoothed function-word cosine distance
  char3_distance               0.581   damped character 3-gram distance
  delta                        0.022   intra-document Burrows Delta on function words
  left  first_person=0.154 second_person=0.000 contraction=0.154 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.143 second_person=0.000 contraction=0.143 formal=0.000 hedge=0.000 we_person=0.000

## cut after unit 4   score=0.120   pred=0 gold=0
verdict: true seam
  register_l1                  0.030   six-number register vector (exam card)
  function_cosine_distance     0.094   smoothed function-word cosine distance
  char3_distance               0.590   damped character 3-gram distance
  delta                        0.069   intra-document Burrows Delta on function words
  left  first_person=0.154 second_person=0.000 contraction=0.154 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.138 second_person=0.000 contraction=0.138 formal=0.000 hedge=0.000 we_person=0.000

## cut after unit 5   score=0.064   pred=0 gold=0
verdict: true seam
  register_l1                  0.012   six-number register vector (exam card)
  function_cosine_distance     0.095   smoothed function-word cosine distance
  char3_distance               0.586   damped character 3-gram distance
  delta                        0.072   intra-document Burrows Delta on function words
  left  first_person=0.149 second_person=0.000 contraction=0.149 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.143 second_person=0.000 contraction=0.143 formal=0.000 hedge=0.000 we_person=0.000

