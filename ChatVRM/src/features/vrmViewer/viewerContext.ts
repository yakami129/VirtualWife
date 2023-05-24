import { createContext } from "react";
import { Viewer } from "./viewer";

const viewer = new Viewer();

export const ViewerContext = createContext({ viewer });
