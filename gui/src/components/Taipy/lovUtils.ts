import { useMemo } from "react";

import { TaipyBaseProps, TaipyImage } from "./utils";

export interface LovItem {
    id: string;
    item: string | TaipyImage;
}

export interface LovProps extends TaipyBaseProps {
    defaultLov?: string;
    lov: LoV;
    value?: string | string[];
}

export type LoV = [string, string | TaipyImage][];

export const useLovListMemo = (lov: LoV, defaultLov: string): LovItem[] =>
    useMemo(() => {
        if (lov) {
            if (lov.length && lov[0][0] === undefined) {
                console.debug("Selector lov wrong format ", lov);
                return [];
            }
            return lov.map((elt) => ({ id: elt[0], item: elt[1] || elt[0] }));
        } else if (defaultLov) {
            let parsedLov;
            try {
                parsedLov = JSON.parse(defaultLov);
            } catch (e) {
                parsedLov = [];
            }
            return parsedLov.map((elt: [string, string | TaipyImage]) => ({ id: elt[0], item: elt[1] || elt[0] }));
        }
        return [];
    }, [lov, defaultLov]);