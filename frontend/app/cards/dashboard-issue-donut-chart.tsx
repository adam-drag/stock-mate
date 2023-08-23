'use client';

import {
    Card,
    Col,
    DeltaType,
    DeltaBar,
    DonutChart,
    Dropdown,
    DropdownItem,
    Flex,
    List,
    ListItem,
    Text,
    Title,
    Bold,
    Grid,
    Color,
} from "@tremor/react";
import { IssueStat } from "../../models/issue-stat";

export default function DashboardIssueDonutChart({issueStats}:{issueStats:Array<IssueStat>}) {
    

    return (
        <Card className="max-w-4xl mx-auto">
            <Grid numColsLg={1} className="mt-1 gap-y-10 gap-x-14">
                <Flex>
                    <DonutChart
                        data={issueStats}
                        category='quantity'
                        showLabel={true}
                        id="severity"
                        index="severity"
                        variant='donut'
                        colors={["rose", "amber", "zinc"]}
                        label="Issues"
                    />
                </Flex>
                <Col numColSpan={1} numColSpanLg={2}>
                    <Flex>
                        <Text className="truncate">
                            <Bold>Issue</Bold>
                        </Text>
                        <Text>
                            <Bold>Diff since last update</Bold>
                        </Text>
                    </Flex>
                    <div className="hidden sm:block">
                        <List className="mt-1">
                            {issueStats.map((issue) => (
                                <ListItem key={issue.severity}>
                                    <Text className="truncate" color={issue.color}>{issue.severity}: {issue.quantity}</Text>
                                    <div>
                                        <Flex justifyContent="end" className="space-x-4">
                                            <Text color={issue.delta > 0 ? 'red' : issue.delta === 0 ? 'zinc':'green' } className="truncate">
                                                {Intl.NumberFormat("us", {
                                                    signDisplay: "exceptZero",
                                                })
                                                    .format(issue.delta)
                                                    .toString()}
                                                
                                            </Text>

                                        </Flex>
                                    </div>
                                </ListItem>
                            ))}
                        </List>
                    </div>
                </Col>
            </Grid>
        </Card>
    );
}