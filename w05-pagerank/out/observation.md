# Observations

## Task 1

- In the broken version, a page with no outgoing links receives a score but does not pass it on, so the total score decreases. In the working version, I split that score equally among all pages, including the page itself.
- Letting scores move to any page helps with both problems. It keeps scores from disappearing at a dead end and gives them a way out of a group of pages that only link to each other.
- With beta=0.85, the surfer follows a link 85% of the time and jumps to a randomly chosen page 15% of the time.

## Task 2

- With 1,200 nodes and tol=1e-10, changing beta from 0.5 to 0.99 increased the number of repetitions from 14 to 24. With fewer random jumps, the scores took longer to settle down.
- At beta=0.85, increasing the graph from 1,200 to 20,000 nodes only changed the repetitions from 20 to 21, but the time went from about 0.0192 to 0.5155 seconds. This helped me see that each repetition can take more time even when the number of repetitions barely changes.
- Of the beta values tested, 0.7 was the first where seventh and eighth place swapped. The same ten pages stayed in the top 10, but their order was not exactly the same, so I would check the beta value before comparing rankings.

## Task 3

- I used the existing lists of links instead of making a table for every possible pair of pages. For N pages and E links, the graph stores N pages and E links, while the old and new scores need 2N numbers. The code reports 2N+16 to also allow for a few extra numbers used during calculation.
- Every page gets the same amount from a random jump, so I can calculate that amount once and add it to each page. I handle the score from dead ends in the same way. I only need to visit each page and each actual link, rather than fill an N-by-N table.
- In the saved run, the new version was about 53 times faster and used 2,416 score-related number slots instead of 1,440,000, about 596 times fewer. The largest score difference was only 1.18e-15, below the allowed 1e-9. Computers round decimal calculations, so changing the calculation order can leave a tiny difference; the measured speed can also vary between runs.
