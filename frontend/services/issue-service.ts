import { Issue, IssueSeverity } from "../models/issue";
import { IssueStat } from "../models/issue-stat";
import {  Product } from "../models/product";

export class IssueService {


    getIssuesSummary(): Array<IssueStat> {
        return [
            {
                severity: IssueSeverity.SEVERE,
                quantity: 3,
                delta: 1,
                color: 'rose'
            },
            {
                severity: IssueSeverity.MAJOR,
                quantity: 5,
                delta: -1,
                color: 'amber'
            },
            {
                severity: IssueSeverity.LOW,
                quantity: 10,
                delta: 0,
                color: 'zinc'
            }
        ]
    }

    getProductIssues(product: Product): Array<Issue> {
        return [
            {
                id: 'is_01',
                severity: IssueSeverity.SEVERE,
                product: product
            }, 
            {
                id: 'is_02',
                severity: IssueSeverity.LOW,
                product: product
            },
        ]
    }
}