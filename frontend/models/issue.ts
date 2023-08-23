import {  Product } from "./product";

export enum IssueSeverity {
    SEVERE = "Severe",
    MAJOR = "Major",
    LOW = "Low"
}

export interface Issue {
    id: String,
    severity: IssueSeverity,
    product: Product
}
