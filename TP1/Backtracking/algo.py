def max_subarray_backtracking(arr: list[int]):
  n = len(arr)
  best_sum = -float('inf')
  best_start = 0
  best_end = 0

  def extend_subarray(start, index, current_sum):
    nonlocal best_sum, best_start, best_end
    if index >= n:
      return
    current_sum += arr[index]
    if current_sum > best_sum:
      best_sum = current_sum
      best_start = start
      best_end = index
    if current_sum > 0:
      extend_subarray(start, index + 1, current_sum)
    
    return

  def backtrack_from(i):
    if i >= n:
      return
    extend_subarray(i, i, 0)
    backtrack_from(i + 1)
  
  backtrack_from(0)
  return best_sum, arr[best_start: best_end + 1]
