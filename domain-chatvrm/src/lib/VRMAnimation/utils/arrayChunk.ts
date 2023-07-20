/**
 * ```js
 * arrayChunk( [ 1, 2, 3, 4, 5, 6 ], 2 )
 * // will be
 * [ [ 1, 2 ], [ 3, 4 ], [ 5, 6 ] ]
 * ```
 */
export function arrayChunk<T>(array: ArrayLike<T>, every: number): T[][] {
  const N = array.length;

  const ret: T[][] = [];

  let current: T[] = [];
  let remaining = 0;

  for (let i = 0; i < N; i ++) {
    const el = array[i];

    if (remaining <= 0) {
      remaining = every;
      current = [];
      ret.push(current);
    }

    current.push(el);
    remaining--;
  }

  return ret;
}
