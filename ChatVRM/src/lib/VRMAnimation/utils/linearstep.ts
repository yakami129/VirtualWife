import { saturate } from './saturate';

export const linearstep = (a: number, b: number, t: number) => (
  saturate((t - a) / (b - a))
);
