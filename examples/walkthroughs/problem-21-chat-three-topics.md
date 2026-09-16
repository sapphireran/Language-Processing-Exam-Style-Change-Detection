# problem-21-chat-three-topics
site: control
voices: chat, chat, chat
gold authors: 1   return_author: False
gold changes: [0, 0, 0, 0, 0]
notes: Short chat units jitter length and vocatives. A known false-alarm risk.

## cut after unit 1   score=0.396   pred=1 gold=0
verdict: false fold (chat_jitter)
drivers: first_person higher on the right (0.100 vs 0.174); contraction higher on the right (0.100 vs 0.174)
  register_l1                  0.194   six-number register vector (exam card)
  function_cosine_distance     0.081   smoothed function-word cosine distance
  char3_distance               0.957   damped character 3-gram distance
  delta                        0.047   intra-document Burrows Delta on function words
  left  first_person=0.100 second_person=0.000 contraction=0.100 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.174 second_person=0.000 contraction=0.174 formal=0.000 hedge=0.000 we_person=0.000

## cut after unit 2   score=0.372   pred=0 gold=0
verdict: true seam
  register_l1                  0.191   six-number register vector (exam card)
  function_cosine_distance     0.065   smoothed function-word cosine distance
  char3_distance               0.877   damped character 3-gram distance
  delta                        0.040   intra-document Burrows Delta on function words
  left  first_person=0.158 second_person=0.000 contraction=0.158 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.162 second_person=0.000 contraction=0.162 formal=0.000 hedge=0.000 we_person=0.000

## cut after unit 3   score=0.354   pred=0 gold=0
verdict: true seam
drivers: first_person higher on the right (0.133 vs 0.192); contraction higher on the right (0.133 vs 0.192)
  register_l1                  0.212   six-number register vector (exam card)
  function_cosine_distance     0.069   smoothed function-word cosine distance
  char3_distance               0.861   damped character 3-gram distance
  delta                        0.041   intra-document Burrows Delta on function words
  left  first_person=0.133 second_person=0.000 contraction=0.133 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.192 second_person=0.000 contraction=0.192 formal=0.000 hedge=0.000 we_person=0.000

## cut after unit 4   score=0.414   pred=0 gold=0
verdict: true seam
drivers: first_person higher on the right (0.139 vs 0.200)
  register_l1                  0.213   six-number register vector (exam card)
  function_cosine_distance     0.084   smoothed function-word cosine distance
  char3_distance               0.907   damped character 3-gram distance
  delta                        0.053   intra-document Burrows Delta on function words
  left  first_person=0.139 second_person=0.000 contraction=0.167 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.200 second_person=0.000 contraction=0.150 formal=0.000 hedge=0.000 we_person=0.000

## cut after unit 5   score=0.495   pred=1 gold=0
verdict: false fold (chat_jitter)
drivers: first_person higher on the right (0.143 vs 0.286); contraction higher on the right (0.143 vs 0.286)
  register_l1                  0.311   six-number register vector (exam card)
  function_cosine_distance     0.054   smoothed function-word cosine distance
  char3_distance               0.819   damped character 3-gram distance
  delta                        0.037   intra-document Burrows Delta on function words
  left  first_person=0.143 second_person=0.000 contraction=0.143 formal=0.000 hedge=0.000 we_person=0.000
  right first_person=0.286 second_person=0.000 contraction=0.286 formal=0.000 hedge=0.000 we_person=0.000

