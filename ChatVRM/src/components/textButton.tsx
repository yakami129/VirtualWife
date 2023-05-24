import { ButtonHTMLAttributes } from "react";
type Props = ButtonHTMLAttributes<HTMLButtonElement>;

export const TextButton = (props: Props) => {
  return (
    <button
      {...props}
      className={`px-24 py-8 text-white font-bold bg-primary hover:bg-primary-hover active:bg-primary-press-press disabled:bg-primary-disabled rounded-oval  ${props.className}`}
    >
      {props.children}
    </button>
  );
};
