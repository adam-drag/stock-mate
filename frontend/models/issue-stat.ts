import { Color } from "@tremor/react";

export interface IssueStat {
    severity: string,
    quantity: number,
    delta: number,
    color: Color
}