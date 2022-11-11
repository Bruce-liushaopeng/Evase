import React from 'react'

import Icon from '@mdi/react'
import {
    mdiArchiveCancelOutline,
    mdiCloudUploadOutline,
    mdiFileChartCheckOutline,
    mdiDotsVertical,
    mdiFileChartOutline
} from '@mdi/js'

import { 
    Card,
    CardHeader,
    CardAction,
    CardContent,
    ProgressCircular,
    Button,
    Radio,
    RadioGroup,
    H6,
    Subtitle2,
    IconButton,
    Body2,
    withResize
} from 'ui-neumorphism'


class AnalysisForm extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
        <>
            <CardHeader 
            title={<H6>{this.props.title}</H6>}
            subtitle={<Subtitle2>{this.props.subtitle}</Subtitle2>}
            action={
                <IconButton>
                    <Icon path={mdiDotsVertical} size={1}></Icon>
                </IconButton>
                }
            />
            <CardContent>
                <ProgressCircular
                    indeterminate={true}
                />
                <RadioGroup vertical>
                    <Radio checked={false} label="SQL Injection"/>
                    <Radio checked={false} label="Deadlock"/>
                    <Radio checked={false} label="Password Encryption"/>
                </RadioGroup>
                <Button rounded>Analze</Button>
            </CardContent>
        </>
        );
    }
}

export default withResize(AnalysisForm);