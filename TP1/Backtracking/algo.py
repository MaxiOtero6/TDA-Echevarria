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

def read_sets(path: str):
  sets = []
  with open(path, "r", encoding="utf-8") as f:
    for raw in f:
      line = raw.split("#", 1)[0].strip()
      if not line:
        continue
      line = line.replace(",", " ")
      nums = [int(tok) for tok in line.split()]
      sets.append(nums)
  return sets

def main():
  datasets = read_sets("datasets.txt")
  if not datasets:
    print("No se encontraron sets en el archivo. Verificá que tengas datasets.txt en el directorio")
    return
  
  results = []
  for i, arr in enumerate(datasets, start=1):
    best_sum, subseq = max_subarray_backtracking(arr)
    results.append((i, arr, best_sum, subseq))
    print(f"== Set {i} ==")
    print(f"Input: {arr}")
    print(f"Mejor suma: {best_sum}")
    print(f"Subsecuencia óptima: {subseq}\n")

  with open("results.txt", "w", encoding="utf-8") as out:
    for i, arr, best_sum, subseq in results:
      out.write(f"== Set {i} ==\n")
      out.write(f"Input: {arr}\n")
      out.write(f"Mejor suma: {best_sum}\n")
      out.write(f"Subsecuencia óptima: {subseq}\n\n")

  print("Resultados guardados en results.txt")

if __name__ == "__main__":
  main()